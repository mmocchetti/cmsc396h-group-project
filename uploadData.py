import mysql.connector
import mysql_user_config

# Creates the data base if it does not exist, then it creates the table if it does not already exist
def create_databse(cursor):
	# This creates the database
	#cmd = 'CREATE DATABASE IF NOT EXISTS yelp_weather_db'
	#cursor.execute(cmd)

	# This will create the table
	# weather => |state| myDate| temp|
	cmd = 'CREATE TABLE IF NOT EXISTS weather (state VARCHAR(50),myDate DATE,temp INT)'
	cursor.execute(cmd)
	print "Database CREATED!!!"

db = mysql.connector.connect(user=mysql_user_config.user, password=mysql_user_config.password, host=mysql_user_config.host, database="yelp_weather_db")
cursor = db.cursor()
	
create_databse(cursor)

filepath = 'C:\\Users\\nbathras\\OneDrive\\Documents\\Coding\\Python Coding\\weather_project\\az_2010_2018.txt'  
with open(filepath) as fp:  
	line = fp.readline()
	cnt = 1
	while line:
		if cnt < 2:
			cnt += 1
			line = fp.readline()
			pass
		else:
			#print("Line {}: {}".format(cnt, line.strip()))
			#print("Line " + str(cnt) + ": " + line.strip())
			split_string = line.strip().split(',')
			date_string = split_string[2][0:5] + "-" + split_string[2][5:7] + "-" + split_string[2][7:9] + " 00:00:00"
			int_temp = 10
			print(str(int(float(split_string[3]))) + " " + date_string + " " + split_string[2])
			insertStatement = "INSERT INTO weather (state, myDate, temp) VALUES ('AZ','" + date_string + "'," + str(int(float(split_string[3]))) + ")"
			cursor.execute(insertStatement)
			line = fp.readline()
			cnt += 1

db.commit()	
