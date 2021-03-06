# Imports

import json
import subprocess
import mysql.connector
from mysql.connector import errorcode
import os

# Dependences
# Linux tool "pgrep" in function cuckoo_status()

# Constants

MYSQL_USER = "cuckoo"
MYSQL_PASSWORD = "ac9100my"
MYSQL_HOST = "localhost"
MYSQL_DATABASE = "cuckoo"
MYSQL_TABLES = ("connection_type", "file", "file_action", "file_dropped", "folder_action", "network_dns",
                "network_http", "network_tcp", "network_udp", "process", "registry_action", "dll", "command_line")
PATH_ANALYSES = "/home/alex/.cuckoo/storage/analyses/"
PATH_STANDART_SET = "/home/alex/PycharmProjects/Cuckoo/white_list_set/"
PATH_UPLOADS = "/home/alex/PycharmProjects/Cuckoo/uploads/"
CONF_CUCKOO_VM = "Cuckoo"
CONF_CUCKOO_SCAN_TIME = "12"
PRINT_FLAG = False
CONNECTION_TABLE_FLAG = False


# Functions
# Function to open JSON file

def json_open(file_path, file_name):
    """ file_path - input path to file
        file_name - input name of JSON file to open
        If file opened successfully function return object of opened file
        Else error exit
    """

    print_string = "json_open: "
    global jfile

    try:
        jfile = open(file_path + file_name)
        jdata = json.load(jfile)

        print("%-30s" % print_string + "%s" % "File " + file_name + " opened.")

        return jdata

    except IOError:
        error_exit(print_string + "Open of file" + file_name + " false.")


# Function to close JSON file

def json_close():
    """ If file closed successfully function return True
        Else error exit
    """

    print_string = "json_close: "

    try:
        jfile.close()

        print("%-30s" % print_string + "%s" % "File closed.")

        return True

    except IOError:
        error_exit(print_string + "File closing false.")


# Function to create MySQL connection

def mysql_create_connection():
    """ If database created well and cursor created successfully, function return cursor
        and turns database object and cursor be a global
        Else error exit
    """

    mysql_parameters = {
        "user":     MYSQL_USER,
        "password": MYSQL_PASSWORD,
        "host":     MYSQL_HOST,
        "database": MYSQL_DATABASE,
        "raise_on_warnings": True
    }

    print_string = "mysql_create_connection: "

    try:
        db = mysql.connector.connect(**mysql_parameters)
        cursor = db.cursor()

        print("%-30s" % print_string + "%s" % "MySQL connection created.")

        return db, cursor

    except errorcode as err:
        if err.errno == err.ER_ACCESS_DENIED_ERROR:
            error_exit(print_string + "Wrong MySQL pair user name and password.")
        elif err.errno == err.ER_BAD_DB_ERROR:
            error_exit(print_string + "Database does not exist.")
        else:
            error_exit(print_string + err)


# Function to close MySQL connection

def mysql_close_connection(db, cursor):
    """ If connection closed successfully, function return True
        Else error exit
    """

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
    """ error_message - input message about error """

    print_string = "error_exit: "

    print("%-30s" % print_string + "%s" % error_message)
    exit()


# Function to insert data to MySQL

def insert_data(db, cursor, data_type, data1, data2="", data3="", data4="", data5=""):
    """ data_type - input variable which define type of data to insert
        data1, data2, data3, data4, data5 - input data
        If data inserted successfully, function return True
        Else return False and print message about insert miss
    """

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

        elif data_type == "dll":
            # data1 - full_path

            add_string = "INSERT INTO dll SET full_path='" + data1 + "'"
            data_ready_flag = True

        elif data_type == "command_line":
            # data1 - command

            add_string = "INSERT INTO command_line SET command='" + data1 + "'"
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

            if PRINT_FLAG is True:
                print("%-30s" % print_string + "%s" % "Data inserted.")

            return cursor.lastrowid
        else:
            return False

    except errorcode as err:
        error_exit(print_string + err)


# Function to check existence of data in MySQL

def check_data(cursor, data_type, data1, data2="", data3="", data4="", data5=""):
    """ data_type - input variable which define type of data to check
        data1, data2, data3, data4, data5 - input data
        If data exist in database, function return id of data in database
        Else return False
        In case which data type is 'file', function return last id of existed data
    """

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

        elif data_type == "dll":
            # data1 - full_path
            query = "SELECT id FROM dll WHERE full_path = '" + data1 + "'"
            data_ready_flag = True

        elif data_type == "command_line":
            # data1 - command
            query = "SELECT id FROM command_line WHERE command = '" + data1 + "'"
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
            data_id = cursor.fetchone()

            # print("%-30s" % print_string + "%s" % "Data selected." + str(type(item[0])))

            if data_id is None:
                if PRINT_FLAG is True:
                    print("%-30s" % print_string + "%s" % "Data checked." + " Data no exist.")
                return False
            else:
                if PRINT_FLAG is True:
                    print("%-30s" % print_string + "%s" % "Data checked." + " ID: " + str(data_id[0]) + " (" +
                          data_type + ")")
                return data_id[0]
        else:
            return False

    except errorcode as err:
        error_exit(print_string + err)


