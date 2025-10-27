@echo off
SETLOCAL

REM Launch IBE-100 v1.6.0 from the correct location
SET "APP_PATH=E:\NEW DOWNLOADS\Enc-100\Encoder-100\IBE-100_v1.4.0\dist\IBE-100_v1.6.0\IBE-100.exe"

REM Check if the executable exists
IF NOT EXIST "%APP_PATH%" (
    ECHO Error: IBE-100.exe not found at "%APP_PATH%".
    ECHO Please ensure the application is built and located in the correct directory.
    GOTO :EOF
)

REM Launch the application
ECHO ========================================
ECHO Launching IBE-100 v1.6.0
ECHO ========================================
ECHO New Features:
ECHO - NO hardcoded markers!
ECHO - Dynamic marker selection
ECHO - Preview command button
ECHO ========================================
ECHO.

START "" "%APP_PATH%"

ENDLOCAL
