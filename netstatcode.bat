@echo off
netstat -an -o > netstat_results.txt
findstr /c:":80 " netstat_results.txt
del netstat_results.txt
pause