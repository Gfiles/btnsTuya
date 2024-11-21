import tinytuya # https://github.com/jasonacox/tinytuya
import json
import os
import sys
from flask import Flask, render_template, request, jsonify #pip install Flask

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute_batch', methods=['POST'])
def execute_batch():
    #button_value = request.form['button_value']
    #batch_file = f"batch_{button_value}.cmd"  # Adjust batch file name as needed
    btnNum = int(request.form.get('btnNum'))
    btnState = request.form.get('btnState')
    print(f"{btnState} {btnNum}")
    
    if btnState == "On":
        switch[btnNum-1].turn_on()
    if btnState == "Off":
        switch[btnNum-1].turn_off()
    """
    batch_file = "batch_on.cmd"  # Replace with your batch file name
    try:
        result = subprocess.run(batch_file, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return "Batch file executed successfully."
        else:
            return f"Error executing batch file: {result.stderr}"
    except FileNotFoundError:
        return "Batch file not found."
    """
    return "Batch file executed successfully."

@app.route('/get_state')
def get_state():
    state = ["On", "Off"]  # Replace with your actual state logic
    return jsonify({'state': state})

def readConfig():
    settingsFile = os.path.join(cwd, "config.json")
    if os.path.isfile(settingsFile):
        with open(settingsFile) as json_file:
            data = json.load(json_file)
    else:
        data = {
                "description_devices" : ["dev_Name", "dev_id", "address",  "local_key"],
                "devices" : [
                    ["Ekaza1", "abcdefghijklmnopqrstuv", "Auto", "local_key_Pass_Code"],
                    ["Ekaza2", "abcdefghijklmnopqrstuv", "192.168.0.34", "local_key_Pass_Code"]
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
    try:
        switch.append(tinytuya.OutletDevice(dev_id=item[1], address=item[2],local_key=item[3],version=3.3))
    except:
        print(f"{item[0] not found}")
#for i in range(len(devices)):
    #print(f"device {devices[i][0]} result: {switch[i].status()}")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')