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


@app.route('/upload', methods=['POST'])
def upload():
    # Save the uploaded file in the directory to uploads

    f = request.files['file']
    f.save('uploads/' + secure_filename(f.filename))

    # Open MySQL connection

    functions.mysql_create_connection()

    # Check the uploaded report

    data = functions.check_report("uploads/", secure_filename(f.filename))

    # Delete uploaded file from host

    subprocess.call(["rm", "uploads/" + secure_filename(f.filename)])

    # Close MySQL connection

    functions.mysql_close_connection()

    return json.dumps(data)


@app.route('/file_upload', methods=['POST'])
def upload_file():
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

    vbs_code = "Dim objShell\n"\
               + "Set objShell = WScript.CreateObject(\"WScript.Shell\")\n" \
               + "objShell.Run \"cmd /c copy \\\\VBOXSVR\uploads\\" + uploaded_file_name \
               + " C:\Users\\alex\Desktop\\" + uploaded_file_name + "\"\n" \
               + "WScript.Sleep 1000\n" \
               + "objShell.Run \"cmd /c start C:\Users\\alex\Desktop\\" + uploaded_file_name + "\""

    vbs_file_name = "uploads/file_" + str(random.randint(1, 100000)) + "_.vbs"
    vbs_file = open(vbs_file_name, "w")
    vbs_file.write(vbs_code)
    vbs_file.close()

    # Cuckoo running

    result = subprocess.check_output(["cuckoo", "submit", "--machine", "Cuckoo", "--timeout", "10", "--package",
                                      "vbs", vbs_file_name])
    result_pointer = result.find("ID #")
    report_id = result[result_pointer+4:len(result)-1]
    print("Task ID: " + report_id)
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

    # Open MySQL connection

    functions.mysql_create_connection()

    # Check the uploaded report

    time.sleep(2)
    file_path = "/home/alex/.cuckoo/storage/analyses/" + str(report_id) + "/reports/"
    data = functions.check_report(file_path, "report.json")

    # Close MySQL connection

    functions.mysql_close_connection()

    # Delete uploaded file from host

    # subprocess.call(["rm", vbs_file_name])
    subprocess.call(["rm", "uploads/" + uploaded_file_name])

    # Stop time

    print("Running time: " + str(time.time() - start_t))
    return json.dumps(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
