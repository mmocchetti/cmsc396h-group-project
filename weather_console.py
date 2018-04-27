import mysql.connector
import sys
import mysql_user_config

cnx = mysql.connector.connect(user=mysql_user_config.user, password=mysql_user_config.password, host=mysql_user_config.host, database=mysql_user_config.database)
cursor = cnx.cursor()

#query = raw_input("Type MySQL query here: ")
#cursor.execute(query)

query = ("SELECT id,business_id,stars,date FROM review LIMIT 100")
cursor.execute(query)

business_list = list()

for id,business_id,stars,date in cursor:
    individual_business = list()
    #print(str(id) + " | " + str(business_id) + " | " + str(stars) + " | " + str(date))
    individual_business.append(str(id))
    individual_business.append(str(business_id))
    individual_business.append(str(stars))
    individual_business.append(str(date))
    
    business_list.append(individual_business)
    
print("Review ID:             | Business ID:           | Date of Review      | * | State: |")
print("-----------------------+------------------------+---------------------+---+--------+---------------------------------------")
    
for individual_business in business_list:
    query = ("SELECT id,name,state FROM business WHERE (id='" + individual_business[1] +"')")
    cursor.execute(query)
    
    for id,name,state in cursor:
        print(individual_business[0] + " | " + str(id) + " | " + individual_business[3] + " | " + individual_business[2] + " |   " + str(state) + "   | " + str(name))