# Function to add report to database

def add_report(db, cursor, file_path, file_name):
    """ file_path - path to file
        file_name - name of file
        Before function call MySQL connection must be created
    """

    virus_flag = False
    print_string = "add_report: "

    # Open JSON file

    jdata = json_open(file_path, file_name)

    # Creating of virustotal check variable

    check_jdata = ""
    if "virustotal" in jdata:
        check_jdata = jdata["virustotal"]

    # Virustotal check

    if "scans" in check_jdata:
        for scan in jdata["virustotal"]["scans"]:
            if "detected" in scan:
                if virus_flag is False and jdata["virustotal"]["scans"][scan]["detected"] is True:
                    virus_flag = True

    # Insert file information

    if "target" in jdata:
        if "file" in jdata["target"]:
            if "name" in jdata["target"]["file"] and "size" in jdata["target"]["file"] and "md5" in\
                    jdata["target"]["file"] and "type" in jdata["target"]["file"]:
                file_info = {
                    "name": str(jdata["target"]["file"]["name"].encode("utf-8")),
                    "type": str(jdata["target"]["file"]["type"].encode("utf-8")),
                    "size": str(jdata["target"]["file"]["size"]),
                    "md5":  str(jdata["target"]["file"]["md5"].encode("utf-8")),
                    "flag_virustotal": virus_flag * 1
                }

                file_id = insert_data(db, cursor, "file", file_info["name"], file_info["type"],
                                      file_info["size"], file_info["md5"], file_info["flag_virustotal"])
            else:
                json_close()
                return
        else:
            json_close()
            return
    else:
        json_close()
        return

    # Creating of network check variable

    check_jdata = ""
    if "network" in jdata:
        check_jdata = jdata["network"]

    # Insert DNS connections

    if "dns" in check_jdata:
        for dns in jdata["network"]["dns"]:
            if "type" in dns and "request" in dns:
                dns_info = {
                    "type":     str(dns["type"].encode("utf-8")),
                    "request":  str(dns["request"].encode("utf-8"))
                }

                data_id = check_data(cursor, "network_dns", dns_info["type"], dns_info["request"])

                if data_id is False:
                    data_id = insert_data(db, cursor, "network_dns", dns_info["type"], dns_info["request"])

                if CONNECTION_TABLE_FLAG is True:
                    insert_data(db, cursor, "connection_type", "network_dns", file_id, data_id)

    # Insert HTTP connections

    if "http" in check_jdata:
        for http in jdata["network"]["http"]:
            if "uri" in http and "host" in http:
                http_info = {
                    "url":      str(http["uri"].encode("utf-8")),
                    "host":     str(http["host"].encode("utf-8"))
                }

                data_id = check_data(cursor, "network_http", http_info["url"], http_info["host"])

                if data_id is False:
                    data_id = insert_data(db, cursor, "network_http", http_info["url"], http_info["host"])

                if CONNECTION_TABLE_FLAG is True:
                    insert_data(db, cursor, "connection_type", "network_http", file_id, data_id)

    # Insert TCP connections

    if "tcp" in check_jdata:
        for tcp in jdata["network"]["tcp"]:
            if "src" in tcp and "dst" in tcp:
                tcp_info = {
                    "source":       str(tcp["src"].encode("utf-8")),
                    "destination":  str(tcp["dst"].encode("utf-8"))
                }

                data_id = check_data(cursor, "network_tcp", tcp_info["source"], tcp_info["destination"])

                if data_id is False:
                    data_id = insert_data(db, cursor, "network_tcp", tcp_info["source"], tcp_info["destination"])

                if CONNECTION_TABLE_FLAG is True:
                    insert_data(db, cursor, "connection_type", "network_tcp", file_id, data_id)

    # Insert UDP connections

    if "udp" in check_jdata:
        for udp in jdata["network"]["udp"]:
            if "src" in udp and "dst" in udp:
                udp_info = {
                    "source":       str(udp["src"].encode("utf-8")),
                    "destination":  str(udp["dst"].encode("utf-8"))
                }

                data_id = check_data(cursor, "network_udp", udp_info["source"], udp_info["destination"])

                if data_id is False:
                    data_id = insert_data(db, cursor, "network_udp", udp_info["source"], udp_info["destination"])

                if CONNECTION_TABLE_FLAG is True:
                    insert_data(db, cursor, "connection_type", "network_udp", file_id, data_id)

    # Creating of memory check variable

    check_jdata = ""
    if "memory" in jdata:
        check_jdata = jdata["memory"]

    # Insert processes

    if "pslist" in check_jdata:
        if "data" in check_jdata["pslist"]:
            for process in jdata["memory"]["pslist"]["data"]:
                if "process_name" in process:
                    process_info = {
                        "process_name": str(process["process_name"].encode("utf-8"))
                    }

                    data_id = check_data(cursor, "process", process_info["process_name"])

                    if data_id is False:
                        data_id = insert_data(db, cursor, "process", process_info["process_name"])

                    if CONNECTION_TABLE_FLAG is True:
                        insert_data(db, cursor, "connection_type", "process", file_id, data_id)

    # Insert dropped files

    if "dropped" in jdata:
        for file_temp in jdata["dropped"]:
            process_name = ""
            if "pids" in file_temp:
                if len(file_temp["pids"]) is not 0:
                    for process in jdata["behavior"]["generic"]:
                        if process["pid"] == file_temp["pids"][0]:
                            process_name = process["process_name"]
                            break

            if "filepath" in file_temp and "type" in file_temp and "size" in file_temp:
                file_info = {
                    "path":     str(file_temp["filepath"].encode("utf-8")),
                    "type":     str(file_temp["type"].encode("utf-8")),
                    "process":  process_name,
                    "size":     str(file_temp["size"]),
                }

                data_id = check_data(cursor, "file_dropped", file_info["path"], file_info["type"],
                                     file_info["process"], file_info["size"])

                if data_id is False:
                    data_id = insert_data(db, cursor, "file_dropped", file_info["path"], file_info["type"],
                                          file_info["process"], file_info["size"])

                if CONNECTION_TABLE_FLAG is True:
                    insert_data(db, cursor, "connection_type", "file_dropped", file_id, data_id)

    # Creating of behavior check variable

    check_jdata = ""
    if "behavior" in jdata:
        if "summary" in jdata["behavior"]:
            check_jdata = jdata["behavior"]["summary"]

    # Insert loaded dlls

    if "dll_loaded" in check_jdata:
        for dll in jdata["behavior"]["summary"]["dll_loaded"]:
            dll_info = {
                "data_type":    "DLL loaded",
                "full_path":    str(dll.encode("utf-8").replace("\\", "/").replace("'", "_"))
            }

            data_id = check_data(cursor, "dll", dll_info["full_path"])

            if data_id is False:
                data_id = insert_data(db, cursor, "dll", dll_info["full_path"])

            if CONNECTION_TABLE_FLAG is True:
                insert_data(db, cursor, "connection_type", "dll", file_id, data_id)

    # Insert command line

    if "command_line" in check_jdata:
        for command in jdata["behavior"]["summary"]["command_line"]:
            command_info = {
                "data_type":    "Command line",
                "command":      str(command.encode("utf-8").replace("\\", "/").replace("'", "_"))
            }

            data_id = check_data(cursor, "command_line", command_info["command"])

            if data_id is False:
                data_id = insert_data(db, cursor, "command_line", command_info["command"])

            if CONNECTION_TABLE_FLAG is True:
                insert_data(db, cursor, "connection_type", "command_line", file_id, data_id)

    # Insert opened files

    if "file_opened" in check_jdata:
        for file_temp in jdata["behavior"]["summary"]["file_opened"]:
            file_info = {
                "action_type": "file_opened",
                "full_path": str(file_temp.encode("utf-8").replace("\\", "/").replace("'", "_"))
            }

            data_id = check_data(cursor, "file_action", file_info["action_type"], file_info["full_path"])

            if data_id is False:
                data_id = insert_data(db, cursor, "file_action", file_info["action_type"], file_info["full_path"])

            if CONNECTION_TABLE_FLAG is True:
                insert_data(db, cursor, "connection_type", "file_action", file_id, data_id)

    # Insert created files

    if "file_created" in check_jdata:
        for file_temp in jdata["behavior"]["summary"]["file_created"]:
            file_info = {
                "action_type": "file_created",
                "full_path": str(file_temp.encode("utf-8").replace("\\", "/").replace("'", "_"))
            }

            data_id = check_data(cursor, "file_action", file_info["action_type"], file_info["full_path"])

            if data_id is False:
                data_id = insert_data(db, cursor, "file_action", file_info["action_type"], file_info["full_path"])

            if CONNECTION_TABLE_FLAG is True:
                insert_data(db, cursor, "connection_type", "file_action", file_id, data_id)

    # Insert copied files

    if "file_copied" in check_jdata:
        for file_temp in jdata["behavior"]["summary"]["file_copied"][0]:
            file_info = {
                "action_type": "file_copied",
                "full_path": str(file_temp.encode("utf-8").replace("\\", "/").replace("'", "_"))
            }

            data_id = check_data(cursor, "file_action", file_info["action_type"], file_info["full_path"])

            if data_id is False:
                data_id = insert_data(db, cursor, "file_action", file_info["action_type"], file_info["full_path"])

            if CONNECTION_TABLE_FLAG is True:
                insert_data(db, cursor, "connection_type", "file_action", file_id, data_id)

    # Insert written files
    
    if "file_written" in check_jdata:
        for file_temp in jdata["behavior"]["summary"]["file_written"]:
            file_info = {
                "action_type": "file_written",
                "full_path": str(file_temp.encode("utf-8").replace("\\", "/").replace("'", "_"))
            }

            data_id = check_data(cursor, "file_action", file_info["action_type"], file_info["full_path"])

            if data_id is False:
                data_id = insert_data(db, cursor, "file_action", file_info["action_type"], file_info["full_path"])

            if CONNECTION_TABLE_FLAG is True:
                insert_data(db, cursor, "connection_type", "file_action", file_id, data_id)

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
                "full_path": str(file_temp.encode("utf-8").replace("\\", "/").replace("'", "_"))
            }

            data_id = check_data(cursor, "file_action", file_info["action_type"], file_info["full_path"])

            if data_id is False:
                data_id = insert_data(db, cursor, "file_action", file_info["action_type"], file_info["full_path"])

            if CONNECTION_TABLE_FLAG is True:
                insert_data(db, cursor, "connection_type", "file_action", file_id, data_id)

    # Insert created folders

    if "directory_created" in check_jdata:
        for directory in jdata["behavior"]["summary"]["directory_created"]:
            directory_info = {
                "action_type": "directory_created",
                "full_path": str(directory.encode("utf-8").replace("\\", "/").replace("'", "_"))
            }

            data_id = check_data(cursor, "folder_action", directory_info["action_type"], directory_info["full_path"])

            if data_id is False:
                data_id = insert_data(db, cursor, "folder_action", directory_info["action_type"],
                                      directory_info["full_path"])

            if CONNECTION_TABLE_FLAG is True:
                insert_data(db, cursor, "connection_type", "folder_action", file_id, data_id)

    # Insert deleted folders

    if "directory_removed" in check_jdata:
        for directory in jdata["behavior"]["summary"]["directory_removed"]:
            directory_info = {
                "action_type": "directory_removed",
                "full_path": str(directory.encode("utf-8").replace("\\", "/").replace("'", "_"))
            }

            data_id = check_data(cursor, "folder_action", directory_info["action_type"], directory_info["full_path"])

            if data_id is False:
                data_id = insert_data(db, cursor, "folder_action", directory_info["action_type"],
                                      directory_info["full_path"])

            if CONNECTION_TABLE_FLAG is True:
                insert_data(db, cursor, "connection_type", "folder_action", file_id, data_id)

    # Insert written registry

    if "regkey_written" in check_jdata:
        for regkey in jdata["behavior"]["summary"]["regkey_written"]:
            regkey_info = {
                "action_type": "regkey_written",
                "full_path": str(regkey.encode("utf-8").replace("\\", "/").replace("'", "_"))
            }

            data_id = check_data(cursor, "registry_action", regkey_info["action_type"], regkey_info["full_path"])

            if data_id is False:
                data_id = insert_data(db, cursor, "registry_action", regkey_info["action_type"],
                                      regkey_info["full_path"])

            if CONNECTION_TABLE_FLAG is True:
                insert_data(db, cursor, "connection_type", "registry_action", file_id, data_id)

    # Insert opened registry

    if "regkey_opened" in check_jdata:
        for regkey in jdata["behavior"]["summary"]["regkey_opened"]:
            regkey_info = {
                "action_type": "regkey_opened",
                "full_path": str(regkey.encode("utf-8").replace("\\", "/").replace("'", "_"))
            }

            data_id = check_data(cursor, "registry_action", regkey_info["action_type"], regkey_info["full_path"])

            if data_id is False:
                data_id = insert_data(db, cursor, "registry_action", regkey_info["action_type"],
                                      regkey_info["full_path"])

            if CONNECTION_TABLE_FLAG is True:
                insert_data(db, cursor, "connection_type", "registry_action", file_id, data_id)

    # Insert deleted registry

    if "regkey_deleted" in check_jdata:
        for regkey in jdata["behavior"]["summary"]["regkey_deleted"]:
            regkey_info = {
                "action_type": "regkey_deleted",
                "full_path": str(regkey.encode("utf-8").replace("\\", "/").replace("'", "_"))
            }

            data_id = check_data(cursor, "registry_action", regkey_info["action_type"], regkey_info["full_path"])

            if data_id is False:
                data_id = insert_data(db, cursor, "registry_action", regkey_info["action_type"],
                                      regkey_info["full_path"])

            if CONNECTION_TABLE_FLAG is True:
                insert_data(db, cursor, "connection_type", "registry_action", file_id, data_id)

    # Insert readed registry

    if "regkey_read" in check_jdata:
        for regkey in jdata["behavior"]["summary"]["regkey_read"]:
            regkey_info = {
                "action_type": "regkey_read",
                "full_path": str(regkey.encode("utf-8").replace("\\", "/").replace("'", "_"))
            }

            data_id = check_data(cursor, "registry_action", regkey_info["action_type"], regkey_info["full_path"])

            if data_id is False:
                data_id = insert_data(db, cursor, "registry_action", regkey_info["action_type"],
                                      regkey_info["full_path"])

            if CONNECTION_TABLE_FLAG is True:
                insert_data(db, cursor, "connection_type", "registry_action", file_id, data_id)

    print("%-30s" % print_string + "%s" % "Report added.")

    # Close JSON file

    json_close()


