import sys
import os
import mysql.connector
import mysql_user_config

# Creates the data base if it does not exist, then it creates the table if it does not already exist
def create_databse():
	# Connects to MYSQL server
	db = mysql.connector.connect(user=mysql_user_config.user, password=mysql_user_config.password, host=mysql_user_config.host)
	cursor = db.cursor()
	# Create new database, yelp_weather_db, if it does not already exists
	query = 'CREATE DATABASE IF NOT EXISTS yelp_weather_db'
	cursor.execute(query)

	# Uses that database
	query = 'USE yelp_weather_db'
	cursor.execute(query)
	
	# Creates table in the yelp_weather_db database if the weather table does not already exist
	# weather => |state| myDate| temp|
	cmd = 'CREATE TABLE IF NOT EXISTS weather (state VARCHAR(50),myDate DATE,temp INT)'
	cursor.execute(cmd)
	print "Database CREATED!!!"
	
	# closes unneeded connections
	cursor.close()
	db.close()
	
# clears old data to prevent duplicate data from being entered
def clear_weather_table(cursor):
	query = 'TRUNCATE TABLE weather'
	cursor.execute(query)
	print "Table CLEARED!!!\n"

# reads from text file and inputs extracted data into database
def insert_txtfile_into_table(cursor, filepath):
	counter = 1
	with open(filepath) as fp:  
		line = fp.readline()
		state = "None"
		while line:
			if counter == 1:
				split_string = line.split(',')
				if len(split_string) == 2 and split_string[0].lower() == "state":
					state = split_string[1].strip()
					sys.stdout.write(state.upper() + ": [")
				else:
					sys.stdout.write('ERROR: Valid state NOT found!')
					break
			elif counter == 2:
				pass
			else:
				split_string = line.strip().split(',')
				
				date_string = split_string[2][0:5] + "-" + split_string[2][5:7] + "-" + split_string[2][7:9] + " 00:00:00"
				temp_string = str(int(float(split_string[3])))
				insertStatement = "INSERT INTO weather (state, myDate, temp) VALUES ('" + state + "','" + date_string + "'," + temp_string + ")"
				cursor.execute(insertStatement)
				
				#print(temp_string + " " + date_string + " " + split_string[2])
				
			if counter % 100 == 0:
				sys.stdout.write('#')
			
			line = fp.readline()
			counter += 1
	db.commit()
	print("] (Total Rows Read: " + str(counter - 2) + ")")

'''
Execution Starts Here
'''
	
create_databse()

db = mysql.connector.connect(user=mysql_user_config.user, password=mysql_user_config.password, host=mysql_user_config.host, database="yelp_weather_db")
cursor = db.cursor()

# prompts users on if they wish to reset database before loading new data to prevent duplicate data from being entered
isClear = raw_input("Clear weather table before upload? (Y/n):");
if isClear.lower() == "y":
	clear_weather_table(cursor)

# gets all files from the selected container folder name 'weather_file_container' in the same directory as this file
data_file_directory_path = os.path.dirname(sys.argv[0]) + "\\weather_file_container\\"
data_file_list = [f for f in os.listdir(data_file_directory_path) if os.path.isfile(os.path.join(data_file_directory_path, f))]

# loops through all files in the container and uploads there data
for filepath in data_file_list:
	filepath = data_file_directory_path + filepath
	insert_txtfile_into_table(cursor, filepath)
