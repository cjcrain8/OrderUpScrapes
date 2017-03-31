for /f %%x in ('wmic path win32_localtime get /format:list ^| findstr "="') do set %%x
set today=%Month%.%Day%.%Year%

echo %today%


schtasks /create /sc once /ri 5 /tn "BoulderScrape"  /st 12:00 /DU 24:00 /tr "D:Boulder_Scrapes\start_direct.cmd  boulder %today% 
