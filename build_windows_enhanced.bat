@echo off
REM Enhanced Windows Build Script for IBE-100 v1.1.0
REM Professional SCTE-35 Streaming Solution for Distributors

echo.
echo ========================================
echo IBE-100 v1.1.0 - Windows Build Script
echo Professional SCTE-35 Streaming Solution
echo ========================================
echo.

REM Set version and application info
set APP_NAME=IBE-100
set APP_VERSION=1.1.0
set BUILD_TYPE=%1
if "%BUILD_TYPE%"=="" set BUILD_TYPE=onefile

echo 🚀 Starting IBE-100 v%APP_VERSION% build process...
echo 📱 Platform: Windows
echo 📦 Build Type: %BUILD_TYPE%
echo 🔧 Version: %APP_VERSION%
echo.

REM Check Python installation
echo ℹ️  Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.9+ and try again.
    pause
    exit /b 1
)
echo ✅ Python found

REM Check PyInstaller
echo ℹ️  Checking PyInstaller installation...
python -c "import PyInstaller" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  PyInstaller not found. Installing...
    pip install pyinstaller>=5.0.0
    if %errorlevel% neq 0 (
        echo ❌ Failed to install PyInstaller
        pause
        exit /b 1
    )
)
echo ✅ PyInstaller is ready

REM Check TSDuck (optional)
echo ℹ️  Checking TSDuck installation...
where tsp >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  TSDuck not found. Please install TSDuck for full functionality.
    echo    Download from: https://tsduck.io/download/
) else (
    echo ✅ TSDuck found
)

REM Create build directories
echo ℹ️  Creating build directories...
if not exist "build" mkdir build
if not exist "dist" mkdir dist
if not exist "releases" mkdir releases
echo ✅ Build directories created

REM Install dependencies
echo ℹ️  Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)
echo ✅ Dependencies installed

REM Create application assets
echo ℹ️  Creating application assets...
if not exist "assets" mkdir assets
echo ✅ Application assets ready

REM Build application
echo ℹ️  Building %APP_NAME% application...

if "%BUILD_TYPE%"=="onefile" (
    echo ℹ️  Creating single executable file...
    python -m PyInstaller --onefile --windowed ^
        --name "%APP_NAME%" ^
        --icon "assets/icon.ico" ^
        --add-data "scte35_final;scte35_final" ^
        --add-data "scte35_templates;scte35_templates" ^
        --add-data "README.md;." ^
        --add-data "LICENSE.txt;." ^
        --hidden-import "PyQt6.QtCore" ^
        --hidden-import "PyQt6.QtWidgets" ^
        --hidden-import "PyQt6.QtGui" ^
        --hidden-import "psutil" ^
        --hidden-import "threefive" ^
        --exclude-module "tkinter" ^
        --exclude-module "matplotlib" ^
        --exclude-module "numpy" ^
        --exclude-module "pandas" ^
        enc100.py
    
    if %errorlevel% neq 0 (
        echo ❌ Build failed
        pause
        exit /b 1
    )
    
    echo ✅ Single executable created: dist\%APP_NAME%.exe
    
) else if "%BUILD_TYPE%"=="onedir" (
    echo ℹ️  Creating directory distribution...
    python -m PyInstaller --onedir --windowed ^
        --name "%APP_NAME%" ^
        --icon "assets/icon.ico" ^
        --add-data "scte35_final;scte35_final" ^
        --add-data "scte35_templates;scte35_templates" ^
        --add-data "README.md;." ^
        --add-data "LICENSE.txt;." ^
        --hidden-import "PyQt6.QtCore" ^
        --hidden-import "PyQt6.QtWidgets" ^
        --hidden-import "PyQt6.QtGui" ^
        --hidden-import "psutil" ^
        --hidden-import "threefive" ^
        --exclude-module "tkinter" ^
        --exclude-module "matplotlib" ^
        --exclude-module "numpy" ^
        --exclude-module "pandas" ^
        enc100.py
    
    if %errorlevel% neq 0 (
        echo ❌ Build failed
        pause
        exit /b 1
    )
    
    echo ✅ Directory distribution created: dist\%APP_NAME%
    
) else if "%BUILD_TYPE%"=="spec" (
    echo ℹ️  Building using spec file...
    python -m PyInstaller specs/IBE-100.spec
    if %errorlevel% neq 0 (
        echo ❌ Build failed
        pause
        exit /b 1
    )
    echo ✅ Spec-based build completed
    
) else (
    echo ❌ Invalid build type: %BUILD_TYPE%
    echo Valid options: onefile, onedir, spec
    pause
    exit /b 1
)

REM Create Windows installer (NSIS)
echo ℹ️  Creating Windows installer...
if exist "installer\nsis_installer.nsi" (
    if exist "C:\Program Files (x86)\NSIS\makensis.exe" (
        "C:\Program Files (x86)\NSIS\makensis.exe" installer\nsis_installer.nsi
        if %errorlevel% equ 0 (
            echo ✅ Windows installer created
        ) else (
            echo ⚠️  NSIS installer creation failed (NSIS may not be installed)
        )
    ) else (
        echo ⚠️  NSIS not found. Install NSIS to create Windows installer.
        echo    Download from: https://nsis.sourceforge.io/Download
    )
) else (
    echo ⚠️  NSIS installer script not found
)

REM Copy to releases folder
echo ℹ️  Copying files to releases folder...
if exist "dist\%APP_NAME%.exe" (
    copy "dist\%APP_NAME%.exe" "releases\%APP_NAME%-v%APP_VERSION%-Windows.exe"
    echo ✅ Windows executable copied to releases
)

if exist "dist\%APP_NAME%" (
    xcopy "dist\%APP_NAME%" "releases\%APP_NAME%-v%APP_VERSION%-Windows\" /E /I
    echo ✅ Windows directory distribution copied to releases
)

REM Create release info
echo ℹ️  Creating release information...
echo IBE-100 v%APP_VERSION% - Windows Build > releases\BUILD_INFO.txt
echo Build Date: %date% %time% >> releases\BUILD_INFO.txt
echo Build Type: %BUILD_TYPE% >> releases\BUILD_INFO.txt
echo Platform: Windows >> releases\BUILD_INFO.txt
echo Version: %APP_VERSION% >> releases\BUILD_INFO.txt
echo.

REM Show results
echo ✅ 🎉 Build completed successfully!
echo ℹ️  📁 Output directory: dist\
echo ℹ️  📦 Build type: %BUILD_TYPE%
echo ℹ️  🔧 Platform: Windows
echo ℹ️  📋 Generated files:
dir dist\
echo.
echo ℹ️  📁 Releases directory: releases\
dir releases\
echo.

echo 🎬 IBE-100 v%APP_VERSION% is ready for Windows!
echo 📋 Features included:
echo    ✅ SCTE-35 Marker Generation System
echo    ✅ Professional Template System
echo    ✅ Enhanced User Interface
echo    ✅ TSDuck Integration
echo    ✅ Cross-platform Compatibility
echo.
echo 🚀 Ready for professional broadcast operations!
pause
