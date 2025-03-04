import csv
import os
import re

### parameter setting ###
# LOG file path
# folder_path = "./LOG/async_serial_battery"
folder_path = "./LOG/async_serial_battery_r16"
# front part of LOG file name
file_name = "async_serial_battery_r16.linde-r16.ros.log.INFO"
# saved csv file name
csv_file = file_name+".csv"
# seperate file name to get the time and date info
pattern = re.compile(r"async_serial_battery_r16\.linde-r16\.ros\.log\.INFO\.(\d{8}-\d{6}\.\d+)")


# select and save file name which correspond expect file name
files = [f for f in os.listdir(folder_path) if f.startswith(file_name)]

# parse and sort timestamp
def extract_timestamp(filename):
    match = pattern.search(filename)
    return match.group(1) if match else ""

sorted_files = sorted(files, key=extract_timestamp)

# create csv and write tile
with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        '時間', '電壓', '電流', 'SOC', 'Temp Max', 'Temp Min', 'CellV Max', 'CellV Min',
        'CHG_Current', 'DSG_Current', 'Basic_Status0', 'Basic_Status1', 'Basic_Status2',
        'ExtendedStatus', 'SOCStatus', 'ErrorCode', 'Relay/Mos', 'Cycle', 'FW Version'
    ])


with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    # read all saved file name
    for file in sorted_files:
        time, voltage, current, soc, tempmax, tempmin, cellV_max = "", "", "", "", "", "", ""
        cellV_min, chg_current, dsg_current, basic_status0, basic_status1, basic_status2 = "", "", "", "", "", ""
        extendedStatus, socStatus, errorCode, relay_Mos, cycle, fw_version = "", "", "", "", "", ""

        with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    file_info, data = line.split("]")
                    value = data.split(":")
                    item = value[0].strip()
                except Exception as e:
                    print("Error: ", e)
                    item = ""

                if item == "時間":
                    time = value[1] + ":" + value[2] + ":" + value[3]
                elif item == "電壓":
                    voltage = value[1].strip()
                elif item == "電流":
                    current = value[1].strip()
                elif item == "SOC":
                    soc = value[1].strip()
                elif item == "Temp Max":
                    tempmax = value[1].strip()
                elif item == "Temp Min":
                    tempmin = value[1].strip()
                elif item == "CellV Max":
                    cellV_max = value[1].strip()
                elif item == "CellV Min":
                    cellV_min = value[1].strip()
                elif item == "CHG_Current":
                    chg_current = value[1].strip()
                elif item == "DSG_Current":
                    dsg_current = value[1].strip()
                elif item == "Basic_Status0":
                    basic_status0 = value[1].strip()
                elif item == "Basic_Status1":
                    basic_status1 = value[1].strip()
                elif item == "Basic_Status2":
                    basic_status2 = value[1].strip()
                elif item == "ExtendedStatus":
                    extendedStatus = value[1].strip()
                elif item == "SOCStatus":
                    socStatus = value[1].strip()
                elif item == "ErrorCode":
                    errorCode = value[1].strip()
                elif item == "Relay/Mos":
                    relay_Mos = value[1].strip()
                elif item == "Cycle":
                    cycle = value[1].strip()
                elif item == "FW Version":
                    fw_version = value[1].strip()

                if all([time, voltage, current, soc, tempmax, tempmin, cellV_max, cellV_min,
                        chg_current, dsg_current, basic_status0, basic_status1, basic_status2,
                        extendedStatus, socStatus, errorCode, relay_Mos, cycle, fw_version]):
                    writer.writerow([
                        time, voltage, current, soc, tempmax, tempmin, cellV_max, cellV_min,
                        chg_current, dsg_current, basic_status0, basic_status1, basic_status2,
                        extendedStatus, socStatus, errorCode, relay_Mos, cycle, fw_version
                    ])

                    time, voltage, current, soc, tempmax, tempmin, cellV_max = "", "", "", "", "", "", ""
                    cellV_min, chg_current, dsg_current, basic_status0, basic_status1, basic_status2 = "", "", "", "", "", ""
                    extendedStatus, socStatus, errorCode, relay_Mos, cycle, fw_version = "", "", "", "", "", ""

print(f"CSV save as {csv_file}")

