import datetime
import mysql_user_config
import mysql.connector
import sys
import unicodedata

def safe_str_convert(convert_val):
    if type(convert_val) == unicode:
        return unicodedata.normalize('NFKD', convert_val).encode('ascii','ignore')
    elif type(convert_val) == int:
        return str(convert_val)
    elif type(convert_val) == datetime.datetime:
        return str(convert_val)
    else:
        return "None"
		
def get_list_of_business(max_rows, cursor):
    query = ("SELECT id, business_id, stars, date FROM review LIMIT " + max_rows)
    cursor.execute(query)

    business_list = list()

    for id,business_id, stars, date in cursor:
        individual_business = list()
        
        individual_business.append(safe_str_convert(id))
        individual_business.append(safe_str_convert(business_id))
        individual_business.append(safe_str_convert(stars))
        individual_business.append(safe_str_convert(date))
        
        business_list.append(individual_business)
    
    return business_list
    
cnx = mysql.connector.connect(user=mysql_user_config.user, password=mysql_user_config.password, host=mysql_user_config.host, database="yelp_db")
cursor = cnx.cursor()

weather_cnx    = mysql.connector.connect(user=mysql_user_config.user, password=mysql_user_config.password, host=mysql_user_config.host, database="yelp_weather_db")
weather_cursor = weather_cnx.cursor()
	
max_rows = raw_input("Enter maximum amount of rows to return:\n");	
	
business_list = get_list_of_business(max_rows, cursor)
    
print("Review ID:             | Business ID:           | Date of Review      | * | Temperature: | State: |")
print("-----------------------+------------------------+---------------------+---+--------------+--------+------------------------------")
	
for individual_business in business_list:
    query = ("SELECT id, name, state FROM business WHERE (id='" + individual_business[1] +"')")
    cursor.execute(query)
    
    for id, name, state in cursor:
		#print(individual_business[0] + " | " + str(id) + " | " + individual_business[3] + " | " + individual_business[2] + " |   " + str(state) + "   | " + str(name))

		query = ("SELECT state, myDate, temp FROM weather WHERE (state='" + str(state) + "') AND (myDate='" + individual_business[3] + "')")
		weather_cursor.execute(query)

		for state, myDate, temp in weather_cursor:
			print(individual_business[0] + " | " + unicodedata.normalize('NFKD', id).encode('ascii','ignore') + " | " + individual_business[3] + " | " + individual_business[2] + " |      " + str(temp) + "      |   " + str(state) + "   | " + unicodedata.normalize('NFKD', name).encode('ascii','ignore'))
            

            
