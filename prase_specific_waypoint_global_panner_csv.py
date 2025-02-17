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
        'sourceID', 'targetID',
        'sourceID_x', 'sourceID_y', 'sourceID_yaw',
        'curr_x', 'curr_y', 'curr_yaw',
        'curr_error_x', 'curr_error_y', 'curr_error_xy', 'curr_error_yaw',
        'targetID_x', 'targetID_y', 'targetID_yaw',
        'end_x', 'end_y', 'end_yaw', 'error_xy', 'error_yaw'
    ])

sourceID, targetID = "", ""
sourceID_x, sourceID_y, sourceID_yaw = "", "", ""
curr_x, curr_y, curr_yaw = "", "", ""
curr_error_x, curr_error_y, curr_error_xy, curr_error_yaw = "", "", "", ""
targetID_x, targetID_y, targetID_yaw, end_x, end_y, end_yaw = "", "", "", "", "", ""
error_xy, error_yaw = "", ""

counter, amount_error_xy, amount_error_yaw, amount_curr_error_xy, amount_curr_error_yaw = 0.0, 0.0, 0.0, 0.0, 0.0
max_error_xy, max_error_yaw, max_curr_error_xy, max_curr_error_yaw = 0.0, 0.0, 0.0, 0.0
min_error_xy, min_error_yaw, min_curr_error_xy, min_curr_error_yaw = 100.0, 100.0, 100.0, 100.0

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

                        sourceID_x = row['sourceID_x']
                        sourceID_y = row['sourceID_y']
                        sourceID_yaw = row['sourceID_yaw']

                        curr_x = row['curr_x']
                        curr_y = row['curr_y']
                        curr_yaw = row['curr_yaw']
                        curr_error_x = row['curr_error_x']
                        curr_error_y = row['curr_error_y']
                        curr_error_xy = row['curr_error_xy']
                        curr_error_yaw = row['curr_error_yaw']

                        targetID_x = row['targetID_x']
                        targetID_y = row['targetID_y']
                        targetID_yaw = row['targetID_yaw']
                        end_x = row['end_x']
                        end_y = row['end_y']
                        end_yaw = row['end_yaw']
                        error_xy = row['error_xy']
                        error_yaw = row['error_yaw']


                        if float(row['curr_error_xy']) > max_error_xy:
                            max_error_xy = float(row['curr_error_xy'])

                        if abs(float(row['curr_error_yaw'])) > abs(max_error_yaw):
                            max_error_yaw = float(row['curr_error_yaw'])

                        if float(row['error_xy']) > max_curr_error_xy:
                            max_curr_error_xy = float(row['error_xy'])

                        if abs(float(row['error_yaw'])) > abs(max_curr_error_yaw):
                            max_curr_error_yaw = float(row['error_yaw'])

                        if float(row['curr_error_xy']) < min_error_xy:
                            min_error_xy = float(row['curr_error_xy'])

                        if abs(float(row['curr_error_yaw'])) < abs(min_error_yaw):
                            min_error_yaw = float(row['curr_error_yaw'])

                        if float(row['error_xy']) < min_curr_error_xy:
                            min_curr_error_xy = float(row['error_xy'])

                        if abs(float(row['error_yaw'])) < abs(min_curr_error_yaw):
                            min_curr_error_yaw = float(row['error_yaw'])

                    except:
                        pass

                    if all([sourceID, targetID,
                            sourceID_x, sourceID_y, sourceID_yaw,
                            curr_x, curr_y, curr_yaw,
                            curr_error_x, curr_error_y, curr_error_xy, curr_error_yaw,
                            targetID_x, targetID_y, targetID_yaw, end_x, end_y, end_yaw]):
                        writer.writerow([
                            sourceID, targetID,
                            sourceID_x, sourceID_y, sourceID_yaw,
                            curr_x, curr_y, curr_yaw,
                            curr_error_x, curr_error_y, curr_error_xy, curr_error_yaw,
                            targetID_x, targetID_y, targetID_yaw, end_x, end_y, end_yaw, error_xy, error_yaw
                        ])

                        try:
                            amount_error_xy += float(error_xy)
                            amount_error_yaw += float(error_yaw)
                            amount_curr_error_xy += float(curr_error_xy)
                            amount_curr_error_yaw += float(curr_error_yaw)
                            counter += 1
                        except:
                            pass

                        sourceID, targetID = "", ""
                        sourceID_x, sourceID_y, sourceID_yaw = "", "", ""
                        curr_x, curr_y, curr_yaw = "", "", ""
                        curr_error_x, curr_error_y, curr_error_xy, curr_error_yaw = "", "", "", ""
                        targetID_x, targetID_y, targetID_yaw, end_x, end_y, end_yaw = "", "", "", "", "", ""
                        error_xy, error_yaw = "", ""

            amount_error_xy /= counter
            amount_error_yaw /= counter
            amount_curr_error_xy /= counter
            amount_curr_error_yaw /= counter

            writer.writerow(["max_error_xy", max_error_xy, "max_error_yaw", max_error_yaw, "min_error_xy", min_error_xy, "min_error_yaw", min_error_yaw])
            writer.writerow(["max_curr_error_xy", max_curr_error_xy, "max_curr_error_yaw", max_curr_error_yaw, "min_curr_error_xy", min_curr_error_xy, "min_curr_error_yaw", min_curr_error_yaw])
            writer.writerow(["avg_curr_error_xy", amount_curr_error_xy, "avg_curr_error_yaw", amount_curr_error_yaw,
                             "avg_error_xy", amount_error_xy, "avg_error_yaw", amount_error_yaw, "count", counter])
            writer.writerow([])
            counter, amount_error_xy, amount_error_yaw, amount_error_xy, amount_error_yaw = 0.0, 0.0, 0.0, 0.0, 0.0
            max_error_xy, max_error_yaw, max_curr_error_xy, max_curr_error_yaw = 0.0, 0.0, 0.0, 0.0
            min_error_xy, min_error_yaw, min_curr_error_xy, min_curr_error_yaw = 100.0, 100.0, 100.0, 100.0

print(f"CSV save as {csv_file}")