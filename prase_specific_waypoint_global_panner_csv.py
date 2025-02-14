import csv


### parameter setting ###
# read csv file name
read_file = "WaypointGlobalPlanner.linde-r16.ros.log.INFO.csv"
# saved csv file name
csv_file = "prase_" + read_file.split(".")[0].strip() + ".csv"



### select all target ID ###
column_name = "targetID"

targetID_value = set()
with open(read_file, newline='', encoding='utf-8') as f:
    # read csv and convert to dict
    reader = csv.DictReader(f)
    for row in reader:
        targetID_value.add(row[column_name])
# convert to list
targetID_list = list(targetID_value)

### create csv and write tile ###
with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        'sourceID', 'targetID', 'targetID_x', 'targetID_y', 'targetID_yaw', 'end_x', 'end_y', 'end_yaw', 'error_xy', 'error_yaw'
    ])


sourceID, targetID, targetID_x, targetID_y, targetID_yaw, end_x, end_y, end_yaw = "", "", "", "", "", "", "", ""
error_xy, error_yaw = "", ""

counter, amount_error_xy, amount_error_yaw = 0.0, 0.0, 0.0


with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    ### detect and prase date ###
    for file in targetID_list:
        # detect all target ID and save corresponding data
        with open(read_file, newline='', encoding='utf-8') as f:
            # read csv and convert to dict
            reader = csv.DictReader(f)
            for row in reader:
                if (file == row[column_name]):

                    try:
                        sourceID = row['sourceID']
                        targetID = row['targetID']
                        targetID_x = row['targetID_x']
                        targetID_y = row['targetID_y']
                        targetID_yaw = row['targetID_yaw']
                        end_x = row['end_x']
                        end_y = row['end_y']
                        end_yaw = row['end_yaw']
                        error_xy = row['error_xy']
                        error_yaw = row['error_yaw']
                    except:
                        pass

                    if all([sourceID, targetID, targetID_x, targetID_y, targetID_yaw, end_x, end_y, end_yaw]):
                        writer.writerow([
                            sourceID, targetID, targetID_x, targetID_y, targetID_yaw, end_x, end_y, end_yaw, error_xy, error_yaw
                        ])

                        try:
                            amount_error_xy += float(error_xy)
                            amount_error_yaw += float(error_yaw)
                            counter += 1
                        except:
                            pass

                        sourceID, targetID, targetID_x, targetID_y, targetID_yaw, end_x, end_y, end_yaw = "", "", "", "", "", "", "", ""
                        error_xy, error_yaw = "", ""


            amount_error_xy /= counter
            amount_error_yaw /= counter

            writer.writerow(["avg_error_xy", amount_error_xy, "avg_error_yaw", amount_error_yaw, "count", counter])
            writer.writerow([])
            counter, amount_error_xy, amount_error_yaw = 0.0, 0.0, 0.0

print(f"CSV save as {csv_file}")