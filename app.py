import subprocess
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute_batch', methods=['POST'])
def execute_batch():
    button_value = request.form['button_value']
    batch_file = f"batch_{button_value}.cmd"  # Adjust batch file name as needed
    try:
        result = subprocess.run(batch_file, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return "Batch file executed successfully."
        else:
            return f"Error executing batch file: {result.stderr}"
    except FileNotFoundError:
        return "Batch file not found."

if __name__ == '__main__':
    app.run(debug=True)