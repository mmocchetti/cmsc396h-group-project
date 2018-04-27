import mysql.connector
import sys
import mysql_user_config
import unicodedata

#
# Make sure to run these commands first: we have not automated this system yet
# use yelp_weather_db;
# CREATE DATABASE IF NOT EXISTS yelp_weather_db;
# CREATE TABLE IF NOT EXISTS weather (state VARCHAR(50),myDate DATE,temp INT);
#

cnx = mysql.connector.connect(user=mysql_user_config.user, password=mysql_user_config.password, host=mysql_user_config.host, database=mysql_user_config.database)
cursor = cnx.cursor()

query = ("SELECT id,business_id,stars,date FROM review LIMIT 1000")
cursor.execute(query)

business_list = list()

for id,business_id,stars,date in cursor:
    individual_business = list()
    #print(str(id) + " | " + str(business_id) + " | " + str(stars) + " | " + str(date))
    individual_business.append(unicodedata.normalize('NFKD', id).encode('ascii','ignore'))
    individual_business.append(unicodedata.normalize('NFKD', business_id).encode('ascii','ignore'))
    individual_business.append(str(stars))
    individual_business.append(str(date))
    
    business_list.append(individual_business)
    
print("Review ID:             | Business ID:           | Date of Review      | * | Temperature: | State: |")
print("-----------------------+------------------------+---------------------+---+--------------+--------+------------------------------")
    
cnx2 = mysql.connector.connect(user=mysql_user_config.user, password=mysql_user_config.password, host=mysql_user_config.host, database="yelp_weather_db")
cursor2 = cnx2.cursor()
	
for individual_business in business_list:
    query = ("SELECT id,name,state FROM business WHERE (id='" + individual_business[1] +"')")
    cursor.execute(query)
    
    for id,name,state in cursor:
		#print(individual_business[0] + " | " + str(id) + " | " + individual_business[3] + " | " + individual_business[2] + " |   " + str(state) + "   | " + str(name))

		query = ("SELECT state,myDate,temp FROM weather WHERE (state='" + str(state) + "') AND (myDate='" + individual_business[3] + "')")
		cursor2.execute(query)

		for state,myDate,temp in cursor2:
			print(individual_business[0] + " | " + unicodedata.normalize('NFKD', id).encode('ascii','ignore') + " | " + individual_business[3] + " | " + individual_business[2] + " |      " + str(temp) + "      |   " + str(state) + "   | " + unicodedata.normalize('NFKD', name).encode('ascii','ignore'))
