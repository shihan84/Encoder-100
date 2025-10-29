@echo off
REM Test SRT Input Connection
echo Testing SRT input: cdn.itassist.one:8888
echo.
echo This will test if the input source is continuously available
echo Press Ctrl+C to stop
echo.

tsp -I srt cdn.itassist.one:8888 --transtype live --messageapi --latency 2000 --streamid "#!::r=srt_shrinews,m=request" -O drop

pause