# Function to process report

def check_report(cursor, file_path, file_name):
    """ file_path - path to file
        file_name - name of file
        Before function call MySQL connection must be created
        Function return array with new data
    """

    virus_flag = "Clean"
    print_string = "check_report: "
    data = []
    virus_array = ""

    # Open JSON file

    jdata = json_open(file_path, file_name)

    # Creating of virustotal check variable

    check_jdata = ""
    if "virustotal" in jdata:
        check_jdata = jdata["virustotal"]

    # Virustotal check

    if "scans" in check_jdata:
        for scan in check_jdata["scans"]:
            if "detected" in check_jdata["scans"][scan]:
                if check_jdata["scans"][scan]["detected"] is True:
                    virus_flag = "Malware"
                    if "result" in check_jdata["scans"][scan]:
                        virus_array = virus_array + str(check_jdata["scans"][scan]["result"]) + ", "

    # File information

    if "target" in jdata:
        if "file" in jdata["target"]:
            if "name" in jdata["target"]["file"] and "size" in jdata["target"]["file"] and "md5" in\
                    jdata["target"]["file"] and "type" in jdata["target"]["file"]:
                file_info = {
                    "data_type": "File info",
                    "name": str(jdata["target"]["file"]["name"].encode("utf-8")),
                    "type": str(jdata["target"]["file"]["type"].encode("utf-8")),
                    "size": str(jdata["target"]["file"]["size"] * 1.0 / (1024 * 1024)) + "MB",
                    "md5":  str(jdata["target"]["file"]["md5"].encode("utf-8")),
                    "flag_virustotal": virus_flag,
                    "virus_array": virus_array
                }

                data.append(file_info)

    # Signatures

    if "signatures" in jdata:
        for sig in jdata["signatures"]:
            if "description" in sig:
                sig_info = {
                    "data_type":        "Signature",
                    "description":      str(sig["description"].encode("utf-8")),
                }

                data.append(sig_info)

    # Creating of network check variable

    check_jdata = ""
    if "network" in jdata:
        check_jdata = jdata["network"]

    # DNS connections

    if "dns" in check_jdata:
        for dns in jdata["network"]["dns"]:
            if "type" in dns and "request" in dns and "answers" in dns:
                dns_info = {
                    "data_type":    "DNS connection",
                    "type":         str(dns["type"].encode("utf-8")),
                    "request":      str(dns["request"].encode("utf-8")),
                    "answer":       ""
                }

                if len(dns["answers"]) > 0:
                    if "data" in dns["answers"][0]:
                        dns_info["answer"] = str(dns["answers"][0]["data"].encode("utf-8"))

                data_id = check_data(cursor, "network_dns", dns_info["type"], dns_info["request"])

                if data_id is False:
                    data.append(dns_info)

    # HTTP connections

    if "http" in check_jdata:
        for http in jdata["network"]["http"]:
            if "uri" in http and "host" in http:
                http_info = {
                    "data_type":    "HTTP connection",
                    "url":          str(http["uri"].encode("utf-8")),
                    "host":         str(http["host"].encode("utf-8"))
                }

                data_id = check_data(cursor, "network_http", http_info["url"], http_info["host"])

                if data_id is False:
                    data.append(http_info)

    # TCP connections

    if "tcp" in check_jdata:
        for tcp in jdata["network"]["tcp"]:
            if "src" in tcp and "dst" in tcp:
                tcp_info = {
                    "data_type":    "TCP connection",
                    "source":       str(tcp["src"].encode("utf-8")),
                    "destination":  str(tcp["dst"].encode("utf-8"))
                }

                data_id = check_data(cursor, "network_tcp", tcp_info["source"], tcp_info["destination"])

                if data_id is False:
                    data.append(tcp_info)

    # UDP connections

    if "udp" in check_jdata:
        for udp in jdata["network"]["udp"]:
            if "src" in udp and "dst" in udp:
                udp_info = {
                    "data_type":    "UDP connection",
                    "source":       str(udp["src"].encode("utf-8")),
                    "destination":  str(udp["dst"].encode("utf-8"))
                }

                data_id = check_data(cursor, "network_udp", udp_info["source"], udp_info["destination"])

                if data_id is False:
                    data.append(udp_info)

    # Creating of memory check variable

    check_jdata = ""
    if "memory" in jdata:
        check_jdata = jdata["memory"]

    # Processes

    if "pslist" in check_jdata:
        if "data" in check_jdata["pslist"]:
            for process in jdata["memory"]["pslist"]["data"]:
                if "process_name" in process:
                    process_info = {
                        "data_type":    "Process",
                        "process_name": str(process["process_name"].encode("utf-8"))
                    }

                    data_id = check_data(cursor, "process", process_info["process_name"])

                    if data_id is False:
                        data.append(process_info)

    # Dropped files

    if "dropped" in jdata:
        for file_temp in jdata["dropped"]:
            process_name = ""
            if "pids" in file_temp:
                if len(file_temp["pids"]) is not 0:
                    for process in jdata["behavior"]["generic"]:
                        if process["pid"] == file_temp["pids"][0]:
                            process_name = process["process_name"]
                            break

            if "filepath" in file_temp and "type" in file_temp and "size" in file_temp:
                file_info = {
                    "data_type":    "Dropped file",
                    "path":     str(file_temp["filepath"].encode("utf-8")),
                    "type":     str(file_temp["type"].encode("utf-8")),
                    "process":  process_name,
                    "size":     str(file_temp["size"]),
                }

                data_id = check_data(cursor, "file_dropped", file_info["path"], file_info["type"],
                                     file_info["process"], file_info["size"])

                if data_id is False:
                    data.append(file_info)

    # Creating of behavior check variable

    check_jdata = ""
    if "behavior" in jdata:
        if "summary" in jdata["behavior"]:
            check_jdata = jdata["behavior"]["summary"]

    # Loaded dlls

    if "dll_loaded" in check_jdata:
        for dll in jdata["behavior"]["summary"]["dll_loaded"]:
            dll_info = {
                "data_type":    "DLL loaded",
                "full_path":    str(dll.encode("utf-8").replace("\\", "/").replace("'", "_"))
            }

            data_id = check_data(cursor, "dll", dll_info["full_path"])

            if data_id is False:
                data.append(dll_info)

    # Command line

    if "command_line" in check_jdata:
        for command in jdata["behavior"]["summary"]["command_line"]:
            command_info = {
                "data_type":        "Command line",
                "command":     str(command.encode("utf-8").replace("\\", "/").replace("'", "_"))
            }

            data_id = check_data(cursor, "command_line", command_info["command"])

            if data_id is False:
                data.append(command_info)

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
                "full_path":    str(file_temp.encode("utf-8").replace("\\", "/").replace("'", "_"))
            }

            data_id = check_data(cursor, "file_action", file_info["action_type"], file_info["full_path"])

            if data_id is False:
                data.append(file_info)

    # Created files
    # Detect all files except .tmp and .TMP

    if "file_created" in check_jdata:
        for file_temp in jdata["behavior"]["summary"]["file_created"]:
            # if file_temp.find(".tmp") is not -1:
            #    continue
            # elif file_temp.find(".TMP") is not -1:
            #    continue

            file_info = {
                "data_type":    "Created file",
                "action_type":  "file_created",
                "full_path":    str(file_temp.encode("utf-8").replace("\\", "/").replace("'", "_"))
            }

            data_id = check_data(cursor, "file_action", file_info["action_type"], file_info["full_path"])

            if data_id is False:
                data.append(file_info)

    # Copied files

    if "file_copied" in check_jdata:
        for file_temp in jdata["behavior"]["summary"]["file_copied"][0]:
            file_info = {
                "data_type":    "Copied file",
                "action_type":  "file_copied",
                "full_path":    str(file_temp.encode("utf-8").replace("\\", "/").replace("'", "_"))
            }

            data_id = check_data(cursor, "file_action", file_info["action_type"], file_info["full_path"])

            if data_id is False:
                data.append(file_info)

    # Opened files

    if "file_opened" in check_jdata:
        for file_temp in jdata["behavior"]["summary"]["file_opened"]:
            file_info = {
                "data_type":    "Opened file",
                "action_type":  "file_opened",
                "full_path":    str(file_temp.encode("utf-8").replace("\\", "/").replace("'", "_"))
            }

            data_id = check_data(cursor, "file_action", file_info["action_type"], file_info["full_path"])

            if data_id is False:
                data.append(file_info)

    # Written files

    if "file_written" in check_jdata:
        for file_temp in jdata["behavior"]["summary"]["file_written"]:
            file_info = {
                "data_type":    "Written file",
                "action_type":  "file_written",
                "full_path":    str(file_temp.encode("utf-8").replace("\\", "/").replace("'", "_"))
            }

            data_id = check_data(cursor, "file_action", file_info["action_type"], file_info["full_path"])

            if data_id is False:
                data.append(file_info)

    # Created folders

    if "directory_created" in check_jdata:
        for directory in jdata["behavior"]["summary"]["directory_created"]:
            directory_info = {
                "data_type":    "Created folder",
                "action_type":  "directory_created",
                "full_path":    str(directory.encode("utf-8").replace("\\", "/").replace("'", "_"))
            }

            data_id = check_data(cursor, "folder_action", directory_info["action_type"], directory_info["full_path"])

            if data_id is False:
                data.append(directory_info)

    # Deleted folders

    if "directory_removed" in check_jdata:
        for directory in jdata["behavior"]["summary"]["directory_removed"]:
            directory_info = {
                "data_type":    "Deleted folder",
                "action_type":  "directory_removed",
                "full_path":    str(directory.encode("utf-8").replace("\\", "/").replace("'", "_"))
            }

            data_id = check_data(cursor, "folder_action", directory_info["action_type"], directory_info["full_path"])

            if data_id is False:
                data.append(directory_info)

    # Written registry

    if "regkey_written" in check_jdata:
        for regkey in jdata["behavior"]["summary"]["regkey_written"]:
            regkey_info = {
                "data_type":    "Written registry",
                "action_type":  "regkey_written",
                "full_path":    str(regkey.encode("utf-8").replace("\\", "/").replace("'", "_"))
            }

            data_id = check_data(cursor, "registry_action", regkey_info["action_type"], regkey_info["full_path"])

            if data_id is False:
                data.append(regkey_info)

    # Opened registry

    if "regkey_opened" in check_jdata:
        for regkey in jdata["behavior"]["summary"]["regkey_opened"]:
            regkey_info = {
                "data_type":    "Opened registry",
                "action_type":  "regkey_opened",
                "full_path":    str(regkey.encode("utf-8").replace("\\", "/").replace("'", "_"))
            }

            data_id = check_data(cursor, "registry_action", regkey_info["action_type"], regkey_info["full_path"])

            if data_id is False:
                data.append(regkey_info)

    # Deleted registry

    if "regkey_deleted" in check_jdata:
        for regkey in jdata["behavior"]["summary"]["regkey_deleted"]:
            regkey_info = {
                "data_type":    "Deleted registry",
                "action_type":  "regkey_deleted",
                "full_path":    str(regkey.encode("utf-8").replace("\\", "/").replace("'", "_"))
            }

            data_id = check_data(cursor, "registry_action", regkey_info["action_type"], regkey_info["full_path"])

            if data_id is False:
                data.append(regkey_info)

    # Readed registry

    if "regkey_read" in check_jdata:
        for regkey in jdata["behavior"]["summary"]["regkey_read"]:
            regkey_info = {
                "data_type":    "Readed registry",
                "action_type":  "regkey_read",
                "full_path":    str(regkey.encode("utf-8").replace("\\", "/").replace("'", "_"))
            }

            data_id = check_data(cursor, "registry_action", regkey_info["action_type"], regkey_info["full_path"])

            if data_id is False:
                data.append(regkey_info)

    # Print new data

    if PRINT_FLAG is True:
        for i in range(0, len(data)):
            print(print_string + data[i]["data_type"] + ": " + str(data[i]))

    print("%-30s" % print_string + "Total detected data: " + str(len(data)))

    # Close JSON file

    json_close()

    # Return array with new data

    return data


