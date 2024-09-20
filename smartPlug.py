"""
python -m tinytuya scan
https://pypi.org/project/tinytuya/
https://github.com/jasonacox/tinytuya#setup-wizard---getting-local-keys
python -m tinytuya wizard to get device id and keys
"""
# Example Usage of TinyTuya
import tinytuya
import json
import os
import sys

def readConfig():
    settingsFile = os.path.join(cwd, "config.json")
    if os.path.isfile(settingsFile):
        with open(settingsFile) as json_file:
            data = json.load(json_file)
    else:
        data = {
                "description_devices" : ["dev_Name", "dev_id", "address",  "local_key"],
                "devices" : [
                    ["YDSw001", "ebbcc8dc8756d2a98c6rqx", "Auto", "$Cg+n+7!<F2?#@bM"],
                    ["YDSw002", "ebcd7d812e28ddf646oupo", "Auto", "?3*Z>^bt+/5sr#I+"]
                ]
        }
        # Serializing json
        json_object = json.dumps(data, indent=4)
 
        # Writing to config.json
        with open(settingsFile, "w") as outfile:
            outfile.write(json_object)
    return data

# Get the current working 
# directory (CWD)
try:
    this_file = __file__
except NameError:
    this_file = sys.argv[0]
this_file = os.path.abspath(this_file)
if getattr(sys, 'frozen', False):
    cwd = os.path.dirname(sys.executable)
else:
    cwd = os.path.dirname(this_file)
    
#print("Current working directory:", cwd)

# Read Config File
config = readConfig()
devices = config["devices"]

switch = list()
for item in devices:
    switch.append(tinytuya.OutletDevice(dev_id=item[1], address=item[2],local_key=item[3],version=3.3))

for i in range(len(devices)):
    print(f"device {devices[i][0]} result: {switch[i].status()}")
    
if len(sys.argv) == 1:
    print(f"Possible comands are: (On|Off) [deviceNumber]")
else:
    command = sys.argv[1]
    if len(sys.argv) == 3:
        deviceNum = int(sys.argv[2])
        if command == "On":
            switch[deviceNum].turn_on()
        if command == "Off":
            switch[deviceNum].turn_off()
    else:
        for device in switch:
            if command == "On":
                device.turn_on()
            if command == "Off":
                device.turn_off()            

# Connect to Device

"""
d = tinytuya.OutletDevice(
    dev_id='ebcd7d812e28ddf646oupo',
    address='Auto',      # Or set to 'Auto' to auto-discover IP address
    local_key='?3*Z>^bt+/5sr#I+', 
    version=3.3)

# Get Status
data = d.status() 
print('set_status() result %r' % data)

# Turn On
d.turn_on()

# Turn Off
d.turn_off()
"""