import csv

glog_file = 'ros_battery_driver.linde-r16.ros.log.INFO.20240703-141005.37470'
csv_file = glog_file+".csv"

time, voltage, current, soc, tempmax, tempmin, cellV_max = "", "", "", "", "", "", ""
cellV_min, chg_current, dsg_current, basic_status0, basic_status1, basic_status2 = "", "", "", "", "", ""
extendedStatus, socStatus, errorCode, relay_Mos, cycle, fw_version = "", "", "", "", "", ""

with open(glog_file, 'r') as f, open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['時間', '電壓', '電流', 'SOC', 'Temp Max', 'Temp Min', 'CellV Max', 'CellV Min', 'CHG_Current', 'DSG_Current',
                     'Basic_Status0', 'Basic_Status1', 'Basic_Status2', 'ExtendedStatus', 'SOCStatus', 'ErrorCode', 'Relay/Mos', 'Cycle', 'FW Version'])

    for line in f:
        try:
            filename, data = line.split("]")
            value = data.split(":")
            item = value[0].strip()
        except:
            item = ""

        if item == "時間":
            time = value[1]+":"+value[2]+":"+value[3]
        elif item == "電壓":
            voltage = value[1]
        elif item == "電流":
            current = value[1]
        elif item == "SOC":
            soc = value[1]
        elif item == "Temp Max":
            tempmax = value[1]
        elif item == "Temp Min":
            tempmin = value[1]
        elif item == "CellV Max":
            cellV_max = value[1]
        elif item == "CellV Min":
            cellV_min = value[1]
        elif item == "CHG_Current":
            chg_current = value[1]
        elif item == "DSG_Current":
            dsg_current = value[1]
        elif item == "Basic_Status0":
            basic_status0 = value[1]
        elif item == "Basic_Status1":
            basic_status1 = value[1]
        elif item == "Basic_Status2":
            basic_status2 = value[1]
        elif item == "ExtendedStatus":
            extendedStatus = value[1]
        elif item == "SOCStatus":
            socStatus = value[1]
        elif item == "ErrorCode":
            errorCode = value[1]
        elif item == "Relay/Mos":
            relay_Mos = value[1]
        elif item == "Cycle":
            cycle = value[1]
        elif item == "FW Version":
            fw_version = value[1]

        if time and voltage and current and soc and tempmax and tempmin and cellV_max and cellV_min and \
           chg_current and dsg_current and basic_status0 and basic_status1 and basic_status2 and \
           extendedStatus and socStatus and errorCode and relay_Mos and cycle and fw_version:
            writer.writerow([time, voltage, current, soc, tempmax, tempmin, cellV_max, cellV_min,
                            chg_current, dsg_current, basic_status0, basic_status1, basic_status2,
                            extendedStatus, socStatus, errorCode, relay_Mos, cycle, fw_version])

            time, voltage, current, soc, tempmax, tempmin, cellV_max = "", "", "", "", "", "", ""
            cellV_min, chg_current, dsg_current, basic_status0, basic_status1, basic_status2 = "", "", "", "", "", ""
            extendedStatus, socStatus, errorCode, relay_Mos, cycle, fw_version = "", "", "", "", "", ""
