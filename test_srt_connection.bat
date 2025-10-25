@echo off
echo ============================================================
echo SRT Connection Test - IBE-100
echo ============================================================
echo.

echo [INFO] Testing SRT connection to cdn.itassist.one:8888
echo.

echo [STEP 1] Testing basic SRT connection...
tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 -O srt --caller cdn.itassist.one:8888 --streamid "#!::r=scte/scte,m=publish" --latency 2000

echo.
echo [STEP 2] If basic connection fails, try with different parameters...
tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 -O srt --caller cdn.itassist.one:8888 --streamid "#!::r=scte/scte,m=publish" --latency 2000 --transtype live --rcvbuf 10000000 --sndbuf 10000000

echo.
echo [STEP 3] If still failing, test local UDP output...
tsp -I hls https://cdn.itassist.one/BREAKING/NEWS/index.m3u8 -O ip 127.0.0.1:9999

echo.
echo [INFO] SRT connection test completed
echo [INFO] Check the output above for connection status
echo.
pause
