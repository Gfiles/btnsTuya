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
from flask import Flask, render_template, request, jsonify #pip install Flask

app = Flask(__name__)

@app.route("/")
def index():
    switch_states = []
    voltages = []
    switchInfo = []
    i = 0
    for switch in switches:
        try:
            data = switch.status()
            #print(data)
            switch_state = data["dps"]["1"]
            voltage = data["dps"]["20"]
            switch_states.append(switch_state)
            voltages.append(voltage)
            switchTemp = [devices[i][0], devices[i][1], switch_state, voltage/10]
            switchInfo.append(switchTemp)
            i = i + 1
        except Exception as error:
            print("An exception occurred:", error)
        #print(switchInfo)
    return render_template("index.html", switches=switchInfo)

# Route for toggling a switch
@app.route("/toggle/<device_id>")
def toggle_switch(device_id):
    switch = switches[device_id]
    current_state = switch.status()["dps"]["1"]
    #new_state = 1 if current_state == 0 else 0
    if current_state:
        switch.turn_on()
    else:
        switch.turn_off()
    return redirect("/")

def readConfig():
    settingsFile = os.path.join(cwd, "config.json")
    if os.path.isfile(settingsFile):
        with open(settingsFile) as json_file:
            data = json.load(json_file)
    else:
        data = {
                "description_devices" : ["dev_Name", "Solution_Name", "dev_id", "address",  "local_key"],
                "devices" : [
                    ["Ekaza1", "SolutionName", "abcdefghijklmnopqrstuv", "Auto", "local_key_Pass_Code"],
                    ["Ekaza2", "SolutionName", "abcdefghijklmnopqrstuv", "192.168.0.34", "local_key_Pass_Code"]
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

switches = list()
for item in devices:
    try:
        new_device = tinytuya.OutletDevice(dev_id=item[2], address=item[3],local_key=item[4],version=3.3)
        switches.append(new_device)
    except:
        print(f"{item[0]} not found")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)
