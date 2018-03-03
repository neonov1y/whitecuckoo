# Imports

import json
import subprocess
import mysql.connector
from mysql.connector import errorcode


# Functions
# Function to open JSON file

def json_open(file_path, file_name):
    # file_path - input path to file
    # file_name - input name of JSON file to open
    # If file opened successfully function return object of opened file
    # Else error exit

    print_string = "json_open: "
    global jfile

    try:
        jfile = open(file_path + file_name)
        jdata = json.load(jfile)

        print("%-30s" % print_string + "%s" % "File " + file_name + ".json opened.")

        return jdata

    except IOError:
        error_exit(print_string + "Open of file" + file_name + ".json false.")


# Function to close JSON file

def json_close():
    # If file closed successfully function return True
    # Else error exit

    print_string = "json_close: "

    try:
        jfile.close()

        print("%-30s" % print_string + "%s" % "File closed.")

        return True

    except IOError:
        error_exit(print_string + "File closing false.")


# Function to create MySQL connection

def mysql_create_connection():
    # If database created well and cursor created successfully, function return cursor
    # and turns database object and cursor be a global
    # Else error exit

    mysql_parameters = {
        "user": "cuckoo",
        "password": "ac9100my",
        "host": "localhost",
        "database": "cuckoo",
        "raise_on_warnings": True
    }

    print_string = "mysql_create_connection: "

    try:
        global cursor
        global db

        db = mysql.connector.connect(**mysql_parameters)
        cursor = db.cursor()

        print("%-30s" % print_string + "%s" % "MySQL connection created.")

        return cursor

    except errorcode as err:
        if err.errno == err.ER_ACCESS_DENIED_ERROR:
            error_exit(print_string + "Wrong MySQL pair user name and password.")
        elif err.errno == err.ER_BAD_DB_ERROR:
            error_exit(print_string + "Database does not exist.")
        else:
            error_exit(print_string + err)


# Function to close MySQL connection

def mysql_close_connection():
    # If connection closed successfully, function return True
    # Else error exit

    print_string = "mysql_close_connection: "

    try:
        cursor.close()
        db.close()

        print("%-30s" % print_string + "%s" % "Connection closed.")

        return True

    except errorcode as err:
        error_exit(print_string + err)


# Function to exit in error case

def error_exit(error_message):
    # error_message - input message about error

    print_string = "error_exit: "

    print("%-30s" % print_string + "%s" % error_message)
    exit()


# Function to insert data to MySQL

