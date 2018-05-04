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

def addCategories(cursor):
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
cursor = db.cursor(buffered=True)

# Start using the yelp database
query = "USE yelp_db"
cursor.execute(query);

isFormatBusiNames = raw_input("Have you formatted the business names? (y/n):");

if isFormatBusiNames.lower() == 'n':
	query = "SELECT id, name FROM business"
	cursor.execute(query)

	db_update = mysql.connector.connect(user=mysql_user_config.user, password=mysql_user_config.password, host=mysql_user_config.host, database="yelp_db")
	cursor_update = db_update.cursor()

	for id,name in cursor:
		updated_name = safe_str_convert(name)
		new_query = "UPDATE business SET name=%s WHERE id=%s"
		cursor_update.execute(new_query, (updated_name,str(id)))
		
	db_update.commit()
	
	print("Business Name have been formatted!")

# Creates a table for the resturaunt categories
query = "SHOW TABLES LIKE 'res_categories'"
cursor.execute(query)
result = cursor.fetchone()

cmd = 'CREATE TABLE IF NOT EXISTS res_categories (res_category VARCHAR(225))'
cursor.execute(cmd)

# Creates new table
cmd = 'CREATE TABLE IF NOT EXISTS res_business (id VARCHAR(22) NOT NULL, category VARCHAR(225), state VARCHAR(225), name VARCHAR(225), PRIMARY KEY (id))'
cursor.execute(cmd)

isExist = raw_input("Do you want to clear previous data in res_categories table? (y/n):");
if isExist.lower() == "y":
	query = 'TRUNCATE TABLE res_categories'
	cursor.execute(query)

addCategories(cursor)
db.commit()

# If the table already exists then remove it
isExist = raw_input("Do you want to clear previous data in res_business? (y/n):");
if isExist.lower() == "y":
	query = 'TRUNCATE TABLE res_business'
	cursor.execute(query)

query = "SELECT id, name FROM business"
cursor.execute(query)
    
# Inserts all data that is the res_categories table into the res_business table
# Known Problem: only records the first category associated with the business
insertCmd = "INSERT IGNORE INTO res_business (id, category, state, name) SELECT business.id, category, state, name FROM business INNER JOIN category ON category.business_id = business.id WHERE category IN (SELECT res_category FROM res_categories)"

cursor.execute(insertCmd)
db.commit()

cursor.close()
print "res_business Table is Done!"
