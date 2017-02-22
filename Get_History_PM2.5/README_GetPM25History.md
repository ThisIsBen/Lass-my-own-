# Get_History_PM2.5
Get each Device's Mean PM2.5 value over the past one week for both "airbox" and "lass" ever 24 hrs,
and store it in "airboxHistory.csv" and "lassHistory.csv" under 
"/var/www/html/LASS/data/csv"  in the format of 
"ID,day1,day1_mean,......day7,day7_mean,total_mean"

Date Dec 26 2016

## Execution


```
	 sudo python GetPM25History.py

```
