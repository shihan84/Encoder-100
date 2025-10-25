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

ECHO [INFO] Testing SCTE-35 XML file loading issues...
ECHO [INFO] This will help identify if the issue is with file paths or XML content.
ECHO.

REM --- Test 1: Check if XML files exist ---
ECHO [TEST 1] Checking if XML files exist...
IF EXIST "scte35_final\preroll_10023.xml" (
    ECHO [SUCCESS] XML file exists: scte35_final\preroll_10023.xml
) ELSE (
    ECHO [ERROR] XML file not found: scte35_final\preroll_10023.xml
    GOTO :EOF
)

ECHO.
REM --- Test 2: Test with relative path ---
ECHO [TEST 2] Testing SCTE-35 with relative path...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% ^
    -P spliceinject --pid 500 --pts-pid 256 --files "scte35_final/preroll_10023.xml" ^
    --inject-count 1 --inject-interval 1000 --start-delay 2000 ^
    -O ip 127.0.0.1:9999

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] SCTE-35 with relative path works!
    GOTO :SUCCESS
) ELSE (
    ECHO [ERROR] SCTE-35 with relative path failed with exit code %ERRORLEVEL%
)

ECHO.
REM --- Test 3: Test with absolute path ---
ECHO [TEST 3] Testing SCTE-35 with absolute path...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% ^
    -P spliceinject --pid 500 --pts-pid 256 --files "E:\NEW DOWNLOADS\Enc-100\Encoder-100\scte35_final\preroll_10023.xml" ^
    --inject-count 1 --inject-interval 1000 --start-delay 2000 ^
    -O ip 127.0.0.1:9999

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] SCTE-35 with absolute path works!
    GOTO :SUCCESS
) ELSE (
    ECHO [ERROR] SCTE-35 with absolute path failed with exit code %ERRORLEVEL%
)

ECHO.
REM --- Test 4: Test with different XML file ---
ECHO [TEST 4] Testing SCTE-35 with different XML file...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% ^
    -P spliceinject --pid 500 --pts-pid 256 --files "scte35_final/preroll_10023_1761394095.xml" ^
    --inject-count 1 --inject-interval 1000 --start-delay 2000 ^
    -O ip 127.0.0.1:9999

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] SCTE-35 with different XML file works!
    GOTO :SUCCESS
) ELSE (
    ECHO [ERROR] SCTE-35 with different XML file failed with exit code %ERRORLEVEL%
)

ECHO.
REM --- Test 5: Test with JSON file ---
ECHO [TEST 5] Testing SCTE-35 with JSON file...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% ^
    -P spliceinject --pid 500 --pts-pid 256 --files "scte35_final/preroll_10023_1761394095.json" ^
    --inject-count 1 --inject-interval 1000 --start-delay 2000 ^
    -O ip 127.0.0.1:9999

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] SCTE-35 with JSON file works!
    GOTO :SUCCESS
) ELSE (
    ECHO [ERROR] SCTE-35 with JSON file failed with exit code %ERRORLEVEL%
)

ECHO.
REM --- Test 6: Test without SCTE-35 (basic stream) ---
ECHO [TEST 6] Testing basic stream without SCTE-35...
"%TSDUCK_BIN%" -I hls %HLS_INPUT% -O ip 127.0.0.1:9999

IF %ERRORLEVEL% EQU 0 (
    ECHO [SUCCESS] Basic stream works!
    ECHO [INFO] The issue is specifically with SCTE-35 XML file processing.
) ELSE (
    ECHO [ERROR] Basic stream failed with exit code %ERRORLEVEL%
    ECHO [INFO] The issue is with basic stream processing, not SCTE-35.
)

ECHO.
ECHO ============================================================
ECHO SCTE-35 XML file issue test completed.
ECHO Check the results above to identify the specific issue.
ECHO ============================================================
GOTO :EOF

:SUCCESS
ECHO.
ECHO ============================================================
ECHO SCTE-35 XML file test successful!
ECHO The working parameters can be used for production.
ECHO ============================================================

ENDLOCAL
