# Parse LOG to csv
* This example code for convert LOG to csv. Prase LOG to make sure it's easy to view

* parameter setting
### LOG file path
```bash
folder_path = "./LOG/linde_base_node"
```
### front part of LOG file name
```bash
file_name = "linde_r16_base_node.linde-r16.ros.log.INFO"
```
### saved csv file name
```bash
csv_file = file_name+".csv"
```
### seperate file name to get the time and date info
```bash
pattern = re.compile(r"linde_r16_base_node\.linde-r16\.ros\.log\.INFO\.(\d{8}-\d{6}\.\d+)")
```