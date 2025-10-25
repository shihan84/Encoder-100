@echo off
SETLOCAL

REM ============================================================
REM IBE-100 v1.3.0 Launcher - Configuration Stability Release
REM ============================================================

REM Define the path to the executable for version 1.3.0
SET "APP_PATH=.\dist\IBE-100.exe"

REM Check if the executable exists
IF NOT EXIST "%APP_PATH%" (
    ECHO Error: IBE-100.exe not found at "%APP_PATH%".
    ECHO Please ensure the application is built and located in the 'dist' directory.
    GOTO :EOF
)

REM Display version information
ECHO ============================================================
ECHO ITAssist Broadcast Encoder - 100 (IBE-100) v1.3.0
ECHO Configuration Stability Release
ECHO ============================================================
ECHO.
ECHO Key Features:
ECHO - Zero Configuration Loading Crashes
ECHO - Professional SCTE-35 Interface
ECHO - Enhanced Error Handling
ECHO - Bulletproof Build Process
ECHO.
ECHO Launching application...

REM Launch the application
START "" "%APP_PATH%"

REM Optional: Add a delay or wait for the application to close
REM TIMEOUT /T 5 /NOBREAK > NUL
REM ECHO Application launched successfully.

ENDLOCAL
