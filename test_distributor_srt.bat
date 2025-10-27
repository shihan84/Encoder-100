@echo off
REM Test Distributor SRT Connection
REM Endpoint: srt://49.40.0.11:9636 (no stream ID)

SETLOCAL
echo.
echo ================================================================
echo   Testing Distributor SRT Connection
echo ================================================================
echo.
echo SRT Server: 49.40.0.11:9636
echo No stream ID required
echo.

REM Test 1: Basic connectivity
echo [1] Testing network connectivity to 49.40.0.11...
ping -n 2 49.40.0.11
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Cannot reach SRT server
    pause
    exit /b 1
)
echo [OK] Server is reachable
echo.

REM Test 2: Test SRT connection with TSDuck
echo [2] Testing SRT connection with TSDuck...
echo.
echo Note: This will attempt to connect as CALLER mode
echo.

REM Create a simple test command
echo Testing connection:
echo tsp -I null -P inject --pid 256 --file "test.ts" -O srt 49.40.0.11:9636 --caller --latency 2000

echo.
echo Attempting connection...
tsp -I null -P inject --pid 256 --file "test.ts" -O srt 49.40.0.11:9636 --caller --latency 2000

echo.
echo ================================================================
echo   Test Complete
echo ================================================================
pause

ENDLOCAL

