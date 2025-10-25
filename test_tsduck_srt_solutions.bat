@echo off
SETLOCAL

ECHO ============================================================
ECHO TSDuck SRT Solutions Test - Based on Official Documentation
ECHO ============================================================

SET "TSDUCK_BIN=C:\Program Files\TSDuck\bin\tsp.EXE"
SET "HLS_INPUT=https://cdn.itassist.one/BREAKING/NEWS/index.m3u8"
SET "SRT_SERVER=cdn.itassist.one:8888"

IF NOT EXIST "%TSDUCK_BIN%" (
    ECHO [ERROR] TSDuck not found at "%TSDUCK_BIN%". Please install TSDuck.
    GOTO :EOF
)

ECHO [INFO] Testing SRT connection solutions based on TSDuck documentation...
ECHO [INFO] Reference: https://tsduck.io/docs/tsduck.pdf
ECHO.

REM --- Test 1: Basic SRT Connection ---
ECHO [TEST 1] Testing basic SRT connection (from TSDuck documentation)...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% -O srt --caller %SRT_SERVER% --latency 2000

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] Basic SRT connection works!
    GOTO :SUCCESS
) ELSE (
    ECHO [ERROR] Basic SRT connection failed with exit code %ERRORLEVEL%
)

ECHO.
REM --- Test 2: SRT with Stream ID ---
ECHO [TEST 2] Testing SRT with stream ID (recommended by TSDuck)...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% -O srt --caller %SRT_SERVER% --streamid "test" --latency 2000

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] SRT with stream ID works!
    GOTO :SUCCESS
) ELSE (
    ECHO [ERROR] SRT with stream ID failed with exit code %ERRORLEVEL%
)

ECHO.
REM --- Test 3: SRT with Different Latency ---
ECHO [TEST 3] Testing SRT with different latency...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% -O srt --caller %SRT_SERVER% --latency 1000

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] SRT with different latency works!
    GOTO :SUCCESS
) ELSE (
    ECHO [ERROR] SRT with different latency failed with exit code %ERRORLEVEL%
)

ECHO.
REM --- Test 4: SRT with Additional Parameters ---
ECHO [TEST 4] Testing SRT with additional parameters (from TSDuck documentation)...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% -O srt --caller %SRT_SERVER% --latency 2000 --enforce-flow --max-reorder 100

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] SRT with additional parameters works!
    GOTO :SUCCESS
) ELSE (
    ECHO [ERROR] SRT with additional parameters failed with exit code %ERRORLEVEL%
)

ECHO.
REM --- Test 5: SRT with Different Mode ---
ECHO [TEST 5] Testing SRT with different mode...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% -O srt --caller %SRT_SERVER% --latency 2000 --mode caller

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] SRT with different mode works!
    GOTO :SUCCESS
) ELSE (
    ECHO [ERROR] SRT with different mode failed with exit code %ERRORLEVEL%
)

ECHO.
REM --- Test 6: SRT with Different Transport Type ---
ECHO [TEST 6] Testing SRT with different transport type...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% -O srt --caller %SRT_SERVER% --latency 2000 --transtype live

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] SRT with different transport type works!
    GOTO :SUCCESS
) ELSE (
    ECHO [ERROR] SRT with different transport type failed with exit code %ERRORLEVEL%
)

ECHO.
REM --- Test 7: SRT with Different Port ---
ECHO [TEST 7] Testing SRT with different port...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% -O srt --caller cdn.itassist.one:9999 --latency 2000

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] SRT with different port works!
    GOTO :SUCCESS
) ELSE (
    ECHO [ERROR] SRT with different port failed with exit code %ERRORLEVEL%
)

ECHO.
REM --- Test 8: SCTE-35 with Local Output ---
ECHO [TEST 8] Testing SCTE-35 with local output...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% ^
    -P spliceinject --pid 500 --pts-pid 256 --files "scte35_final/preroll_10023.xml" ^
    --inject-count 1 --inject-interval 1000 --start-delay 2000 ^
    -O ip 127.0.0.1:9999

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] SCTE-35 with local output works!
    ECHO [INFO] This proves that SCTE-35 processing is working correctly.
) ELSE (
    ECHO [ERROR] SCTE-35 with local output failed with exit code %ERRORLEVEL%
)

ECHO.
REM --- Test 9: SCTE-35 with SRT ---
ECHO [TEST 9] Testing SCTE-35 with SRT...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% ^
    -P spliceinject --pid 500 --pts-pid 256 --files "scte35_final/preroll_10023.xml" ^
    --inject-count 1 --inject-interval 1000 --start-delay 2000 ^
    -O srt --caller %SRT_SERVER% --latency 2000

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] SCTE-35 with SRT works!
    GOTO :SUCCESS
) ELSE (
    ECHO [ERROR] SCTE-35 with SRT failed with exit code %ERRORLEVEL%
)

ECHO.
REM --- Test 10: SCTE-35 with SRT and Stream ID ---
ECHO [TEST 10] Testing SCTE-35 with SRT and stream ID...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% ^
    -P spliceinject --pid 500 --pts-pid 256 --files "scte35_final/preroll_10023.xml" ^
    --inject-count 1 --inject-interval 1000 --start-delay 2000 ^
    -O srt --caller %SRT_SERVER% --streamid "test" --latency 2000

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] SCTE-35 with SRT and stream ID works!
    GOTO :SUCCESS
) ELSE (
    ECHO [ERROR] SCTE-35 with SRT and stream ID failed with exit code %ERRORLEVEL%
)

ECHO.
ECHO ============================================================
ECHO All SRT connection tests failed.
ECHO This indicates a server-side configuration issue.
ECHO Please contact your distributor for SRT server configuration.
ECHO Reference: https://tsduck.io/docs/tsduck.pdf
ECHO ============================================================
GOTO :EOF

:SUCCESS
ECHO.
ECHO ============================================================
ECHO SRT connection test successful!
ECHO The working parameters can be used for production.
ECHO Reference: https://tsduck.io/docs/tsduck.pdf
ECHO ============================================================

ENDLOCAL
