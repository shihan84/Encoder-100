#!/bin/bash
# ITAssist Broadcast Encoder - 100 (IBE-100)
# Professional Build Script for macOS/Linux
# Cross-platform packaging and deployment

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Application Information
APP_NAME="IBE-100"
APP_VERSION="1.0.0"
APP_DESCRIPTION="ITAssist Broadcast Encoder - 100 (IBE-100)"

# Build configuration
BUILD_TYPE=${1:-"onefile"}  # onefile or onedir
PLATFORM=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)

echo -e "${BLUE}🚀 ${APP_DESCRIPTION} - Professional Build Script${NC}"
echo -e "${CYAN}📱 Platform: ${PLATFORM} (${ARCH})${NC}"
echo -e "${CYAN}📦 Build Type: ${BUILD_TYPE}${NC}"
echo -e "${CYAN}🔧 Version: ${APP_VERSION}${NC}"
echo ""

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if Python is installed
check_python() {
    print_info "Checking Python installation..."
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.8+ first."
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_status "Python ${PYTHON_VERSION} found"
}

# Check if PyInstaller is installed
check_pyinstaller() {
    print_info "Checking PyInstaller installation..."
    if ! python3 -c "import PyInstaller" &> /dev/null; then
        print_warning "PyInstaller not found. Installing..."
        pip3 install pyinstaller>=5.0.0
    fi
    
    # Check if PyInstaller can be run
    if ! python3 -m PyInstaller --version &> /dev/null; then
        print_error "PyInstaller is not accessible via python3 -m PyInstaller"
        exit 1
    fi
    print_status "PyInstaller is ready"
}

# Check if TSDuck is installed
check_tsduck() {
    print_info "Checking TSDuck installation..."
    if command -v tsp &> /dev/null; then
        TSP_PATH=$(which tsp)
        print_status "TSDuck found at: ${TSP_PATH}"
    else
        print_warning "TSDuck not found in PATH. Please install TSDuck first."
        print_info "Installation instructions:"
        print_info "  macOS: brew install tsduck"
        print_info "  Linux: sudo apt-get install tsduck (Ubuntu/Debian)"
        print_info "  Linux: sudo yum install tsduck (CentOS/RHEL)"
        exit 1
    fi
}

# Create build directories
create_directories() {
    print_info "Creating build directories..."
    mkdir -p build dist specs assets installer
    print_status "Build directories created"
}

# Install dependencies
install_dependencies() {
    print_info "Installing Python dependencies..."
    pip3 install -r requirements.txt
    print_status "Dependencies installed"
}

# Create assets
create_assets() {
    print_info "Creating application assets..."
    
    # Create placeholder icon (if not exists)
    if [ ! -f "assets/icon.png" ]; then
        print_warning "Creating placeholder icon..."
        # Create a simple 256x256 PNG icon (placeholder)
        python3 -c "
from PIL import Image, ImageDraw, ImageFont
import os

# Create 256x256 image
img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Draw background circle
draw.ellipse([20, 20, 236, 236], fill=(33, 150, 243, 255), outline=(255, 255, 255, 255), width=4)

# Draw text
try:
    font = ImageFont.truetype('/System/Library/Fonts/Arial.ttf', 48)
except:
    font = ImageFont.load_default()

text = 'IBE-100'
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
x = (256 - text_width) // 2
y = (256 - text_height) // 2

draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
img.save('assets/icon.png')
print('✅ Placeholder icon created')
" 2>/dev/null || print_warning "Could not create icon (PIL not available)"
    fi
    
    # Create version info for Windows
    if [ "$PLATFORM" = "linux" ] && command -v wine &> /dev/null; then
        print_info "Creating Windows version info..."
        cat > assets/version_info.txt << EOF
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'ITAssist Broadcast Solutions'),
         StringStruct(u'FileDescription', u'${APP_DESCRIPTION}'),
         StringStruct(u'FileVersion', u'${APP_VERSION}'),
         StringStruct(u'InternalName', u'${APP_NAME}'),
         StringStruct(u'LegalCopyright', u'© 2024 ITAssist Broadcast Solutions | Dubai • Mumbai • Gurugram'),
         StringStruct(u'OriginalFilename', u'${APP_NAME}.exe'),
         StringStruct(u'ProductName', u'${APP_DESCRIPTION}'),
         StringStruct(u'ProductVersion', u'${APP_VERSION}')])
    ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
EOF
        print_status "Version info created"
    fi
}

