@echo off
REM Test Stream to Distributor Endpoint
REM Server: 49.40.0.11:9636 (no stream ID)

SETLOCAL
echo.
echo ================================================================
echo   Testing Stream to Distributor Endpoint
echo ================================================================
echo.
echo Server: 49.40.0.11:9636
echo No Stream ID Required
echo.

REM Test basic connectivity
echo [1] Testing connectivity to 49.40.0.11...
ping -n 2 49.40.0.11
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Cannot reach server
    pause
    exit /b 1
)
echo [OK] Server is reachable
echo.

REM Test SRT connection
echo [2] Testing SRT connection (10 seconds test)...
echo.
echo This will attempt to send test stream for 10 seconds
echo Press Ctrl+C to stop early
echo.

timeout /t 1 /nobreak >nul

REM Create a simple test with TSDuck
echo Starting test stream...
tsp -I null -P inject --pid 256 --file "test.ts" -O srt 49.40.0.11:9636 --caller --latency 2000

echo.
echo Test complete!
pause

ENDLOCAL

