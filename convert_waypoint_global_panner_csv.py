import csv
import os
import re

### parameter setting ###
# LOG file path
folder_path = "./LOG/R16_waaypoint_global_panner_Log"
# front part of LOG file name
file_name = "WaypointGlobalPlanner.linde-r16.ros.log.INFO"
# saved csv file name
csv_file = file_name+".csv"
# seperate file name to get the time and date info
pattern = re.compile(r"WaypointGlobalPlanner\.linde-r16\.ros\.log\.INFO\.(\d{8}-\d{6}\.\d+)")


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
        'date', 'time', 'sourceID',
        'targetID', 'targetID_x', 'targetID_y', 'targetID_yaw',
        'end_x', 'end_y', 'end_yaw',
        'error_xy', 'error_yaw', 'action_state'
    ])

with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    start_signal = False
    end_signal = False

    # read all saved file name
    for file in sorted_files:

        date, time = "", ""
        sourceID, sourceID_x, sourceID_y, sourceID_yaw = "", "", "", ""
        targetID, targetID_x, targetID_y, targetID_yaw = "", "", "", ""
        end_x, end_y, end_yaw = "", "", ""
        error_xy, error_yaw, action_state = "", "", ""

        with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as f:
            for line in f:

                try:
                    info = line.split("]")
                    state = info[1].split("*")[1].strip()

                    if state == '0':
                        date = info[0].split(" ")[0]
                        time = info[0].split(" ")[1]
                        start_signal = True
                except Exception as e:
                    print("Error: ", e)

                if start_signal:
                    try:
                        if state == '1.1':
                            sourceID = line.split("Source ID : ")[1].split("pose")[0].strip()

                            sourceID_x   = line.split(" x [")[1].split("]")[0].strip()
                            sourceID_y   = line.split(" y [")[1].split("]")[0].strip()
                            sourceID_yaw = line.split(" yaw [")[1].split("degree")[0].strip()

                        if state == '1.2':
                            targetID = line.split("Target ID : ")[1].split("pose")[0].strip()

                            targetID_x   = line.split(" x [")[1].split("]")[0].strip()
                            targetID_y   = line.split(" y [")[1].split("]")[0].strip()
                            targetID_yaw = line.split(" yaw [")[1].split("degree")[0].strip()


                        if state == '17':
                            error_xy = line.split("--->")[2].split("m")[0].strip()
                            error_yaw = line.split("---> ")[2].split("m")[1].split("degrees")[0].strip()

                        if state == '17.1':
                            end = line.split("stop at [")[1].split(",")

                            end_x   = end[0].strip()
                            end_y   = end[1].strip()
                            end_yaw = end[2].split("]")[0].strip()

                        if state == '18':
                            action_state = line.split(targetID)[1]
                            end_signal = True

                    except Exception as e:
                        print("Error: ", e)

                if end_signal:
                    if all([date, time]):
                        writer.writerow([
                            date, time, sourceID,
                            targetID, targetID_x, targetID_y, targetID_yaw,
                            end_x, end_y, end_yaw,
                            error_xy, error_yaw, action_state
                        ])

                    date, time = "", ""
                    sourceID, sourceID_x, sourceID_y, sourceID_yaw = "", "", "", ""
                    targetID, targetID_x, targetID_y, targetID_yaw = "", "", "", ""
                    end_x, end_y, end_yaw = "", "", ""
                    error_xy, error_yaw, action_state = "", "", ""

                    start_signal = False
                    end_signal = False

print(f"CSV save as {csv_file}")