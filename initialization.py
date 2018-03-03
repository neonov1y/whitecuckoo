# Imports

import functions

# Variables

reports_ids = (1, 5)
virus_flag = False

# Open MySQL connection

cursor = functions.mysql_create_connection()
functions.cuckoo_status()

# Add JSON files (reports)

#functions.add_report("reports/", "report13.json")

# functions.clear_db()

# for i in range(reports_ids[0], reports_ids[1]):
#    functions.add_report("reports/", "report" + str(i) + ".json")

# Close MySQL connection

functions.mysql_close_connection()