def insert_data(data_type, data1, data2="", data3="", data4="", data5=""):
    # data_type - input variable which define type of data to insert
    # data1, data2, data3, data4, data5 - input data
    # If data inserted successfully, function return True
    # Else return False and print message about insert miss

    print_string = "insert_data: "
    data_ready_flag = False
    add_string = ""
    data = ""

    try:
        if data_type == "file":
            # data1 - name, data2 - type, data3 -size, data4 - md5, data5 - virustotal

            add_string = "INSERT INTO file (name, type, size, md5, flag_virustotal) VALUES (%s, %s, %s, %s, %s)"
            data = (data1, data2, data3, data4, data5)
            data_ready_flag = True

        elif data_type == "network_dns":
            # data1 - type, data2 - request

            add_string = "INSERT INTO network_dns (type, request) VALUES (%s, %s)"
            data = (data1, data2)
            data_ready_flag = True

        elif data_type == "network_http":
            # data1 - url, data2 - host

            add_string = "INSERT INTO network_http (url, host) VALUES (%s, %s)"
            data = (data1, data2)
            data_ready_flag = True

        elif data_type == "network_tcp":
            # data1 - source, data2 - destination

            add_string = "INSERT INTO network_tcp (source, destination) VALUES (%s, %s)"
            data = (data1, data2)
            data_ready_flag = True

        elif data_type == "network_udp":
            # data1 - source, data2 - destination

            add_string = "INSERT INTO network_udp (source, destination) VALUES (%s, %s)"
            data = (data1, data2)
            data_ready_flag = True

        elif data_type == "registry_action":
            # data1 - action_type, data2 - registry

            add_string = "INSERT INTO registry_action (action_type, registry) VALUES (%s, %s)"
            data = (data1, data2)
            data_ready_flag = True

        elif data_type == "process":
            # data1 - process_name, data2 - process_path

            add_string = "INSERT INTO process (process_name, process_path) VALUES (%s, %s)"
            data = (data1, data2)
            data_ready_flag = True

        elif data_type == "file_action":
            # data1 - action_type, data2 - full_path

            add_string = "INSERT INTO file_action (action_type, full_path) VALUES (%s, %s)"
            data = (data1, data2)
            data_ready_flag = True

        elif data_type == "folder_action":
            # data1 - action_type, data2 - full_path

            add_string = "INSERT INTO folder_action (action_type, full_path) VALUES (%s, %s)"
            data = (data1, data2)
            data_ready_flag = True

        elif data_type == "file_dropped":
            # data1 - path, data2 - type, data3 -process, data4 - size

            add_string = "INSERT INTO file_dropped (path, type, process, size) VALUES (%s, %s, %s, %s)"
            data = (data1, data2, data3, data4)
            data_ready_flag = True

        elif data_type == "connection_type":
            # data1 - data_type, data2 - file_id, data3 - data_id

            add_string = "INSERT INTO connection_type (data_type, file_id, data_id) VALUES (%s, %s, %s)"
            data = (data1, data2, data3)
            data_ready_flag = True

        else:
            print("%-30s" % print_string + "%s" % "Wrong data type.")

        if data_ready_flag:
            cursor.execute(add_string, data)
            db.commit()

            print("%-30s" % print_string + "%s" % "Data inserted.")

            return cursor.lastrowid
        else:
            return False

    except errorcode as err:
        error_exit(print_string + err)


# Function to check existence of data in MySQL

def check_data(data_type, data1, data2="", data3="", data4="", data5=""):
    # data_type - input variable which define type of data to check
    # data1, data2, data3, data4, data5 - input data
    # If data exist in database, function return id of data in database
    # Else return False
    # In case which data type is 'file', function return last id of existed data

    print_string = "check_data: "
    data_ready_flag = False
    query = ""

    try:
        if data_type == "file":
            # data1 - name, data2 - type, data3 -size, data4 - md5, data5 - virustotal
            query = "SELECT id FROM file WHERE name = '" + data1 + "' AND type = '" + data2 + \
                    "' AND size = " + str(data3) + " AND md5 = '" + data4 + "' AND flag_virustotal = " + \
                    str(data5) + " ORDER BY id DESC LIMIT 1"
            data_ready_flag = True

        elif data_type == "network_dns":
            # data1 - type, data2 - request
            query = "SELECT id FROM network_dns WHERE type = '" + data1 + "' AND request = '" + data2 + "'"
            data_ready_flag = True

        elif data_type == "network_http":
            # data1 - url, data2 - host
            query = "SELECT id FROM network_http WHERE url = '" + data1 + "' AND host = '" + data2 + "'"
            data_ready_flag = True

        elif data_type == "network_tcp":
            # data1 - source, data2 - destination
            query = "SELECT id FROM network_tcp WHERE source = '" + data1 + "' AND destination = '" + data2 + "'"
            data_ready_flag = True

        elif data_type == "network_udp":
            # data1 - source, data2 - destination
            query = "SELECT id FROM network_udp WHERE source = '" + data1 + "' AND destination = '" + data2 + "'"
            data_ready_flag = True

        elif data_type == "registry_action":
            # data1 - action_type, data2 - registry
            query = "SELECT id FROM registry_action WHERE action_type = '" + data1 + "' AND registry = '" + data2 + "'"
            data_ready_flag = True

        elif data_type == "process":
            # data1 - process_name, data2 - process_path
            query = "SELECT id FROM process WHERE process_name = '" + data1 + "' AND process_path = '" + data2 + "'"
            data_ready_flag = True

        elif data_type == "file_action":
            # data1 - action_type, data2 - full_path
            query = "SELECT id FROM file_action WHERE action_type = '" + data1 + "' AND full_path = '" + data2 + "'"
            data_ready_flag = True

        elif data_type == "folder_action":
            # data1 - action_type, data2 - full_path
            query = "SELECT id FROM folder_action WHERE action_type = '" + data1 + "' AND full_path = '" + data2 + "'"
            data_ready_flag = True

        elif data_type == "file_dropped":
            # data1 - path, data2 - type, data3 -process, data4 - size
            query = "SELECT id FROM file_dropped WHERE type = '" + data2 + \
                    "' AND process = '" + data3 + "' AND size = " + str(data4)
            data_ready_flag = True

        else:
            print("%-30s" % print_string + "%s" % "Wrong data type.")

        if data_ready_flag:
            cursor.execute(query)
            item = cursor.fetchone()

            print("%-30s" % print_string + "%s" % "Data selected.")

            try:
                return item[0]
            except TypeError:
                return False
        else:
            return False

    except errorcode as err:
        error_exit(print_string + err)


