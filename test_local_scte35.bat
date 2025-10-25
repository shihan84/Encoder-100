@echo off
SETLOCAL

ECHO ============================================================
ECHO Local SCTE-35 Processing Test - IBE-100
ECHO ============================================================

SET "TSDUCK_BIN=C:\Program Files\TSDuck\bin\tsp.EXE"
SET "HLS_INPUT=https://cdn.itassist.one/BREAKING/NEWS/index.m3u8"
SET "SCTE35_FILE=scte35_final/preroll_10023.xml"

IF NOT EXIST "%TSDUCK_BIN%" (
    ECHO [ERROR] TSDuck not found at "%TSDUCK_BIN%". Please install TSDuck.
    GOTO :EOF
)

ECHO [INFO] Testing local SCTE-35 processing...
ECHO [INFO] This will test SCTE-35 marker injection locally without SRT.
ECHO [INFO] You can monitor this stream with: tsp -I ip 127.0.0.1:9999 -P analyze -O drop
ECHO.

REM --- Test local SCTE-35 processing ---
ECHO [STEP 1] Testing local SCTE-35 processing...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% ^
    -P sdt --service 1 --name "SCTE-35 Test Stream" --provider "ITAssist" ^
    -P remap 211=256 221=257 ^
    -P pmt --service 1 --add-pid 256/0x1b --add-pid 257/0x0f --add-pid 500/0x86 ^
    -P spliceinject --pid 500 --pts-pid 256 --files "%SCTE35_FILE%" ^
    --inject-count 1 --inject-interval 1000 --start-delay 2000 ^
    -O ip 127.0.0.1:9999

IF %ERRORLEVEL% EQU 0 (
    ECHO.
    ECHO [SUCCESS] Local SCTE-35 processing completed successfully!
    ECHO [INFO] SCTE-35 markers were injected correctly.
    ECHO [INFO] You can monitor the stream with: tsp -I ip 127.0.0.1:9999 -P analyze -O drop
) ELSE (
    ECHO.
    ECHO [ERROR] Local SCTE-35 processing failed with exit code %ERRORLEVEL%
    ECHO [INFO] Check the error messages above for specific issues.
)

ECHO.
ECHO [INFO] Test completed. Check the output above for results.

ENDLOCAL
