from flask import Flask, render_template, request
from werkzeug import secure_filename
import json
import subprocess
import time
import random
import functions

app = Flask(__name__)


@app.route('/')
def index():
    # Open MySQL connection

    functions.mysql_create_connection()

    # Get information about program

    data = functions.size_db()
    cuckoo_status = functions.cuckoo_status()

    # Close MySQL connection

    functions.mysql_close_connection()

    return render_template('index.html', data_connections_number=data[0], files_number=data[1],
                           file_actions_number=data[2], connections_number=data[3], process_number=data[4],
                           registry_actions_number=data[5], dll_number=data[6],
                           command_line_number=data[7], cuckoo_status=cuckoo_status)


@app.route('/admin_list')
def admin_list():
    # Open MySQL connection

    functions.mysql_create_connection()

    # Get information about program

    data = functions.size_db()
    cuckoo_status = functions.cuckoo_status()

    # Close MySQL connection

    functions.mysql_close_connection()

    return render_template('white_list.html', data_connections_number=data[0], files_number=data[1],
                           file_actions_number=data[2], connections_number=data[3], process_number=data[4],
                           registry_actions_number=data[5], dll_number=data[6],
                           command_line_number=data[7], cuckoo_status=cuckoo_status)


@app.route('/upload_process', methods=['POST'])
def upload_process():
    # Start time

    start_t = time.time()

    # Check free space (No finished)

    usage_disk_space = functions.disk_space()

    if usage_disk_space > 30:
        message = [{
            "data_type":    "Message",
            "message":      "No free space on the server."
        }]
        return json.dumps(message)

    # Save the uploaded file in the directory to uploads

    f = request.files["file"]
    uploaded_file_name = str(random.randint(1, 100000)) + secure_filename(f.filename)
    f.save("uploads/" + uploaded_file_name)

    # VBS file creation

    vbs_file_name = functions.create_vbs(uploaded_file_name)

    # Cuckoo submit

    result = subprocess.check_output(["cuckoo", "submit", "--machine", "Cuckoo", "--timeout", "12", "--package",
                                      "vbs", vbs_file_name])
    result_pointer = result.find("ID #")
    report_id = result[result_pointer+4:len(result)-1]
    print("Task ID: " + report_id)

    # Wait to report

    time.sleep(15)

    while 1:
        result = subprocess.check_output(["ls", "/home/alex/.cuckoo/storage/analyses"])
        report_flag = result.find(str(report_id))
        if report_flag is not -1:
            result = subprocess.check_output(["ls", "/home/alex/.cuckoo/storage/analyses/" + report_id])
            report_flag = result.find("reports")
            if report_flag is not -1:
                result = subprocess.check_output(["ls", "/home/alex/.cuckoo/storage/analyses/" + report_id + "/reports/"])
                report_flag = result.find("report.json")
                if report_flag is not -1:
                    break
        time.sleep(1)

    time.sleep(5)

    # Open MySQL connection

    functions.mysql_create_connection()

    # Check/Add the uploaded report

    file_path = "/home/alex/.cuckoo/storage/analyses/" + str(report_id) + "/reports/"

    function_type = request.form["function_type"]
    print(function_type)

    data = ""

    if function_type == "file_check":
        data = functions.check_report(file_path, "report.json")
    elif function_type == "file_add":
        functions.add_report(file_path, "report.json")
        data = [{
            "data_type":    "Message",
            "message":      "File added successfully to white-list."
        }]
        # copy report to special folder

    # Close MySQL connection

    functions.mysql_close_connection()

    # Delete uploaded file from host and memory dump if exist

    subprocess.call(["rm", "uploads/" + uploaded_file_name])
    functions.delete_memory_dump(report_id)

    # Stop time

    print("Running time: " + str(time.time() - start_t))
    return json.dumps(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
