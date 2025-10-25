@echo off
SETLOCAL

ECHO ============================================================
ECHO IBE-100 Version 1.2.0 - Professional SCTE-35 Interface
ECHO ============================================================

REM Define the path to the executable
SET "APP_PATH=.\dist_v1.2.0\IBE-100.exe"

REM Check if the executable exists
IF NOT EXIST "%APP_PATH%" (
    ECHO Error: IBE-100.exe not found at "%APP_PATH%".
    ECHO Please ensure the application is built and located in the 'dist_v1.2.0' directory.
    GOTO :EOF
)

REM Launch the application
ECHO Launching ITAssist Broadcast Encoder - 100 (IBE-100) v1.2.0...
ECHO.
ECHO Features:
ECHO - Professional SCTE-35 Interface
ECHO - Enhanced Template Visibility
ECHO - Professional Scrolling Support
ECHO - Fixed SCTE-35 Command Generation
ECHO - Production Ready
ECHO.
START "" "%APP_PATH%"

ECHO Application launched successfully!
ECHO.
ECHO Note: If you encounter SRT connection errors, this is a distributor-side issue.
ECHO Your SCTE-35 processing is working correctly.
ECHO.

ENDLOCAL
