# Imports
import time
import subprocess
import functions

# Variables

reports_ids = (1, 5)
virus_flag = False

# Open MySQL connection

cursor = functions.mysql_create_connection()
# functions.clear_db()

# functions.cuckoo_status()

# Add JSON files (reports)

# functions.add_report("reports/", "report12.json")

# functions.clear_db()

# for i in range(reports_ids[0], reports_ids[1]):
#    functions.add_report("reports/", "report" + str(i) + ".json")
# data = functions.check_report("reports/", "report20.json")

functions.disk_space()

# Close MySQL connection

functions.mysql_close_connection()

# VBS file creation

while 0:
    result = subprocess.check_output(["ls", "/home/alex/.cuckoo/storage/analyses/latest/"])
    print(result.find("reports"))
    if result is not -1:
        time.sleep(1)
        break
    time.sleep(1)
