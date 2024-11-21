import tinytuya
import sys
import json

# Connect to Tuya Cloud
# c = tinytuya.Cloud()  # uses tinytuya.json 
c = tinytuya.Cloud(
        apiRegion="us", 
        apiKey="p3s3hh35mfjhdjx9u583", 
        apiSecret="51164ae1ec2c461fa44ade634c29e5bb", 
        apiDeviceID="ebec94d70e910c2ed8ivnf")

# Display list of devices
devices = c.getdevices()

# Serializing json
json_object = json.dumps(devices, indent=4)
 
# Writing to config.json
with open("tuyaDevices.json", "w") as outfile:
    outfile.write(json_object)
sys.exit()

print("Device List: %r" % devices)
# Select a Device ID to Test
id = "xxxxxxxxxxxxxxxxxxID"

# Display Properties of Device
result = c.getproperties(id)
print("Properties of device:\n", result)

# Display Status of Device
result = c.getstatus(id)
print("Status of device:\n", result)

# Send Command - Turn on switch
commands = {
    "commands": [
        {"code": "switch_1", "value": True},
        {"code": "countdown_1", "value": 0},
    ]
}
print("Sending command...")
result = c.sendcommand(id,commands)
print("Results\n:", result)