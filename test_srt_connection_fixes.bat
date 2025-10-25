@echo off
SETLOCAL

ECHO ============================================================
ECHO SRT Connection Troubleshooting - IBE-100
ECHO ============================================================

SET "TSDUCK_BIN=C:\Program Files\TSDuck\bin\tsp.EXE"
SET "HLS_INPUT=https://cdn.itassist.one/BREAKING/NEWS/index.m3u8"
SET "SRT_SERVER=cdn.itassist.one:8888"

IF NOT EXIST "%TSDUCK_BIN%" (
    ECHO [ERROR] TSDuck not found at "%TSDUCK_BIN%". Please install TSDuck.
    GOTO :EOF
)

ECHO [INFO] Testing various SRT connection parameters to resolve peer rejection...
ECHO [INFO] The error "Peer rejected connection" suggests server-side configuration issues.
ECHO.

REM --- Test 1: Basic SRT connection ---
ECHO [TEST 1] Testing basic SRT connection...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% -O srt --caller %SRT_SERVER% --latency 2000

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] Basic SRT connection works!
    GOTO :SUCCESS
) ELSE (
    ECHO [ERROR] Basic SRT connection failed with exit code %ERRORLEVEL%
)

ECHO.
REM --- Test 2: SRT with streamid ---
ECHO [TEST 2] Testing SRT with streamid...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% -O srt --caller %SRT_SERVER% --streamid "test" --latency 2000

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] SRT with streamid works!
    GOTO :SUCCESS
) ELSE (
    ECHO [ERROR] SRT with streamid failed with exit code %ERRORLEVEL%
)

ECHO.
REM --- Test 3: SRT with different streamid format ---
ECHO [TEST 3] Testing SRT with different streamid format...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% -O srt --caller %SRT_SERVER% --streamid "#!::r=test/test,m=publish" --latency 2000

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] SRT with different streamid format works!
    GOTO :SUCCESS
) ELSE (
    ECHO [ERROR] SRT with different streamid format failed with exit code %ERRORLEVEL%
)

ECHO.
REM --- Test 4: SRT with different latency ---
ECHO [TEST 4] Testing SRT with different latency...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% -O srt --caller %SRT_SERVER% --latency 1000

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] SRT with different latency works!
    GOTO :SUCCESS
) ELSE (
    ECHO [ERROR] SRT with different latency failed with exit code %ERRORLEVEL%
)

ECHO.
REM --- Test 5: SRT with different parameters ---
ECHO [TEST 5] Testing SRT with different parameters...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% -O srt --caller %SRT_SERVER% --latency 2000 --enforce-flow --max-reorder 100

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] SRT with different parameters works!
    GOTO :SUCCESS
) ELSE (
    ECHO [ERROR] SRT with different parameters failed with exit code %ERRORLEVEL%
)

ECHO.
REM --- Test 6: SRT with authentication ---
ECHO [TEST 6] Testing SRT with authentication...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% -O srt --caller %SRT_SERVER% --latency 2000 --passphrase "test"

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] SRT with authentication works!
    GOTO :SUCCESS
) ELSE (
    ECHO [ERROR] SRT with authentication failed with exit code %ERRORLEVEL%
)

ECHO.
REM --- Test 7: SRT with different port ---
ECHO [TEST 7] Testing SRT with different port...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% -O srt --caller cdn.itassist.one:9999 --latency 2000

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] SRT with different port works!
    GOTO :SUCCESS
) ELSE (
    ECHO [ERROR] SRT with different port failed with exit code %ERRORLEVEL%
)

ECHO.
REM --- Test 8: SRT with different host ---
ECHO [TEST 8] Testing SRT with different host...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% -O srt --caller 127.0.0.1:8888 --latency 2000

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] SRT with different host works!
    GOTO :SUCCESS
) ELSE (
    ECHO [ERROR] SRT with different host failed with exit code %ERRORLEVEL%
)

ECHO.
REM --- Test 9: SRT with different protocol ---
ECHO [TEST 9] Testing SRT with different protocol...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% -O srt --caller %SRT_SERVER% --latency 2000 --transtype live

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] SRT with different protocol works!
    GOTO :SUCCESS
) ELSE (
    ECHO [ERROR] SRT with different protocol failed with exit code %ERRORLEVEL%
)

ECHO.
REM --- Test 10: SRT with different mode ---
ECHO [TEST 10] Testing SRT with different mode...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% -O srt --caller %SRT_SERVER% --latency 2000 --mode caller

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] SRT with different mode works!
    GOTO :SUCCESS
) ELSE (
    ECHO [ERROR] SRT with different mode failed with exit code %ERRORLEVEL%
)

ECHO.
ECHO ============================================================
ECHO All SRT connection tests failed.
ECHO This indicates a server-side configuration issue.
ECHO Please contact your distributor for SRT server configuration.
ECHO ============================================================
GOTO :EOF

:SUCCESS
ECHO.
ECHO ============================================================
ECHO SRT connection test successful!
ECHO The working parameters can be used for production.
ECHO ============================================================

ENDLOCAL
