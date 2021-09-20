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
data = subprocess.Popen(['./adb.exe', '-s', device, 'shell', 'getevent -lt /dev/input/event2'], stdout=subprocess.PIPE)
#Pipe log output to file. Show time remaining for session, prompt to end session early.
print("***Tracking Session Started***")
while(session_time > 0):
    print("Time Remaining: " + str(session_time) + " seconds.", end="\r", flush=True)
    time.sleep(1)
    session_time -= 1
data.terminate()
#Load Data
data = data.stdout.read().decode('utf-8')
print(data)
#Process Data line-by-line using dictionary
os.chdir("C:\ATA")
csv_file = open("touch_data.csv", 'w', newline='')
csv_writer = csv.writer(csv_file)
header = ['Timestamp', 'Event Type', 'Event Semantic', 'Value']
csv_writer.writerow(header)

data = data.split("\n")
start_time = float(data[0].replace('[', "").replace(']', "").split()[0])
for i in range(len(data)):
    if len(row) < 5:
        break
    row = data[i]
    row = row.replace('[', "").replace(']', "")
    row = row.split()
    row[0] = float(row[0])-start_time
    #row = {'TS':float(row[0])-start_time, 'ET':row[1], 'ES':row[2], 'VAL':row[3]}
    data[i] = row
    csv_writer.writerow(row)
#Format Data in CSV Format.
csv_file.close()
print()
#Save Data to Drive

#Upload to One-Drive Account.

#Profit.