# Function to add report to database

def add_report(file_path, file_name):
    # file_path - path to file
    # file_name - name of file
    # Before function call MySQL connection must be created

    virus_flag = False
    print_string = "add_report: "
    process_name = ""

    # Open JSON file

    jdata = json_open(file_path, file_name)

    # Creating of virustotal check variable

    check_jdata = jdata["virustotal"]

    # Virustotal check

    if "scans" in check_jdata:
        for scan in jdata["virustotal"]["scans"]:
            if virus_flag is False and jdata["virustotal"]["scans"][scan]["detected"] is True:
                virus_flag = True

    # Insert file information

    file_info = {
        "name": str(jdata["target"]["file"]["name"]),
        "type": str(jdata["info"]["package"]),
        "size": str(jdata["target"]["file"]["size"]),
        "md5":  str(jdata["target"]["file"]["md5"]),
        "flag_virustotal": virus_flag * 1
    }

    file_id = insert_data("file", file_info["name"], file_info["type"],
                          file_info["size"], file_info["md5"], file_info["flag_virustotal"])

    # Insert DNS connections

    for dns in jdata["network"]["dns"]:
        dns_info = {
            "type":     str(dns["type"]),
            "request":  str(dns["request"])
        }

        data_id = check_data("network_dns", dns_info["type"], dns_info["request"])

        if data_id is False:
            data_id = insert_data("network_dns", dns_info["type"], dns_info["request"])

        insert_data("connection_type", "network_dns", file_id, data_id)

    # Insert HTTP connections

    for http in jdata["network"]["http"]:
        http_info = {
            "url":      str(http["uri"]),
            "host":     str(http["host"])
        }

        data_id = check_data("network_http", http_info["url"], http_info["host"])

        if data_id is False:
            data_id = insert_data("network_http", http_info["url"], http_info["host"])

        insert_data("connection_type", "network_http", file_id, data_id)

    # Insert TCP connections

    for tcp in jdata["network"]["tcp"]:
        tcp_info = {
            "source":       str(tcp["src"]),
            "destination":  str(tcp["dst"])
        }

        data_id = check_data("network_tcp", tcp_info["source"], tcp_info["destination"])

        if data_id is False:
            data_id = insert_data("network_tcp", tcp_info["source"], tcp_info["destination"])

        insert_data("connection_type", "network_tcp", file_id, data_id)

    # Insert UDP connections

    for udp in jdata["network"]["tcp"]:
        udp_info = {
            "source":       str(udp["src"]),
            "destination":  str(udp["dst"])
        }

        data_id = check_data("network_udp", udp_info["source"], udp_info["destination"])

        if data_id is False:
            data_id = insert_data("network_udp", udp_info["source"], udp_info["destination"])

        insert_data("connection_type", "network_udp", file_id, data_id)

    # Creating of memory check variable

    check_jdata = jdata["memory"]

    # Insert processes

    if "pslist" in check_jdata:
        for process in jdata["memory"]["pslist"]["data"]:
            process_info = {
                "process_name": str(process["process_name"])
            }

            data_id = check_data("process", process_info["process_name"])

            if data_id is False:
                data_id = insert_data("process", process_info["process_name"])

            insert_data("connection_type", "process", file_id, data_id)

    # Insert dropped files

    for file_temp in jdata["dropped"]:
        if len(file_temp["pids"]) is not 0:
            for process in jdata["behavior"]["generic"]:
                if process["pid"] == file_temp["pids"][0]:
                    process_name = process["process_name"]
                    break
        else:
            process_name = ""

        file_info = {
            "path":     str(file_temp["filepath"]),
            "type":     str(file_temp["type"]),
            "process":  process_name,
            "size":     str(file_temp["size"]),
        }

        data_id = check_data("file_dropped", file_info["path"], file_info["type"],
                             file_info["process"], file_info["size"])

        if data_id is False:
            data_id = insert_data("file_dropped", file_info["path"], file_info["type"],
                                  file_info["process"], file_info["size"])

        insert_data("connection_type", "file_dropped", file_id, data_id)

    # Creating of behavior check variable

    check_jdata = jdata["behavior"]["summary"]

    '''
    # Insert opened files

    if "file_opened" in check_jdata:
        for file_temp in jdata["behavior"]["summary"]["file_opened"]:
            file_info = {
                "action_type": "file_opened",
                "full_path": str(file_temp.replace("\\", "/"))
            }

            data_id = check_data("file_action", file_info["action_type"], file_info["full_path"])

            if data_id is False:
                data_id = insert_data("file_action", file_info["action_type"], file_info["full_path"])

            insert_data("connection_type", "file_action", file_id, data_id)

    # Insert created files
    
    for file_temp in jdata["behavior"]["summary"]["file_created"]:
        file_info = {
            "action_type": "file_created",
            "full_path": str(file_temp.replace("\\", "/"))
        }

        data_id = check_data("file_action", file_info["action_type"], file_info["full_path"])

        if data_id is False:
            data_id = insert_data("file_action", file_info["action_type"], file_info["full_path"])

        insert_data("connection_type", "file_action", file_id, data_id)

    # Insert written files
    
    if "file_written" in check_jdata:
        for file_temp in jdata["behavior"]["summary"]["file_written"]:
            file_info = {
                "action_type": "file_written",
                "full_path": str(file_temp.replace("\\", "/"))
            }

            data_id = check_data("file_action", file_info["action_type"], file_info["full_path"])

            if data_id is False:
                data_id = insert_data("file_action", file_info["action_type"], file_info["full_path"])

            insert_data("connection_type", "file_action", file_id, data_id)
    '''

    # Insert deleted files
    # Detect all files except .tmp and .TMP

    if "file_deleted" in check_jdata:
        for file_temp in jdata["behavior"]["summary"]["file_deleted"]:
            if file_temp.find(".tmp") is not -1:
                continue
            elif file_temp.find(".TMP") is not -1:
                continue

            file_info = {
                "action_type": "file_deleted",
                "full_path": str(file_temp.replace("\\", "/"))
            }

            data_id = check_data("file_action", file_info["action_type"], file_info["full_path"])

            if data_id is False:
                data_id = insert_data("file_action", file_info["action_type"], file_info["full_path"])

            insert_data("connection_type", "file_action", file_id, data_id)

    # Insert created folders

    if "directory_created" in check_jdata:
        for directory in jdata["behavior"]["summary"]["directory_created"]:
            directory_info = {
                "action_type": "directory_created",
                "full_path": str(directory.replace("\\", "/"))
            }

            data_id = check_data("folder_action", directory_info["action_type"], directory_info["full_path"])

            if data_id is False:
                data_id = insert_data("folder_action", directory_info["action_type"], directory_info["full_path"])

            insert_data("connection_type", "folder_action", file_id, data_id)

    # Insert deleted folders

    if "directory_removed" in check_jdata:
        for directory in jdata["behavior"]["summary"]["directory_removed"]:
            directory_info = {
                "action_type": "directory_removed",
                "full_path": str(directory.replace("\\", "/"))
            }

            data_id = check_data("folder_action", directory_info["action_type"], directory_info["full_path"])

            if data_id is False:
                data_id = insert_data("folder_action", directory_info["action_type"], directory_info["full_path"])

            insert_data("connection_type", "folder_action", file_id, data_id)

    # Insert written registry

    if "regkey_written" in check_jdata:
        for regkey in jdata["behavior"]["summary"]["regkey_written"]:
            regkey_info = {
                "action_type": "regkey_written",
                "full_path": str(regkey.replace("\\", "/"))
            }

            data_id = check_data("registry_action", regkey_info["action_type"], regkey_info["full_path"])

            if data_id is False:
                data_id = insert_data("registry_action", regkey_info["action_type"], regkey_info["full_path"])

            insert_data("connection_type", "registry_action", file_id, data_id)

    # Insert opened registry

    if "regkey_opened" in check_jdata:
        for regkey in jdata["behavior"]["summary"]["regkey_opened"]:
            regkey_info = {
                "action_type": "regkey_opened",
                "full_path": str(regkey.replace("\\", "/"))
            }

            data_id = check_data("registry_action", regkey_info["action_type"], regkey_info["full_path"])

            if data_id is False:
                data_id = insert_data("registry_action", regkey_info["action_type"], regkey_info["full_path"])

            insert_data("connection_type", "registry_action", file_id, data_id)

    # Insert deleted registry

    if "regkey_deleted" in check_jdata:
        for regkey in jdata["behavior"]["summary"]["regkey_deleted"]:
            regkey_info = {
                "action_type": "regkey_deleted",
                "full_path": str(regkey.replace("\\", "/"))
            }

            data_id = check_data("registry_action", regkey_info["action_type"], regkey_info["full_path"])

            if data_id is False:
                data_id = insert_data("registry_action", regkey_info["action_type"], regkey_info["full_path"])

            insert_data("connection_type", "registry_action", file_id, data_id)

    # Insert readed registry

    if "regkey_read" in check_jdata:
        for regkey in jdata["behavior"]["summary"]["regkey_read"]:
            regkey_info = {
                "action_type": "regkey_read",
                "full_path": str(regkey.replace("\\", "/"))
            }

            data_id = check_data("registry_action", regkey_info["action_type"], regkey_info["full_path"])

            if data_id is False:
                data_id = insert_data("registry_action", regkey_info["action_type"], regkey_info["full_path"])

            insert_data("connection_type", "registry_action", file_id, data_id)

    print("%-30s" % print_string + "%s" % "Report added.")

    # Close JSON file

    json_close()


