# Imports

from flask import Flask, render_template, request
from werkzeug import secure_filename
import json
import subprocess
import time
import random
import functions

# Variables

print_string = "server: "

# Server

app = Flask(__name__)


@app.route('/')
def index():
    # print(request.environ['REMOTE_ADDR'])
    cuckoo_status = functions.cuckoo_status()

    return render_template('index.html', cuckoo_status=cuckoo_status)


@app.route('/admin_list')
def admin_list():
    db, cursor = functions.mysql_create_connection()

    # Get information about program
    data = functions.length_db(cursor)
    size_db = "%.2f" % functions.size_db(cursor)
    cuckoo_status = functions.cuckoo_status()
    scans, average_scan_time = functions.statistic_data(db, cursor, False)
    average_scan_time = "%.2f" % average_scan_time

    functions.mysql_close_connection(db, cursor)

    return render_template('white_list.html', data_connections_number=data[0], files_number=data[1],
                           file_actions_number=data[2], connections_number=data[3], process_number=data[4],
                           registry_actions_number=data[5], dll_number=data[6],
                           command_line_number=data[7], cuckoo_status=cuckoo_status, scans=scans,
                           average_scan_time=average_scan_time, size_db=size_db)


@app.route('/upload_process', methods=['POST'])
def upload_process():
    # Start time
    start_t = time.time()

    function_type = secure_filename(request.form["function_type"])
    data = ""

    if function_type == "file_check" or function_type == "file_add":
        # Check free space
        usage_disk_space = functions.disk_space()

        if usage_disk_space < 5:
            message = [{
                "data_type":    "Message",
                "message":      "Sorry your file no scanned, no free space on the server."
            }]
            return json.dumps(message)

        # Save the uploaded file in the directory to uploads
        f = request.files["file"]
        uploaded_file_name = str(random.randint(1, 100000)) + "_" + secure_filename(f.filename)
        f.save(functions.PATH_UPLOADS + uploaded_file_name)

        # Run Cuckoo
        memory_dump_statment = secure_filename(request.form["memory_dump"])
        if memory_dump_statment == "true":
            result = subprocess.check_output(["cuckoo", "submit", "--machine", functions.CONF_CUCKOO_VM, "--timeout",
                                              functions.CONF_CUCKOO_SCAN_TIME, "--memory", functions.PATH_UPLOADS +
                                              uploaded_file_name])
        elif memory_dump_statment == "false":
            result = subprocess.check_output(["cuckoo", "submit", "--machine", functions.CONF_CUCKOO_VM, "--timeout",
                                              functions.CONF_CUCKOO_SCAN_TIME, functions.PATH_UPLOADS +
                                              uploaded_file_name])

        result_pointer = result.find("ID #")
        report_id = result[result_pointer+4:len(result)-1]
        print("%-30s" % print_string + "Task ID: " + report_id)

        # Wait to report
        time.sleep(15)

        while 1:
            result = subprocess.check_output(["ls", functions.PATH_ANALYSES])
            report_flag = result.find(str(report_id))
            if report_flag is not -1:
                result = subprocess.check_output(["ls", functions.PATH_ANALYSES + report_id])
                report_flag = result.find("reports")
                if report_flag is not -1:
                    result = subprocess.check_output(["ls", functions.PATH_ANALYSES + report_id + "/reports/"])
                    report_flag = result.find("report.json")
                    if report_flag is not -1:
                        break
            time.sleep(1)

        time.sleep(5)

        # Delete uploaded file from host and memory dump if exist
        subprocess.call(["rm", functions.PATH_UPLOADS + uploaded_file_name])
        functions.delete_memory_dump(report_id)

        # Open MySQL connection
        db, cursor = functions.mysql_create_connection()

        # Check/Add the uploaded report
        file_path = functions.PATH_ANALYSES + str(report_id) + "/reports/"

        if function_type == "file_check":
            data = functions.check_report(cursor, file_path, "report.json")
            functions.statistic_data(db, cursor, True, time.time() - start_t)

        elif function_type == "file_add":
            functions.add_report(db, cursor, file_path, "report.json")
            data = [{
                "data_type":    "Message",
                "message":      "File added successfully to white-list."
            }]
            # copy report to special folder

        functions.mysql_close_connection(db, cursor)

    elif function_type == "clear_list":
        db, cursor = functions.mysql_create_connection()
        functions.clear_db(db, cursor)
        functions.mysql_close_connection(db, cursor)

        data = [{
            "data_type":    "Message",
            "message":      "White-list cleared out."
        }]

    elif function_type == "learn_set":
        db, cursor = functions.mysql_create_connection()
        functions.learn_set(db, cursor, functions.PATH_STANDART_SET)
        functions.mysql_close_connection(db, cursor)

        data = [{
            "data_type":    "Message",
            "message":      "Standart set added to white-list."
        }]

    elif function_type == "statistic_reset":
        db, cursor = functions.mysql_create_connection()
        functions.statistic_reset(db, cursor)
        functions.mysql_close_connection(db, cursor)

        data = [{
            "data_type":    "Message",
            "message":      "Statistical data reseted."
        }]

    # Stop time
    print("%-30s" % print_string + "Running time: " + str(time.time() - start_t))

    return json.dumps(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
