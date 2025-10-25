@echo off
SETLOCAL

ECHO ============================================================
ECHO IBE-100 SCTE-35 Stream with Latest Marker
ECHO ============================================================

REM Find the latest preroll marker file
SET "LATEST_MARKER="
FOR /F "delims=" %%i IN ('dir /B /O-D scte35_final\preroll_*.xml 2^>nul') DO (
    SET "LATEST_MARKER=%%i"
    GOTO :FOUND
)

:FOUND
IF "%LATEST_MARKER%"=="" (
    ECHO [ERROR] No preroll marker files found in scte35_final directory
    GOTO :EOF
)

ECHO [INFO] Using latest marker: %LATEST_MARKER%

REM Run TSDuck with the latest marker
"C:\Program Files\TSDuck\bin\tsp.EXE" -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 ^
    -P sdt --service 1 --name "SCTE-35 Stream" --provider "ITAssist" ^
    -P remap 211=256 221=257 ^
    -P pmt --service 1 --add-pid 256/0x1b --add-pid 257/0x0f --add-pid 500/0x86 ^
    -P spliceinject --pid 500 --pts-pid 256 --files "scte35_final/%LATEST_MARKER%" ^
    --inject-count 1 --inject-interval 1000 --start-delay 2000 ^
    -O srt --caller cdn.itassist.one:8888 --streamid "#!::r=scte/scte,m=publish"

ENDLOCAL
