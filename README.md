## Batch traceoute on real routers
###### Use netmiko and pandas to get traceroute result
###### 1. Install Libraries
```
pip install pandas
pip install pprint
pip install netmiko
```
###### 2. Put traceroute destination IPs in iplist.txt
###### 3. Proceed batch_tracerutes.py
###### 4. Select router, and clicke "Confirm RT"
###### 5. Enter VRF, click "Confirm VRF"
###### 6. Enter source IP, click "Confirm SrIP"
###### 7. Click "Confirm DstIPs", and select iplist.txt
###### 8. If you would like to change the data above, you can change them and click "Confirm" button accordingly.
###### 9. Click "All Confirmed" button
###### 10. You will get traceroutes_results.csv
###### _Note:_ you can also convert the .py to .exe file by the following steps:
###### - `pip install pyinstaller`
###### - Open PowerShell and excute `pyinstaller --onefile -w 'getTopTenSourceIP_V1_2.py'`
