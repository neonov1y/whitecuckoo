# imports
import functions

# variables
reports_ids = (1, 5)
virus_flag = False
print_string = "initialization: "
# open mysql connection
cursor = functions.mysql_create_connection()

data_id = functions.insert_data("file", "hi77", "pdf", 2000, "500", True)
print("%-30s" % print_string + "Data ID = %s" % data_id)

# data_id = functions.check_data("file", "hi", "pdf", 2000, "500", True)
# print("%-30s" % print_string + "Data ID = %s" % data_id)

functions.mysql_close_connection()
