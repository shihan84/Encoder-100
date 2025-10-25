@echo off
SETLOCAL

ECHO ============================================================
ECHO SCTE-35 Local Test with TSAnalyzer - IBE-100
ECHO ============================================================

SET "TSDUCK_BIN=C:\Program Files\TSDuck\bin\tsp.EXE"
SET "HLS_INPUT=https://cdn.itassist.one/BREAKING/NEWS/index.m3u8"
SET "SCTE35_FILE=scte35_final/preroll_10023.xml"

IF NOT EXIST "%TSDUCK_BIN%" (
    ECHO [ERROR] TSDuck not found at "%TSDUCK_BIN%". Please install TSDuck.
    GOTO :EOF
)

ECHO [INFO] Testing SCTE-35 processing locally and analyzing with tsanalyzer...
ECHO [INFO] This will verify that SCTE-35 markers are being injected correctly.
ECHO.

REM --- Step 1: Test SCTE-35 processing locally ---
ECHO [STEP 1] Testing SCTE-35 processing locally...
ECHO [INFO] Starting SCTE-35 injection to local UDP port 127.0.0.1:9999
ECHO [INFO] This will run in the background for 30 seconds...
ECHO.

START /B "" "%TSDUCK_BIN%" -I hls %HLS_INPUT% ^
    -P spliceinject --pid 500 --pts-pid 256 --files "%SCTE35_FILE%" ^
    --inject-count 1 --inject-interval 1000 --start-delay 2000 ^
    -O ip 127.0.0.1:9999

REM --- Wait a moment for the stream to start ---
ECHO [INFO] Waiting for stream to start...
TIMEOUT /T 5 /NOBREAK > NUL

REM --- Step 2: Analyze the stream with tsanalyzer ---
ECHO [STEP 2] Analyzing stream with tsanalyzer...
ECHO [INFO] This will analyze the stream for SCTE-35 markers...
ECHO.

"%TSDUCK_BIN%" -I ip 127.0.0.1:9999 -P analyze -O drop

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] Stream analysis completed successfully!
    ECHO [INFO] Check the output above for SCTE-35 marker information.
) ELSE (
    ECHO [ERROR] Stream analysis failed with exit code %ERRORLEVEL%
    ECHO [INFO] This might indicate that the SCTE-35 injection is not working.
)

ECHO.
REM --- Step 3: Test basic stream without SCTE-35 ---
ECHO [STEP 3] Testing basic stream without SCTE-35...
ECHO [INFO] This will help compare the streams...
ECHO.

"%TSDUCK_BIN%" -I hls %HLS_INPUT% -O ip 127.0.0.1:9998

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] Basic stream works!
    ECHO [INFO] You can compare this with the SCTE-35 stream.
) ELSE (
    ECHO [ERROR] Basic stream failed with exit code %ERRORLEVEL%
)

ECHO.
REM --- Step 4: Analyze basic stream ---
ECHO [STEP 4] Analyzing basic stream...
ECHO [INFO] This will analyze the basic stream for comparison...
ECHO.

"%TSDUCK_BIN%" -I ip 127.0.0.1:9998 -P analyze -O drop

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] Basic stream analysis completed!
    ECHO [INFO] Compare this with the SCTE-35 stream analysis above.
) ELSE (
    ECHO [ERROR] Basic stream analysis failed with exit code %ERRORLEVEL%
)

ECHO.
ECHO ============================================================
ECHO SCTE-35 test and analysis completed.
ECHO Check the output above for SCTE-35 marker information.
ECHO Look for:
ECHO - SCTE-35 splice information tables
ECHO - SCTE-35 markers in the stream
ECHO - PID 500 (SCTE-35 PID) information
ECHO - Any errors or warnings
ECHO ============================================================

ENDLOCAL
