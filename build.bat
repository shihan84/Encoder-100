@echo off
REM ITAssist Broadcast Encoder - 100 (IBE-100)
REM Professional Build Script for Windows
REM Cross-platform packaging and deployment

setlocal enabledelayedexpansion

REM Application Information
set APP_NAME=IBE-100
set APP_VERSION=1.0.0
set APP_DESCRIPTION=ITAssist Broadcast Encoder - 100 (IBE-100)

REM Build configuration
set BUILD_TYPE=%1
if "%BUILD_TYPE%"=="" set BUILD_TYPE=onefile

echo.
echo 🚀 %APP_DESCRIPTION% - Professional Build Script
echo 📱 Platform: Windows
echo 📦 Build Type: %BUILD_TYPE%
echo 🔧 Version: %APP_VERSION%
echo.

REM Function to print colored output (Windows doesn't support colors in batch)
goto :main

:print_status
echo ✅ %~1
goto :eof

:print_warning
echo ⚠️  %~1
goto :eof

:print_error
echo ❌ %~1
goto :eof

:print_info
echo ℹ️  %~1
goto :eof

:check_python
call :print_info "Checking Python installation..."
python --version >nul 2>&1
if errorlevel 1 (
    call :print_error "Python is not installed. Please install Python 3.8+ first."
    exit /b 1
)
call :print_status "Python found"
goto :eof

:check_pyinstaller
call :print_info "Checking PyInstaller installation..."
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    call :print_warning "PyInstaller not found. Installing..."
    pip install pyinstaller>=5.0.0
)
call :print_status "PyInstaller is ready"
goto :eof

:check_tsduck
call :print_info "Checking TSDuck installation..."
where tsp >nul 2>&1
if errorlevel 1 (
    call :print_warning "TSDuck not found in PATH. Please install TSDuck first."
    call :print_info "Installation instructions:"
    call :print_info "  Download from: https://tsduck.io/download/"
    call :print_info "  Or use: winget install tsduck"
    exit /b 1
)
call :print_status "TSDuck found"
goto :eof

:create_directories
call :print_info "Creating build directories..."
if not exist "build" mkdir build
if not exist "dist" mkdir dist
if not exist "specs" mkdir specs
if not exist "assets" mkdir assets
if not exist "installer" mkdir installer
call :print_status "Build directories created"
goto :eof

:install_dependencies
call :print_info "Installing Python dependencies..."
pip install -r requirements.txt
call :print_status "Dependencies installed"
goto :eof

:create_assets
call :print_info "Creating application assets..."

REM Create version info for Windows
echo VSVersionInfo( > assets\version_info.txt
echo   ffi=FixedFileInfo( >> assets\version_info.txt
echo     filevers=(1, 0, 0, 0), >> assets\version_info.txt
echo     prodvers=(1, 0, 0, 0), >> assets\version_info.txt
echo     mask=0x3f, >> assets\version_info.txt
echo     flags=0x0, >> assets\version_info.txt
echo     OS=0x40004, >> assets\version_info.txt
echo     fileType=0x1, >> assets\version_info.txt
echo     subtype=0x0, >> assets\version_info.txt
echo     date=(0, 0) >> assets\version_info.txt
echo   ), >> assets\version_info.txt
echo   kids=[ >> assets\version_info.txt
echo     StringFileInfo([ >> assets\version_info.txt
echo       StringTable( >> assets\version_info.txt
echo         u'040904B0', >> assets\version_info.txt
echo         [StringStruct(u'CompanyName', u'ITAssist Broadcast Solutions'), >> assets\version_info.txt
echo          StringStruct(u'FileDescription', u'%APP_DESCRIPTION%'), >> assets\version_info.txt
echo          StringStruct(u'FileVersion', u'%APP_VERSION%'), >> assets\version_info.txt
echo          StringStruct(u'InternalName', u'%APP_NAME%'), >> assets\version_info.txt
echo          StringStruct(u'LegalCopyright', u'© 2024 ITAssist Broadcast Solutions ^| Dubai • Mumbai • Gurugram'), >> assets\version_info.txt
echo          StringStruct(u'OriginalFilename', u'%APP_NAME%.exe'), >> assets\version_info.txt
echo          StringStruct(u'ProductName', u'%APP_DESCRIPTION%'), >> assets\version_info.txt
echo          StringStruct(u'ProductVersion', u'%APP_VERSION%')]) >> assets\version_info.txt
echo     ]), >> assets\version_info.txt
echo     VarFileInfo([VarStruct(u'Translation', [1033, 1200])]) >> assets\version_info.txt
echo   ] >> assets\version_info.txt
echo ) >> assets\version_info.txt

call :print_status "Version info created"
goto :eof

:build_application
call :print_info "Building %APP_NAME% application..."

