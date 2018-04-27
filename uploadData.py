import mysql.connector
import test_var

# Creates the data base if it does not exist, then it creates the table if it does not already exist
def create_databse():
	# This creates the database
	db = mysql.connector.connect(host= test_var.host, user= user.host, password= test_var.password)
	cursor = db.cursor()
	cmd = 'CREATE DATABASE IF NOT EXISTS yelp_weather_db'
	cursor.execute(cmd)

	# This will create the table
	# weather => |state| myDate| temp|
	cmd = '''CREATE TABLE IF NOT EXISTS weather (
				state VARCHAR(50),
				myDate DATE DEF,
				temp INT
			'''
	cursor.execute(sql)

# Parses the given file
def read_File(filename):
	
