# Function to process report

def check_report(file_path, file_name):
    # file_path - path to file
    # file_name - name of file
    # Before function call MySQL connection must be created
    # Function return array with new data

    virus_flag = False
    print_string = "add_report: "
    process_name = ""
    data = []

    # Open JSON file

    jdata = json_open(file_path, file_name)

    # Creating of virustotal check variable

    check_jdata = jdata["virustotal"]

    # Virustotal check

    if "scans" in check_jdata:
        for scan in jdata["virustotal"]["scans"]:
            if virus_flag is False and jdata["virustotal"]["scans"][scan]["detected"] is True:
                virus_flag = True

    # File information

    file_info = {
        "name": str(jdata["target"]["file"]["name"]),
        "type": str(jdata["info"]["package"]),
        "size": str(jdata["target"]["file"]["size"]),
        "md5":  str(jdata["target"]["file"]["md5"]),
        "flag_virustotal": virus_flag * 1
    }

    # DNS connections

    for dns in jdata["network"]["dns"]:
        dns_info = {
            "data_type":    "DNS connection",
            "type":         str(dns["type"]),
            "request":      str(dns["request"])
        }

        data_id = check_data("network_dns", dns_info["type"], dns_info["request"])

        if data_id is False:
            data.append(dns_info)

    # HTTP connections

    for http in jdata["network"]["http"]:
        http_info = {
            "data_type":    "HTTP connection",
            "url":          str(http["uri"]),
            "host":         str(http["host"])
        }

        data_id = check_data("network_http", http_info["url"], http_info["host"])

        if data_id is False:
            data.append(http_info)

    # TCP connections

    for tcp in jdata["network"]["tcp"]:
        tcp_info = {
            "data_type":    "TCP connection",
            "source":       str(tcp["src"]),
            "destination":  str(tcp["dst"])
        }

        data_id = check_data("network_tcp", tcp_info["source"], tcp_info["destination"])

        if data_id is False:
            data.append(tcp_info)

    # UDP connections

    for udp in jdata["network"]["tcp"]:
        udp_info = {
            "data_type":    "UDP connection",
            "source":       str(udp["src"]),
            "destination":  str(udp["dst"])
        }

        data_id = check_data("network_udp", udp_info["source"], udp_info["destination"])

        if data_id is False:
            data.append(udp_info)

    # Creating of memory check variable

    check_jdata = jdata["memory"]

    # Processes

    if "pslist" in check_jdata:
        for process in jdata["memory"]["pslist"]["data"]:
            process_info = {
                "data_type":    "Process",
                "process_name": str(process["process_name"])
            }

            data_id = check_data("process", process_info["process_name"])

            if data_id is False:
                data.append(process_info)

    # Dropped files

    if "dropped" in check_jdata:
        for file_temp in jdata["dropped"]:
            if len(file_temp["pids"]) is not 0:
                for process in jdata["behavior"]["generic"]:
                    if process["pid"] == file_temp["pids"][0]:
                        process_name = process["process_name"]
                        break
            else:
                process_name = ""

            file_info = {
                "data_type":    "Dropped file",
                "path":     str(file_temp["filepath"]),
                "type":     str(file_temp["type"]),
                "process":  process_name,
                "size":     str(file_temp["size"]),
            }

            data_id = check_data("file_dropped", file_info["path"], file_info["type"],
                                 file_info["process"], file_info["size"])

            if data_id is False:
                data.append(file_info)

    # Creating of behavior check variable

    check_jdata = jdata["behavior"]["summary"]

    # Deleted files
    # Detect all files except .tmp and .TMP

    if "file_deleted" in check_jdata:
        for file_temp in jdata["behavior"]["summary"]["file_deleted"]:
            if file_temp.find(".tmp") is not -1:
                continue
            elif file_temp.find(".TMP") is not -1:
                continue

            file_info = {
                "data_type":    "Deleted file",
                "action_type":  "file_deleted",
                "full_path":    str(file_temp.replace("\\", "/"))
            }

            data_id = check_data("file_action", file_info["action_type"], file_info["full_path"])

            if data_id is False:
                data.append(file_info)

    # Created folders

    if "directory_created" in check_jdata:
        for directory in jdata["behavior"]["summary"]["directory_created"]:
            directory_info = {
                "data_type":    "Created folder",
                "action_type":  "directory_created",
                "full_path":    str(directory.replace("\\", "/"))
            }

            data_id = check_data("folder_action", directory_info["action_type"], directory_info["full_path"])

            if data_id is False:
                data.append(directory_info)

    # Deleted folders

    if "directory_removed" in check_jdata:
        for directory in jdata["behavior"]["summary"]["directory_removed"]:
            directory_info = {
                "data_type":    "Deleted folder",
                "action_type":  "directory_removed",
                "full_path":    str(directory.replace("\\", "/"))
            }

            data_id = check_data("folder_action", directory_info["action_type"], directory_info["full_path"])

            if data_id is False:
                data.append(directory_info)

    # Written registry

    if "regkey_written" in check_jdata:
        for regkey in jdata["behavior"]["summary"]["regkey_written"]:
            regkey_info = {
                "data_type":    "Written registry",
                "action_type":  "regkey_written",
                "full_path":    str(regkey.replace("\\", "/"))
            }

            data_id = check_data("registry_action", regkey_info["action_type"], regkey_info["full_path"])

            if data_id is False:
                data.append(regkey_info)

    # Opened registry

    if "regkey_opened" in check_jdata:
        for regkey in jdata["behavior"]["summary"]["regkey_opened"]:
            regkey_info = {
                "data_type":    "Opened registry",
                "action_type":  "regkey_opened",
                "full_path":    str(regkey.replace("\\", "/"))
            }

            data_id = check_data("registry_action", regkey_info["action_type"], regkey_info["full_path"])

            if data_id is False:
                data.append(regkey_info)

    # Deleted registry

    if "regkey_deleted" in check_jdata:
        for regkey in jdata["behavior"]["summary"]["regkey_deleted"]:
            regkey_info = {
                "data_type":    "Deleted registry",
                "action_type":  "regkey_deleted",
                "full_path":    str(regkey.replace("\\", "/"))
            }

            data_id = check_data("registry_action", regkey_info["action_type"], regkey_info["full_path"])

            if data_id is False:
                data.append(regkey_info)

    # Readed registry

    if "regkey_read" in check_jdata:
        for regkey in jdata["behavior"]["summary"]["regkey_read"]:
            regkey_info = {
                "data_type":    "Readed registry",
                "action_type":  "regkey_read",
                "full_path":    str(regkey.replace("\\", "/"))
            }

            data_id = check_data("registry_action", regkey_info["action_type"], regkey_info["full_path"])

            if data_id is False:
                data.append(regkey_info)

    # Print new data

    for i in range(0, len(data)):
        print(data[i]["data_type"] + ": " + str(data[i]))

    # Close JSON file

    json_close()

    # Return array with new data

    return data


