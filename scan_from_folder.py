# Imports

from os import listdir
import subprocess
import time
import functions
from werkzeug import secure_filename

# Variables

FILES_FOLDER = "/home/alex/PycharmProjects/Cuckoo/scan_folder/"
REPORTS_FOLDER = "/home/alex/PycharmProjects/Cuckoo/scan_reports/"
FILES_NAME_ADDITION = "_doc_pdf_mix"
MEMORY_DUMP = False


def scan(path, memory_dump_statment=False):
    # Check cuckoo status
    cuckoo_status = functions.cuckoo_status()

    if cuckoo_status is False:
        print("Cuckoo Sandbox is off, to scan files you must turn on Cuckoo.")
        return False

    files = listdir(path)

    for f in range(0, len(files)):
        secure_file_name = secure_filename(files[f])
        if files[f] != secure_file_name:
            subprocess.check_output(["mv", path + files[f], path + secure_file_name])

    files = listdir(path)

    for f in range(0, len(files)):
        # Check free space
        usage_disk_space = functions.disk_space()

        if usage_disk_space < 5:
            print("Free space in the disk is under 5GB.")
            return False

        if memory_dump_statment is True:
            result = subprocess.check_output(["cuckoo", "submit", "--machine", functions.CONF_CUCKOO_VM, "--timeout",
                                              functions.CONF_CUCKOO_SCAN_TIME, "--memory", path + files[f]])
        else:
            result = subprocess.check_output(["cuckoo", "submit", "--machine", functions.CONF_CUCKOO_VM, "--timeout",
                                              functions.CONF_CUCKOO_SCAN_TIME, path + files[f]])

        result_pointer = result.find("ID #")
        report_id = result[result_pointer+4:len(result)-1]
        print("Task ID: " + report_id)

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

        # Add report to MySQL
        file_path = functions.PATH_ANALYSES + str(report_id) + "/reports/"

        db, cursor = functions.mysql_create_connection()
        functions.add_report(db, cursor, file_path, "report.json")
        functions.mysql_close_connection(db, cursor)

        subprocess.check_output(["cp", file_path + "report.json", REPORTS_FOLDER + str(f) + "_report." +
                                 FILES_NAME_ADDITION + "json"])
        subprocess.call(["rm", file_path + "report.json"])


if __name__ == '__main__':
    scan(FILES_FOLDER, MEMORY_DUMP)
