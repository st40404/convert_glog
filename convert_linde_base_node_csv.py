import csv
import os
import re

### parameter setting ###
# LOG file path
folder_path = "./LOG/linde_base_node"
# front part of LOG file name
file_name = "linde_r16_base_node.linde-r16.ros.log.INFO"
# saved csv file name
csv_file = file_name+".csv"
# seperate file name to get the time and date info
pattern = re.compile(r"linde_r16_base_node\.linde-r16\.ros\.log\.INFO\.(\d{8}-\d{6}\.\d+)")


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
        'date', 'time', 'Lift Fork Goal(mm)', 'Current Height(mm)', 'other info', 'action end state'
    ])

with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    save_signal = False
    save_other_data = False

    # read all saved file name
    for file in sorted_files:
        date, time, lift_fork_goal, current_height, other, end_state = "", "", "", "", "", ""

        with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    file_info, data = line.split("]")
                    value = data.split(":")
                    item = value[0].strip()
                    msg = data.split(" ")

                    if msg[1] == "Lift" and msg[2] == "Fork" and msg[3] == "Action":
                        end_state = data
                        save_signal = True
                except:
                    item = ""

                if save_signal:
                    if all([date, time, lift_fork_goal, current_height, end_state]):
                        writer.writerow([
                            date, time, lift_fork_goal, current_height, other, end_state
                        ])

                    date, time, lift_fork_goal, current_height, other, end_state = "", "", "", "", "", ""
                    save_signal = False
                    save_other_data = False

                elif save_other_data:
                    other += data

                elif item == "Lift Fork Goal":
                    date = file_info.split(" ")[0]
                    time = file_info.split(" ")[1]

                    lift_fork_goal = value[1].split(".")[0]
                    current_height = value[2].split(":")[0].split(".")[0]
                    save_other_data = True

print(f"CSV save as {csv_file}")

