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

    # Cuckoo status
    cuckoo_status = functions.cuckoo_status()

    # Close MySQL connection
    functions.mysql_close_connection()

    return render_template('index.html', cuckoo_status=cuckoo_status)


@app.route('/admin_list')
def admin_list():
    # Open MySQL connection
    functions.mysql_create_connection()

    # Get information about program
    data = functions.length_db()
    size_db = "%.2f" % functions.size_db()
    cuckoo_status = functions.cuckoo_status()
    scans, average_scan_time = functions.statistic_change(False)
    average_scan_time = "%.2f" % average_scan_time

    # Close MySQL connection
    functions.mysql_close_connection()

    return render_template('white_list.html', data_connections_number=data[0], files_number=data[1],
                           file_actions_number=data[2], connections_number=data[3], process_number=data[4],
                           registry_actions_number=data[5], dll_number=data[6],
                           command_line_number=data[7], cuckoo_status=cuckoo_status, scans=scans,
                           average_scan_time=average_scan_time, size_db=size_db)


@app.route('/upload_process', methods=['POST'])
def upload_process():
    # Start time
    start_t = time.time()

    function_type = request.form["function_type"]
    data = ""

    if function_type == "file_check" or function_type == "file_add":
        # Check free space (No finished)
        usage_disk_space = functions.disk_space()

        if usage_disk_space < 10:
            message = [{
                "data_type":    "Message",
                "message":      "Sorry your file no scanned, no free space on the server."
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

        # Delete uploaded file from host and memory dump if exist
        subprocess.call(["rm", vbs_file_name])
        subprocess.call(["rm", "uploads/" + uploaded_file_name])
        functions.delete_memory_dump(report_id)

        # Open MySQL connection
        functions.mysql_create_connection()

        # Check/Add the uploaded report
        file_path = "/home/alex/.cuckoo/storage/analyses/" + str(report_id) + "/reports/"

        if function_type == "file_check":
            data = functions.check_report(file_path, "report.json")
            functions.statistic_change(True, time.time() - start_t)

        elif function_type == "file_add":
            functions.add_report(file_path, "report.json")
            data = [{
                "data_type":    "Message",
                "message":      "File added successfully to white-list."
            }]
            # copy report to special folder

        # Close MySQL connection
        functions.mysql_close_connection()

    elif function_type == "clear_list":
        # Open MySQL connection
        functions.mysql_create_connection()

        # Clear white-list
        functions.clear_db()

        # Close MySQL connection
        functions.mysql_close_connection()

        data = [{
            "data_type":    "Message",
            "message":      "White-list cleared out."
        }]

    elif function_type == "learn_set":
        # Open MySQL connection
        functions.mysql_create_connection()

        # Learn set
        file_path = "/home/alex/PycharmProjects/Cuckoo/white_list_set/"
        result = subprocess.check_output(["ls", file_path]).split('\n')
        result = result[0:len(result)-1]

        for file_name in result:
            functions.add_report(file_path, file_name)

        # Close MySQL connection
        functions.mysql_close_connection()

        data = [{
            "data_type":    "Message",
            "message":      "Standart set added to white-list."
        }]

    elif function_type == "statistic_reset":
        # Open MySQL connection
        functions.mysql_create_connection()

        # Learn set
        functions.statistic_reset()

        # Close MySQL connection
        functions.mysql_close_connection()

        data = [{
            "data_type":    "Message",
            "message":      "Statistical data reseted.."
        }]

    # Stop time
    print("Running time: " + str(time.time() - start_t))

    return json.dumps(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
