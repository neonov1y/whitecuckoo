# Imports
import time
import subprocess
import functions

# Variables

reports_ids = (1, 5)
virus_flag = False

# Open MySQL connection

# functions.cuckoo_status()
'''
result = ""
t = subprocess.Popen(["pgrep", "-a", "cuckoo"], stdout=subprocess.PIPE)
stdout = t.communicate()
print(stdout[0].find("cuckoo web"))
if stdout[0].find("cuckoo web") is not -1:
    if len(stdout[0].split()) is 7:
        result = True
    else:
        result = False
elif stdout[0] != "":
    result = True
else:
    result = False

res = stdout[0].split("\n")
print(res)
if res[0] != "":
    result = int(res[0])
print(result)
'''

# db, cursor = functions.mysql_create_connection()
# time.sleep(10)

# functions.statistic_data(False)
# functions.delete_memory_dump(5)
# functions.disk_space()
# functions.learn_set("/home/alex/PycharmProjects/Cuckoo/white_list_set_2/")
# functions.statistic_reset()
# functions.statistic_change(True, 5)
# a, b = functions.statistic_change(False)
# print(str(a) + " " + str(b))

# functions.clear_db()

# functions.cuckoo_status()

# Add JSON files (reports)

# functions.add_report("reports/", "report12.json")

# functions.clear_db()

# for i in range(reports_ids[0], reports_ids[1]):
#    functions.add_report("reports/", "report" + str(i) + ".json")
# data = functions.check_report("/home/alex/.cuckoo/storage/analyses/15/reports/", "report.json")

# functions.disk_space()

# Close MySQL connection

# functions.mysql_close_connection(db, cursor)

# VBS file creation

while 0:
    result = subprocess.check_output(["ls", "/home/alex/.cuckoo/storage/analyses/latest/"])
    print(result.find("reports"))
    if result is not -1:
        time.sleep(1)
        break
    time.sleep(1)
