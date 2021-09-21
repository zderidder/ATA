#Import Libraries
import subprocess, os, time, csv
#Display Launch Prompt
print("Welcome to ATA (Android Touch Acquisition)")
print()
os.chdir("C:\Android\platform-tools")
#Retrieve List of Devices
devices = subprocess.run(['./adb.exe', 'devices'], stdout=subprocess.PIPE)
devices = devices.stdout.decode('utf-8').strip()
devices = devices.replace("\tdevice", "")
devices = devices.split("\r\n")[1:]
#Prompt User to Select Device
print("Select a Device: ")
for i in range(len(devices)):
    print(str(i+1) + ") " + devices[i])

device = int(input("Enter Choice: "))
device = devices[device-1]
print("Selected Device: "+ device)
#Prompt User to Specify Session Length
session_time = int(input("Specify Session Length (min): "))
#Prompt User for Application to launch

#Start Tracking Session
os.chdir("C:\ATA")
log_file = open("raw_data", "w")
os.chdir("C:\Android\platform-tools")
data = subprocess.Popen(['./adb.exe', '-s', device, 'shell', 'getevent -lt /dev/input/event2'], stdout=log_file)
#Pipe log output to file. Show time remaining for session, prompt to end session early.
print("***Tracking Session Started***")
while(session_time > 0):
    print("Time Remaining: " + str(session_time) + " seconds.", end="\r", flush=True)
    time.sleep(1)
    session_time -= 1
data.terminate()
#Load Data
log_file.close()
os.chdir("C:\ATA")
log_file = open("raw_data", "r")
data = log_file.readlines()

csv_file = open("touch_data.csv", 'w', newline='')
csv_writer = csv.writer(csv_file)
header = ['Timestamp', 'X', 'Y', 'BTN_TOUCH']
csv_writer.writerow(header)


start_time = float(data[0].replace('[', "").replace(']', "").replace("\n", "").strip().split()[0])
for i in range(len(data)):
    row = data[i]
    if len(row) < 5:
        break
    row = row.replace('[', "").replace(']', "").replace("\n", "").strip()
    row = row.split()
    row[0] = float(row[0])-start_time
    data[i] = row

lastEventid = 0
events = list()
# template_row = ['','','']
for i in range(len(data)):
    row = data[i]
    if row[1] == "EV_SYN":
        output_row = [row[0], -420, -420, ""] #Adding Timestamp of Event
        while lastEventid <= i:
            inner_row = data[lastEventid]
            if inner_row[2] == "ABS_MT_POSITION_X" :
                output_row[1]=int(inner_row[3], 16)
            if inner_row[2] == "ABS_MT_POSITION_Y" :
                output_row[2]=(int(inner_row[3], 16))
            if inner_row[2] == "BTN_TOUCH":
                output_row[3]=(inner_row[3])
            lastEventid += 1
        if len(events) > 0:
            if output_row[1] == -420:
                output_row[1] = events[-1][1] #get the last event's X coordinate 
            if output_row[2] == -420:
                output_row[2] = events[-1][2] #get the last event's Y coordinate
            if output_row[3] == "":
                output_row[3] = "HELD" #get the last event's Y coordinate           
        events.append(output_row)
        csv_writer.writerow(output_row)

csv_file.close()
print()
#Save Data to Drive

#Upload to One-Drive Account.

#Profit.

