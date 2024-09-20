"""_summary_
python -m tinytuya scan
https://pypi.org/project/tinytuya/
https://github.com/jasonacox/tinytuya#setup-wizard---getting-local-keys
python -m tinytuya wizard (get device id and keys)
https://pimylifeup.com/raspberry-pi-flask-web-app/
"""
import tinytuya #pip install tinytuya
import json
import os
import sys
from flask import Flask, render_template, request, redirect #pip install Flask
import tinytuya

app = Flask(__name__)

@app.route("/")
def index():
    switchInfo = []
    i = 0
    for switch in switches:
        try:
            data = c.getstatus(switch[1])
            #print(data)
            switch_state = data["result"][0]["value"]
            voltage = data["result"][5]["value"]
            switchTemp = ["YDreams", switch[0], switch_state, voltage/10, switch[1]]
            switchInfo.append(switchTemp)
            i = i + 1
        except Exception as error:
            print("An exception occurred:", error)
        #print(switchInfo)
    return render_template("Webindex.html", switches=switchInfo)

# Route for toggling a switch
@app.route("/toggle/<device_id>")
def toggle_switch(device_id):
    print(device_id)
    data = c.getstatus(device_id)
    print(data)
    current_state = data["result"][0]["value"]
    if current_state:
        commands = {
            "commands": [
                {"code": "switch_1", "value": True},
                {"code": "countdown_1", "value": 0},
                ]
        }
        
    else:
        commands = {
            "commands": [
                {"code": "switch_1", "value": False},
                {"code": "countdown_1", "value": 0},
                ]
        }
    c.sendcommand(device_id,commands)
    return redirect("/")

def readConfig():
    settingsFile = os.path.join(cwd, "config.json")
    if os.path.isfile(settingsFile):
        with open(settingsFile) as json_file:
            data = json.load(json_file)
    else:
        data = {
                "apiKey" : "your_access_id",
                "apiSecret" : "your_access_token",
                "description_devices" : ["dev_Name", "Location_Name", "dev_id", "Group",  "local_key"],
                "groups" : [
                    ["YDSw011", "GEX Salvador"],
                    ["YDSw017", "GEX Salvador"]
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
groups = config["groups"]
# Replace with your Tuya API credentials
apiKey = config["apiKey"]
apiSecret = config["apiSecret"]
#apiDeviceID = config["apiDeviceID"]

# Connect to Tuya Cloud
c = tinytuya.Cloud(
        apiRegion="us", 
        apiKey=apiKey, 
        apiSecret=apiSecret)

# Display list of devices
devices = c.getdevices()
#devices[0]
#id = devices[0]["id"]
#print(c.getstatus(id))
# Replace with the device IDs of your Tuya Switches
switches = list()
for device in devices:
    switches.append([device["name"], device["id"]])
#print(switches)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