# Build application
build_application() {
    print_info "Building ${APP_NAME} application..."
    
    if [ "$BUILD_TYPE" = "onefile" ]; then
        print_info "Creating single executable file..."
        python3 -m PyInstaller --onefile --windowed \
            --name "${APP_NAME}" \
            --icon "assets/icon.png" \
            --add-data "scte35_final:scte35_final" \
            --add-data "README.md:." \
            --add-data "LICENSE.txt:." \
            --hidden-import "PyQt6.QtCore" \
            --hidden-import "PyQt6.QtWidgets" \
            --hidden-import "PyQt6.QtGui" \
            --hidden-import "psutil" \
            --exclude-module "tkinter" \
            --exclude-module "matplotlib" \
            --exclude-module "numpy" \
            --exclude-module "pandas" \
            enc100.py
        
        print_status "Single executable created: dist/${APP_NAME}"
        
    elif [ "$BUILD_TYPE" = "onedir" ]; then
        print_info "Creating directory distribution..."
        python3 -m PyInstaller --onedir --windowed \
            --name "${APP_NAME}" \
            --icon "assets/icon.png" \
            --add-data "scte35_final:scte35_final" \
            --add-data "README.md:." \
            --add-data "LICENSE.txt:." \
            --hidden-import "PyQt6.QtCore" \
            --hidden-import "PyQt6.QtWidgets" \
            --hidden-import "PyQt6.QtGui" \
            --hidden-import "psutil" \
            --exclude-module "tkinter" \
            --exclude-module "matplotlib" \
            --exclude-module "numpy" \
            --exclude-module "pandas" \
            enc100.py
        
        print_status "Directory distribution created: dist/${APP_NAME}"
        
    elif [ "$BUILD_TYPE" = "spec" ]; then
        print_info "Building using spec file..."
        python3 -m PyInstaller specs/IBE-100.spec
        print_status "Spec-based build completed"
        
    else
        print_error "Invalid build type: ${BUILD_TYPE}"
        print_info "Valid options: onefile, onedir, spec"
        exit 1
    fi
}

# Create installer (platform-specific)
create_installer() {
    print_info "Creating platform-specific installer..."
    
    if [ "$PLATFORM" = "darwin" ]; then
        print_info "Creating macOS DMG installer..."
        # Create DMG using hdiutil
        if [ -d "dist/${APP_NAME}.app" ]; then
            hdiutil create -volname "${APP_NAME}" -srcfolder "dist/${APP_NAME}.app" -ov -format UDZO "dist/${APP_NAME}-${APP_VERSION}.dmg"
            print_status "macOS DMG created: dist/${APP_NAME}-${APP_VERSION}.dmg"
        fi
        
    elif [ "$PLATFORM" = "linux" ]; then
        print_info "Creating Linux AppImage..."
        # Create AppImage (requires appimagetool)
        if command -v appimagetool &> /dev/null; then
            if [ -d "dist/${APP_NAME}" ]; then
                appimagetool "dist/${APP_NAME}" "dist/${APP_NAME}-${APP_VERSION}.AppImage"
                print_status "Linux AppImage created: dist/${APP_NAME}-${APP_VERSION}.AppImage"
            fi
        else
            print_warning "appimagetool not found. Install with: wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage && chmod +x appimagetool-x86_64.AppImage && sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool"
        fi
    fi
}

# Clean build artifacts
clean_build() {
    print_info "Cleaning build artifacts..."
    rm -rf build/ dist/ __pycache__/
    print_status "Build artifacts cleaned"
}

# Main build process
main() {
    echo -e "${PURPLE}🔧 Starting ${APP_DESCRIPTION} build process...${NC}"
    echo ""
    
    # Pre-build checks
    check_python
    check_pyinstaller
    check_tsduck
    
    # Build setup
    create_directories
    install_dependencies
    create_assets
    
    # Build application
    build_application
    
    # Create installer
    create_installer
    
    echo ""
    print_status "🎉 Build completed successfully!"
    print_info "📁 Output directory: dist/"
    print_info "📦 Build type: ${BUILD_TYPE}"
    print_info "🔧 Platform: ${PLATFORM} (${ARCH})"
    
    # Show output files
    echo ""
    print_info "📋 Generated files:"
    ls -la dist/ 2>/dev/null || print_warning "No output files found"
}

# Handle command line arguments
case "${1:-}" in
    "clean")
        clean_build
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [build_type]"
        echo ""
        echo "Build types:"
        echo "  onefile  - Single executable file (default)"
        echo "  onedir   - Directory distribution"
        echo "  spec     - Use PyInstaller spec file"
        echo "  clean    - Clean build artifacts"
        echo "  help     - Show this help"
        echo ""
        echo "Examples:"
        echo "  $0 onefile    # Create single executable"
        echo "  $0 onedir     # Create directory distribution"
        echo "  $0 clean      # Clean build artifacts"
        ;;
    *)
        main
        ;;
esac
