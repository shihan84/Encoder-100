@echo off
SETLOCAL

ECHO ============================================================
ECHO SCTE-35 XML File Issue Test - IBE-100
ECHO ============================================================

SET "TSDUCK_BIN=C:\Program Files\TSDuck\bin\tsp.EXE"
SET "HLS_INPUT=https://cdn.itassist.one/BREAKING/NEWS/index.m3u8"

IF NOT EXIST "%TSDUCK_BIN%" (
    ECHO [ERROR] TSDuck not found at "%TSDUCK_BIN%". Please install TSDuck.
    GOTO :EOF
)

ECHO [INFO] Testing SCTE-35 XML file processing...
ECHO [INFO] This will help identify if the issue is with XML files or SRT connection.
ECHO.

REM --- Test 1: Basic SRT connection without SCTE-35 ---
ECHO [TEST 1] Testing basic SRT connection without SCTE-35...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% -O srt --caller cdn.itassist.one:8888 --latency 2000

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] Basic SRT connection works!
    ECHO [INFO] The issue is with SCTE-35 XML processing, not SRT connection.
) ELSE (
    ECHO [ERROR] Basic SRT connection failed with exit code %ERRORLEVEL%
    ECHO [INFO] The issue is with SRT connection, not SCTE-35 XML processing.
)

ECHO.
ECHO [TEST 2] Testing SCTE-35 with local UDP output...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% ^
    -P spliceinject --pid 500 --pts-pid 256 --files "scte35_final/preroll_10023.xml" ^
    --inject-count 1 --inject-interval 1000 --start-delay 2000 ^
    -O ip 127.0.0.1:9999

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] SCTE-35 processing works locally!
    ECHO [INFO] The issue is with SRT connection, not SCTE-35 processing.
) ELSE (
    ECHO [ERROR] SCTE-35 processing failed with exit code %ERRORLEVEL%
    ECHO [INFO] The issue is with SCTE-35 XML processing.
)

ECHO.
ECHO [TEST 3] Testing with different XML file...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% ^
    -P spliceinject --pid 500 --pts-pid 256 --files "scte35_final/preroll_10023_1761394095.xml" ^
    --inject-count 1 --inject-interval 1000 --start-delay 2000 ^
    -O ip 127.0.0.1:9999

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] SCTE-35 processing with different XML file works!
    ECHO [INFO] The issue might be with the specific XML file.
) ELSE (
    ECHO [ERROR] SCTE-35 processing with different XML file failed with exit code %ERRORLEVEL%
    ECHO [INFO] The issue is with SCTE-35 XML processing in general.
)

ECHO.
ECHO ============================================================
ECHO Test completed. Check the results above to identify the issue.
ECHO ============================================================

ENDLOCAL
