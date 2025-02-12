import csv
import os
import re

### parameter setting ###
# LOG file path
folder_path = "./LOG/agv_controller_node"
# front part of LOG file name
file_name = "agv_controller_node.linde-r16.ros.log.WARNING"
# saved csv file name
csv_file = file_name+".csv"
# seperate file name to get the time and date info
pattern = re.compile(r"agv_controller_node\.linde-r16\.ros\.log\.WARNING\.(\d{8}-\d{6}\.\d+)")


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
        'date', 'time', 'count'
    ])

with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    count = 0

    # read all saved file name
    for file in sorted_files:
        date, time = "", ""

        with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as f:
            # phrase each line of LOG
            for line in f:
                try:
                    file_info, data = line.split("]")
                    value = data.split(":")
                    item = value[0].strip()
                except:
                    item = ""

                if item == "pressure_test_forklift":
                    date = file_info.split(" ")[0]
                    time = file_info.split(" ")[1]
                    count = count + 1

                if all([date, time]):
                    writer.writerow([
                        date, time, count
                    ])
                    date, time = "", ""

print(f"CSV save as {csv_file}")

