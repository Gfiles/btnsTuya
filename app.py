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
from flask import Flask, render_template, request, jsonify, redirect#pip install Flask
from waitress import serve

app = Flask(__name__)

@app.route("/")
def index():
    switchInfo = []
    i = 0
    for switch in switches:
        try:
            if switch == None:
                switchInfo.append([devices[i]["name"], devices[i]["solutionName"], "offline", 0])             
            else:
                try:
                    data = switch.status()
                    #print(data)
                    switch_state = data["dps"]["1"]
                    try:
                        voltage = data["dps"]["20"]/10
                    except:
                        voltage = 0
                    switchTemp = [devices[i]["name"], devices[i]["solutionName"], switch_state, voltage]
                    switchInfo.append(switchTemp)
                except:
                    [devices[i]["name"], devices[i]["solutionName"], "offline", 0]
            i = i + 1
        except Exception as error:
            print("An exception occurred:", error)
        #print(switchInfo)
    return render_template("index.html", switches=switchInfo, title=title)

# Route for toggling a switch
@app.route("/toggle/<device_id>")
def toggle_switch(device_id):
    i = int(device_id) - 1
    current_state = switches[i].status()["dps"]["1"]
    #new_state = 1 if current_state == 0 else 0
    if current_state:
        switches[i].turn_off()
    else:
        switches[i].turn_on()
    return redirect("/")

def readConfig(settingsFile):
    if os.path.isfile(settingsFile):
        with open(settingsFile) as json_file:
            data = json.load(json_file)
    else:
        data = {
                "title" : "Title",
                "devices" : [
                    {"name": "YDSw010", "solutionName" : "solutionName"},
                    {"name": "YDSw011", "solutionName" : "solutionName"},
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
#Scan for local Tuya DEvices
tinytuya.scan()

# Read Config File
settingsFile = os.path.join(cwd, "config.json")
config = readConfig(settingsFile)
settingsDevices = config["devices"]
title = config["title"]

tuyaDevices = readConfig(os.path.join(cwd, "snapshot.json"))
localDevices = tuyaDevices["devices"]
devices = list()
for device in localDevices:
    if device["ip"] != "":
        j = dict()
        j.update({"name" : device["name"]})
        j.update({"ip" : device["ip"]})
        j.update({"id" : device["id"]})
        j.update({"key" : device["key"]})
        j.update({"solutionName" : device["name"]})
        for solutionName in settingsDevices:
            if device["name"] == solutionName["name"]:
                j.update({"solutionName" : solutionName["solutionName"]})
                break
        devices.append(j)
#print(devices)

switches = list()
for item in devices:
    try:
        new_device = tinytuya.OutletDevice(dev_id=item["id"], address=item["ip"], local_key=item["key"], version=3.4)
        switches.append(new_device)
    except:
        print(f"{item[0]} not found")
        switches.append(None)

if __name__ == '__main__':
    print("Server Running on http://localhost")
    #app.run(debug=True, host='0.0.0.0', port=80)
    serve(app, host="0.0.0.0", port=80)
