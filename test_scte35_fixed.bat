@echo off
SETLOCAL

ECHO ============================================================
ECHO SCTE-35 Fixed Test - IBE-100
ECHO ============================================================

SET "TSDUCK_BIN=C:\Program Files\TSDuck\bin\tsp.EXE"
SET "HLS_INPUT=https://cdn.itassist.one/BREAKING/NEWS/index.m3u8"
SET "SCTE35_FILE=scte35_final/preroll_10023.xml"

IF NOT EXIST "%TSDUCK_BIN%" (
    ECHO [ERROR] TSDuck not found at "%TSDUCK_BIN%". Please install TSDuck.
    GOTO :EOF
)

ECHO [INFO] Testing SCTE-35 processing with fixed multicast address...
ECHO [INFO] The previous error was due to using unicast address for multicast input.
ECHO.

REM --- Test 1: SCTE-35 with multicast output ---
ECHO [TEST 1] Testing SCTE-35 with multicast output...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% ^
    -P spliceinject --pid 500 --pts-pid 256 --files "%SCTE35_FILE%" ^
    --inject-count 1 --inject-interval 1000 --start-delay 2000 ^
    -O ip 224.1.1.1:9999

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] SCTE-35 with multicast output works!
    ECHO [INFO] Now analyzing the multicast stream...
    
    REM --- Analyze multicast stream ---
    ECHO [ANALYSIS] Analyzing multicast stream for SCTE-35 markers...
    "%TSDUCK_BIN%" -I ip 224.1.1.1:9999 -P analyze -O drop
    
    IF %ERRORLEVEL% EQU 0 (
        ECHO [SUCCESS] Stream analysis completed!
        ECHO [INFO] Check the output above for SCTE-35 marker information.
    ) ELSE (
        ECHO [ERROR] Stream analysis failed with exit code %ERRORLEVEL%
    )
) ELSE (
    ECHO [ERROR] SCTE-35 with multicast output failed with exit code %ERRORLEVEL%
)

ECHO.
REM --- Test 2: SCTE-35 with file output ---
ECHO [TEST 2] Testing SCTE-35 with file output...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% ^
    -P spliceinject --pid 500 --pts-pid 256 --files "%SCTE35_FILE%" ^
    --inject-count 1 --inject-interval 1000 --start-delay 2000 ^
    -O file test_scte35_output.ts

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] SCTE-35 with file output works!
    ECHO [INFO] Now analyzing the output file...
    
    REM --- Analyze output file ---
    ECHO [ANALYSIS] Analyzing output file for SCTE-35 markers...
    "%TSDUCK_BIN%" -I file test_scte35_output.ts -P analyze -O drop
    
    IF %ERRORLEVEL% EQU 0 (
        ECHO [SUCCESS] File analysis completed!
        ECHO [INFO] Check the output above for SCTE-35 marker information.
    ) ELSE (
        ECHO [ERROR] File analysis failed with exit code %ERRORLEVEL%
    )
) ELSE (
    ECHO [ERROR] SCTE-35 with file output failed with exit code %ERRORLEVEL%
)

ECHO.
REM --- Test 3: Basic stream without SCTE-35 ---
ECHO [TEST 3] Testing basic stream without SCTE-35...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% -O file test_basic_output.ts

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] Basic stream works!
    ECHO [INFO] Now analyzing the basic stream...
    
    REM --- Analyze basic stream ---
    ECHO [ANALYSIS] Analyzing basic stream for comparison...
    "%TSDUCK_BIN%" -I file test_basic_output.ts -P analyze -O drop
    
    IF %ERRORLEVEL% EQU 0 (
        ECHO [SUCCESS] Basic stream analysis completed!
        ECHO [INFO] Compare this with the SCTE-35 stream analysis above.
    ) ELSE (
        ECHO [ERROR] Basic stream analysis failed with exit code %ERRORLEVEL%
    )
) ELSE (
    ECHO [ERROR] Basic stream failed with exit code %ERRORLEVEL%
)

ECHO.
ECHO ============================================================
ECHO SCTE-35 fixed test completed.
ECHO Check the output above for SCTE-35 marker information.
ECHO Look for:
ECHO - SCTE-35 splice information tables
ECHO - SCTE-35 markers in the stream
ECHO - PID 500 (SCTE-35 PID) information
ECHO - Any errors or warnings
ECHO ============================================================

ENDLOCAL