# Function to clear database

def clear_db(db, cursor):
    """ Function delete all data from database """

    print_string = "clear_db: "

    for i in range(0, len(MYSQL_TABLES)):
        add_string = "DELETE FROM " + MYSQL_TABLES[i] + ""
        cursor.execute(add_string)
        db.commit()
        add_string = "ALTER TABLE " + MYSQL_TABLES[i] + " AUTO_INCREMENT=1"
        cursor.execute(add_string)
        db.commit()

    print("%-30s" % print_string + "%s" % "Data deleted.")


# Function to count database length

def length_db(cursor):
    """ Function return number of elements in database sorted by type of data
        data[0] - number of connection data
        data[1] - number of files in database
        data[2] - number of files actions in database
        data[3] - number of network connections in database
        data[4] - number of process in database
        data[5] - number of registry actions in database
        data[6] - number of DLL's in database
        data[7] - number of command of command line in database
    """

    print_string = "length_db: "
    data = [0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(0, 13):
        add_string = "SELECT COUNT(*) FROM " + MYSQL_TABLES[i]
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
        elif i is 11:
            data[6] = item[0]
        elif i is 12:
            data[7] = item[0]

    print("%-30s" % print_string + "%s" % "Data processed.")

    return data


# Function to check cuckoo status

def cuckoo_status():
    """ Function return True if Cuckoo Sandbox available and else return False """

    print_string = "cuckoo_status: "

    result = subprocess.Popen(["pgrep", "-a", "cuckoo"], stdout=subprocess.PIPE)
    stdout = result.communicate()

    if stdout[0].find("cuckoo web") is not -1:
        if len(stdout[0].split()) is 7:
            print("%-30s" % print_string + "Cuckoo status: On")
            return True
        else:
            print("%-30s" % print_string + "Cuckoo status: Off")
            return False
    elif stdout[0] != "":
        print("%-30s" % print_string + "Cuckoo status: On")
        return True
    else:
        print("%-30s" % print_string + "Cuckoo status: Off")
        return False


# Function to check disk space

def disk_space():
    """ Function return free disk space
        free_space - free disk space
    """

    print_string = "disk_space: "

    statvfs = os.statvfs("/home")
    free_space = (statvfs.f_frsize * statvfs.f_bavail * 1.0) / (1024 * 1024 * 1024)

    print("%-30s" % print_string + "Usage disk space: %.2f" % free_space + "G")

    return free_space


# Function to delete memory dump if exist (Tested with build-in strings)

def delete_memory_dump(report_id):
    """ Function to delete memory dump file """

    print_string = "delete_memory_dump: "

    result = subprocess.check_output(["ls", PATH_ANALYSES + str(report_id)])
    result_flag = result.find("memory.dmp")

    if result_flag is not -1:
        subprocess.call(["rm", PATH_ANALYSES + str(report_id) + "/memory.dmp"])
        print("%-30s" % print_string + "Dump file deleted.")
    else:
        print("%-30s" % print_string + "Dump file not exist.")


# Function to change or return statistical data

def statistic_data(db, cursor, function_type, scan_time=0):
    """ Function to change or return statistical data
        function_type == True - Add scanned file and change average scan time
        function_type == False - Return number of scans and average scan time
        scans or item[0] - scan number
        average_scan_time or item[1] - average scan time
    """

    print_string = "statistic_data: "

    if function_type is True:
        query = "SELECT * FROM statistic LIMIT 1"
        cursor.execute(query)
        item = cursor.fetchone()

        average_scan_time = (item[1] * item[0] + scan_time)/(item[0] + 1)
        scans = item[0] + 1

        add_string = "UPDATE statistic SET scans = %s, average_scan_time = %s"
        data = (scans, average_scan_time)

        cursor.execute(add_string, data)
        db.commit()

        print("%-30s" % print_string + "Scans: %d" % scans + ", Average time scan: %d" % average_scan_time + "sec")

        return scans, average_scan_time

    elif function_type is False:
        query = "SELECT * FROM statistic LIMIT 1"
        cursor.execute(query)
        item = cursor.fetchone()

        print("%-30s" % print_string + "Scans: %d" % item[0] + ", Average time scan: %d" % item[1] + "sec")

        return item[0], item[1]


# Function to reset statistical data

def statistic_reset(db, cursor):
    """ Function reset statistic data """
    print_string = "statistic_reset: "

    add_string = "UPDATE statistic SET scans = %s, average_scan_time = %s"
    data = (0, 0.0)

    cursor.execute(add_string, data)
    db.commit()

    print("%-30s" % print_string + "Statistical data reseted.")


# Function to return database size

def size_db(cursor):
    """ Function return size of database in MB """

    print_string = "size_db: "

    query = "SELECT table_schema AS 'Database', SUM(data_length + index_length) \
     / 1024 / 1024 AS 'Size (MB)' FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'cuckoo'"

    cursor.execute(query)
    item = cursor.fetchone()

    print("%-30s" % print_string + "Database size: %.2f" % item[1] + "MB")

    return item[1]


# Function to add set of reports to database

def learn_set(db, cursor, folder_path):
    """ Function add reports from folder to database
        folder_path - folder with reports
    """

    print_string = "learn_set: "

    files = os.listdir(folder_path)

    for file_name in files:
        if file_name.find(".json") is not -1:
            add_report(db, cursor, folder_path, file_name)

    print("%-30s" % print_string + "All reports added to data base.")
