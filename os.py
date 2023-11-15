from flask import Flask, render_template, jsonify
import psutil
import datetime
import time

app = Flask(__name__)

def categorize_processes():
    user_processes = []
    system_processes = []
    kernel_processes = []

    for process in psutil.process_iter(['pid', 'name', 'username', 'create_time']):
        try:
            process_info = process.info
            if process_info['username'] == 'ishaansharma':
                user_processes.append(process_info)
            elif process_info['username'] == 'root':
                kernel_processes.append(process_info)
            else:
                system_processes.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return user_processes, system_processes, kernel_processes

def format_create_time(create_time):
    return datetime.datetime.fromtimestamp(create_time).strftime('%Y-%m-%d %H:%M:%S')

@app.route('/')
def list_running_processes():
    return render_template('processes.html')

@app.route('/api/get_processes')
def get_processes():
    user_processes, system_processes, kernel_processes = categorize_processes()
    return jsonify({
        "user_processes": user_processes,
        "system_processes": system_processes,
        "kernel_processes": kernel_processes
    })

if __name__ == '__main__':
    app.run(port=8080, debug=True)