if "%BUILD_TYPE%"=="onefile" (
    call :print_info "Creating single executable file..."
    pyinstaller --onefile --windowed ^
        --name "%APP_NAME%" ^
        --icon "assets\icon.ico" ^
        --add-data "scte35_final;scte35_final" ^
        --add-data "README.md;." ^
        --add-data "LICENSE.txt;." ^
        --hidden-import "PyQt6.QtCore" ^
        --hidden-import "PyQt6.QtWidgets" ^
        --hidden-import "PyQt6.QtGui" ^
        --hidden-import "psutil" ^
        --exclude-module "tkinter" ^
        --exclude-module "matplotlib" ^
        --exclude-module "numpy" ^
        --exclude-module "pandas" ^
        tsduck_gui_simplified.py
    
    call :print_status "Single executable created: dist\%APP_NAME%.exe"
    
) else if "%BUILD_TYPE%"=="onedir" (
    call :print_info "Creating directory distribution..."
    pyinstaller --onedir --windowed ^
        --name "%APP_NAME%" ^
        --icon "assets\icon.ico" ^
        --add-data "scte35_final;scte35_final" ^
        --add-data "README.md;." ^
        --add-data "LICENSE.txt;." ^
        --hidden-import "PyQt6.QtCore" ^
        --hidden-import "PyQt6.QtWidgets" ^
        --hidden-import "PyQt6.QtGui" ^
        --hidden-import "psutil" ^
        --exclude-module "tkinter" ^
        --exclude-module "matplotlib" ^
        --exclude-module "numpy" ^
        --exclude-module "pandas" ^
        tsduck_gui_simplified.py
    
    call :print_status "Directory distribution created: dist\%APP_NAME%"
    
) else if "%BUILD_TYPE%"=="spec" (
    call :print_info "Building using spec file..."
    pyinstaller specs\IBE-100.spec
    call :print_status "Spec-based build completed"
    
) else (
    call :print_error "Invalid build type: %BUILD_TYPE%"
    call :print_info "Valid options: onefile, onedir, spec"
    exit /b 1
)
goto :eof

:create_installer
call :print_info "Creating Windows installer..."

REM Create NSIS installer script
echo !define APP_NAME "%APP_NAME%" > installer\installer.nsi
echo !define APP_VERSION "%APP_VERSION%" >> installer\installer.nsi
echo !define APP_DESCRIPTION "%APP_DESCRIPTION%" >> installer\installer.nsi
echo. >> installer\installer.nsi
echo Name "${APP_NAME}" >> installer\installer.nsi
echo OutFile "dist\%APP_NAME%-%APP_VERSION%-installer.exe" >> installer\installer.nsi
echo InstallDir "$PROGRAMFILES\ITAssist\%APP_NAME%" >> installer\installer.nsi
echo. >> installer\installer.nsi
echo Section "MainSection" SEC01 >> installer\installer.nsi
echo   SetOutPath "$INSTDIR" >> installer\installer.nsi
echo   SetOverwrite ifnewer >> installer\installer.nsi
echo   File "dist\%APP_NAME%\*.*" >> installer\installer.nsi
echo   File /r "dist\%APP_NAME%\*" >> installer\installer.nsi
echo. >> installer\installer.nsi
echo   CreateDirectory "$SMPROGRAMS\ITAssist" >> installer\installer.nsi
echo   CreateShortCut "$SMPROGRAMS\ITAssist\%APP_NAME%.lnk" "$INSTDIR\%APP_NAME%.exe" >> installer\installer.nsi
echo   CreateShortCut "$DESKTOP\%APP_NAME%.lnk" "$INSTDIR\%APP_NAME%.exe" >> installer\installer.nsi
echo. >> installer\installer.nsi
echo   WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\%APP_NAME%" "DisplayName" "%APP_DESCRIPTION%" >> installer\installer.nsi
echo   WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\%APP_NAME%" "UninstallString" "$INSTDIR\uninstall.exe" >> installer\installer.nsi
echo   WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\%APP_NAME%" "DisplayVersion" "%APP_VERSION%" >> installer\installer.nsi
echo   WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\%APP_NAME%" "Publisher" "ITAssist Broadcast Solutions" >> installer\installer.nsi
echo. >> installer\installer.nsi
echo   WriteUninstaller "$INSTDIR\uninstall.exe" >> installer\installer.nsi
echo SectionEnd >> installer\installer.nsi
echo. >> installer\installer.nsi
echo Section "Uninstall" >> installer\installer.nsi
echo   Delete "$INSTDIR\*.*" >> installer\installer.nsi
echo   RMDir /r "$INSTDIR" >> installer\installer.nsi
echo   Delete "$SMPROGRAMS\ITAssist\%APP_NAME%.lnk" >> installer\installer.nsi
echo   Delete "$DESKTOP\%APP_NAME%.lnk" >> installer\installer.nsi
echo   RMDir "$SMPROGRAMS\ITAssist" >> installer\installer.nsi
echo   DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\%APP_NAME%" >> installer\installer.nsi
echo SectionEnd >> installer\installer.nsi

call :print_status "NSIS installer script created"
goto :eof

:clean_build
call :print_info "Cleaning build artifacts..."
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "__pycache__" rmdir /s /q "__pycache__"
call :print_status "Build artifacts cleaned"
goto :eof

:main
echo 🔧 Starting %APP_DESCRIPTION% build process...
echo.

REM Pre-build checks
call :check_python
call :check_pyinstaller
call :check_tsduck

REM Build setup
call :create_directories
call :install_dependencies
call :create_assets

REM Build application
call :build_application

REM Create installer
call :create_installer

echo.
call :print_status "🎉 Build completed successfully!"
call :print_info "📁 Output directory: dist\"
call :print_info "📦 Build type: %BUILD_TYPE%"
call :print_info "🔧 Platform: Windows"

REM Show output files
echo.
call :print_info "📋 Generated files:"
dir dist\ 2>nul || call :print_warning "No output files found"

goto :eof

REM Handle command line arguments
if "%1"=="clean" goto :clean_build
if "%1"=="help" goto :help
if "%1"=="-h" goto :help
if "%1"=="--help" goto :help
goto :main

:help
echo Usage: %0 [build_type]
echo.
echo Build types:
echo   onefile  - Single executable file (default)
echo   onedir   - Directory distribution
echo   spec     - Use PyInstaller spec file
echo   clean    - Clean build artifacts
echo   help     - Show this help
echo.
echo Examples:
echo   %0 onefile    # Create single executable
echo   %0 onedir     # Create directory distribution
echo   %0 clean      # Clean build artifacts
goto :eof