# Function to clear database

def clear_db():
    # Function delete all data from database

    print_string = "clear_db: "
    tables = ["connection_type", "file", "file_action", "file_dropped", "folder_action", "network_dns",
              "network_http", "network_tcp", "network_udp", "process", "registry_action"]

    for i in range(0, 11):
        add_string = "DELETE FROM " + tables[i] + "; ALTER TABLE " + tables[i] + " AUTO_INCREMENT=1;"
        cursor.execute(add_string, multi=True)
        db.commit()

    print("%-30s" % print_string + "%s" % "Data deleted.")


# Function to count database size

def size_db():
    # Function delete all data from database
    # data[0] - number of connection data
    # data[1] - number of files in database
    # data[2] - number of files actions in database
    # data[3] - number of network connections in database
    # data[4] - number of process in database
    # data[5] - number of registry actions in database

    print_string = "size_db: "
    tables = ["connection_type", "file", "file_action", "file_dropped", "folder_action", "network_dns",
              "network_http", "network_tcp", "network_udp", "process", "registry_action"]
    data = [0, 0, 0, 0, 0, 0]

    for i in range(0, 11):
        add_string = "SELECT COUNT(*) FROM " + tables[i]
        cursor.execute(add_string)
        item = cursor.fetchone()

        if i is 0:
            data[0] = item[0]
        elif i is 1:
            data[1] = item[0]
        elif i in range(2, 5):
            data[2] += item[0]
        elif i in range(5, 9):
            data[3] += item[0]
        elif i is 9:
            data[4] = item[0]
        elif i is 10:
            data[5] = item[0]

    print("%-30s" % print_string + "%s" % "Data deleted.")

    return data


# Function to check if cuckoo run

def cuckoo_status():
    result = subprocess.call(["pgrep", "cuckoo"])

    if result is not 1:
        return "Available"
    else:
        return "Stopped"
