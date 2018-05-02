import sys
import os
import mysql.connector
import mysql_user_config
import unicodedata	
import datetime


def safe_str_convert(convert_val):
    if type(convert_val) == unicode:
        return unicodedata.normalize('NFKD', convert_val).encode('ascii','ignore')
    elif type(convert_val) == int:
        return str(convert_val)
    elif type(convert_val) == datetime.datetime:
        return str(convert_val)
    else:
        return "None"

def addCategories(sysArgv0, cursor):
	categories_FilePath = os.path.dirname(sys.argv[0]) + "\\categories.txt"
 	file = open(categories_FilePath, 'r')	# Change file according to where it is for you
 	cats = file.read().split("\n")
 	file.close()
 	for curr_category in cats:
 		insertCmd = "INSERT INTO res_categories (res_category) VALUES ('" + curr_category + "')"
 		cursor.execute(insertCmd)


#########################
# Execution Starts Here #
#########################

db = mysql.connector.connect(user=mysql_user_config.user, password=mysql_user_config.password, host=mysql_user_config.host)
cursor = db.cursor()

# Start using the yelp database
query = "USE yelp_db"
cursor.execute(query);

# Creates a table for the resturaunt categories
query = "SHOW TABLES LIKE 'res_categories'"
cursor.execute(query)
result = cursor.fetchone()
# if result is None:

cmd = 'CREATE TABLE IF NOT EXISTS res_categories (res_category VARCHAR(225))'
cursor.execute(cmd)

isExist = raw_input("Does res_categories table already exist for you? (y/n):");
if isExist.lower() == "y":
	query = 'TRUNCATE TABLE res_categories'
	cursor.execute(query)
	addCategories(sys.argv[0], cursor)
	db.commit()

# If the table already exists then remove it
isExist = raw_input("Does this table already exist for you? (y/n):");
if isExist.lower() == "y":
	query = 'TRUNCATE TABLE res_business'
	cursor.execute(query)

# Creates new table
cmd = 'CREATE TABLE IF NOT EXISTS res_business (business_id VARCHAR(22), category VARCHAR(225))'
cursor.execute(cmd)

# Inserts all data that is the res_categories table into the res_business table
insertCmd = "INSERT INTO res_business (business_id, category) SELECT business.id, category FROM business INNER JOIN category ON category.business_id = business.id WHERE category IN (SELECT res_category FROM res_categories)"

cursor.execute(insertCmd)
db.commit()

cursor.close()
print "res_business Table is Done!"