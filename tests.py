# Imports
from os import listdir
import functions


# Constants

TEST_ID = 0
PATH_TEST_JSON_FILES = "/home/alex/PycharmProjects/Cuckoo/test_files/"

# Open MySQL connection
db, cursor = functions.mysql_create_connection()

# Test 1 - open and close json reports (json_open and json_close)
if TEST_ID == 1:
    files = listdir(PATH_TEST_JSON_FILES)

    for file_name in files:
        jdata = functions.json_open(PATH_TEST_JSON_FILES, file_name)
        functions.json_close()

# Test 2 - scan json reports (check_report)
elif TEST_ID == 2:
    files = listdir(PATH_TEST_JSON_FILES)

    for file_name in files:
        data = functions.check_report(cursor, PATH_TEST_JSON_FILES, file_name)
        print(data)

# Test 3 - add json reports (add_report)
elif TEST_ID == 3:
    files = listdir(PATH_TEST_JSON_FILES)

    for file_name in files:
        data = functions.add_report(cursor, PATH_TEST_JSON_FILES, file_name)

# Test 4 - clear database (clear_db)
elif TEST_ID == 4:
    functions.clear_db(db, cursor)

# Test 5 - length database (length_db)
elif TEST_ID == 5:
    data = functions.length_db(cursor)
    print(data)

# Test 6 - check cuckoo sandbox status (cuckoo_status)
elif TEST_ID == 6:
    status = functions.cuckoo_status()
    print(status)

# Test 7 - check free space (disk_space)
elif TEST_ID == 7:
    free_space = functions.disk_space()
    print(free_space)

# Test 8 - delete memory dump (delete_memory_dump)
elif TEST_ID == 8:
    report_id = 50
    functions.delete_memory_dump(report_id)

# Test 9 - get and change statistic data (statistic_data)
elif TEST_ID == 9:
    scans, scan_time = functions.statistic_data(db, cursor, False)
    print("scans: " + str(scans) + " scan_time: " + str(scan_time))
    scans, scan_time = functions.statistic_data(db, cursor, True, 55)
    print("scans: " + str(scans) + " scan_time: " + str(scan_time))
    scans, scan_time = functions.statistic_data(db, cursor, False)
    print("scans: " + str(scans) + " scan_time: " + str(scan_time))

# Test 10 - reset statistic data (statistic_reset)
elif TEST_ID == 10:
    scans, scan_time = functions.statistic_data(db, cursor, False)
    print("scans: " + str(scans) + " scan_time: " + str(scan_time))
    functions.statistic_reset(db, cursor)
    scans, scan_time = functions.statistic_data(db, cursor, False)
    print("scans: " + str(scans) + " scan_time: " + str(scan_time))

# Test 11 - check database size (size_db)
elif TEST_ID == 11:
    size = functions.size_db(cursor)
    print(size)

# Test 12 - learn standart reports set (learn_set)
elif TEST_ID == 12:
    size = functions.learn_set(db, cursor, functions.PATH_STANDART_SET)

# Close MySQL connection
functions.mysql_close_connection(db, cursor)
