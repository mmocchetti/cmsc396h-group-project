import datetime
import mysql_user_config
import mysql.connector
import sys
import time
import unicodedata
import temp_analysis

start_timer = 0

'''
Safely converts values to strings
'''
def safe_str_convert(convert_val):
    if type(convert_val) == unicode:
        return unicodedata.normalize('NFKD', convert_val).encode('ascii','ignore')
    elif type(convert_val) == int:
        return str(convert_val)
    elif type(convert_val) == datetime.datetime:
        return str(convert_val)
    else:
        return "None"
        
def get_list_of_business():
    cnx = mysql.connector.connect(user=mysql_user_config.user, password=mysql_user_config.password, host=mysql_user_config.host, database="yelp_db")
    cursor = cnx.cursor()

    
    max_rows = raw_input("Enter max number of review to anaylize:\n");  

    global start_timer 
    start_timer = time.time()
    
    #query = ("SELECT review.id, review.business_id, review.stars, review.date, res_business.name, res_business.state FROM review INNER JOIN res_business ON business_id = res_business.id LIMIT " + max_rows)
    query = ("SELECT id, business_id, stars, date FROM review LIMIT " + max_rows)
    cursor.execute(query)

    business_list = list()

    #for id,business_id, stars, date ,name, state in cursor:
    for id,business_id, stars, date in cursor:
        individual_business = list()
        
        '''
        individual_business = {
            'review_id':      safe_str_convert(id),             # 0
            'business_id':    safe_str_convert(business_id),    # 1
            'star_rating':    safe_str_convert(stars),          # 2
            'date_of_review': safe_str_convert(date)            # 3
            'business_name':  safe_str_convert(name),           # 4
            'business_state': safe_str_convert(state)           # 5
        }
        '''
        
        individual_business.append(safe_str_convert(id))
        individual_business.append(safe_str_convert(business_id))
        individual_business.append(safe_str_convert(stars))
        individual_business.append(safe_str_convert(date))
        #individual_business.append(safe_str_convert(name))
        #individual_business.append(safe_str_convert(state))
        
        business_list.append(individual_business)
    
    cursor.close()
    cnx.close()
    
    return business_list
    
    
def anaylize_temperature():
    cnx = mysql.connector.connect(user=mysql_user_config.user, password=mysql_user_config.password, host=mysql_user_config.host, database="yelp_weather_db")
    cursor = cnx.cursor()
        
    cnx2 = mysql.connector.connect(user=mysql_user_config.user, password=mysql_user_config.password, host=mysql_user_config.host, database="yelp_db")
    cursor2 = cnx2.cursor()
        
    business_list = get_list_of_business()
        
    star_counter = [0,0,0,0,0,0]
    counter = 0

    temp_analysis_holder = temp_analysis.TempAnalysis()

    print("Review ID:             | Business ID:           | Date of Review      | * | Temperature: | State: |")
    print("-----------------------+------------------------+---------------------+---+--------------+--------+------------------------------")
        
    for individual_business in business_list:
        query = ("SELECT id, name, state FROM res_business WHERE (id='" + individual_business[1] +"')")
        cursor2.execute(query)
        
        for id, name, state in cursor2:
            query = ("SELECT myDate, temp FROM weather WHERE (state='" + str(state) + "') AND (myDate='" + individual_business[3] + "')")
            cursor.execute(query)

            for myDate, temp in cursor:
                #print(individual_business[0] + " | " + individual_business[1] + " | " + individual_business[3] + " | " + individual_business[2] + " |      " + str(temp) + "      |   " + str(state) + "   | " + str(name))
                
                counter = counter + 1
                
                if counter % 100 == 0:
                    print("-----------------------+------------------------+---------------------+---+--------------+--------+------------------------------")
                    print(str(counter) + " rows inputed!!!")
                    print("-----------------------+------------------------+---------------------+---+--------------+--------+------------------------------")
                
                if int(individual_business[2]) == 0:
                    star_counter[0] = star_counter[0] + 1
                if int(individual_business[2]) == 1:
                    star_counter[1] = star_counter[1] + 1
                if int(individual_business[2]) == 2:
                    star_counter[2] = star_counter[2] + 1
                if int(individual_business[2]) == 3:
                    star_counter[3] = star_counter[3] + 1
                if int(individual_business[2]) == 4:
                    star_counter[4] = star_counter[4] + 1 
                if int(individual_business[2]) == 5:
                    star_counter[5] = star_counter[5] + 1
                    
                temp_analysis_holder.add_rating(individual_business[2], temp)
                        
               
    end_timer = time.time()
    global start_timer
    
    print("\n=================================================================================================================================\n")
         
    print("Overall star breakdown: Anaylisis Speed: " + str(round((end_timer - start_timer),2)) + " seconds")
    print("-------------------------")  
    print("Count: " + str(counter))

    if star_counter[0] == 0:
        print("0 Stars: 0.00%")
    else:
        print("0 Stars: " + str(round((star_counter[0] / (counter * 1.0)), 4) * 100) + "%")
       
    if star_counter[1] == 0:
        print("1 Stars: 0.00%")
    else:
        print("1 Stars: " + str(round((star_counter[1] / (counter * 1.0)), 4) * 100) + "%")
        
    if star_counter[2] == 0:
        print("2 Stars: 0.00%")
    else:
        print("2 Stars: " + str(round((star_counter[2] / (counter * 1.0)), 4) * 100) + "%")
        
    if star_counter[3] == 0:
        print("3 Stars: 0.00%")
    else:
        print("3 Stars: " + str(round((star_counter[3] / (counter * 1.0)), 4) * 100) + "%")
        
    if star_counter[4] == 0:
        print("4 Stars: 0.00%")
    else:
        print("4 Stars: " + str(round((star_counter[4] / (counter * 1.0)), 4) * 100) + "%")
        
    if star_counter[5] == 0:
        print("5 Stars: 0.00%")
    else:
        print("5 Stars: " + str(round((star_counter[5] / (counter * 1.0)), 4) * 100) + "%")
        
    print("\n\n")

    print(str(temp_analysis_holder))
    
def anaylitic_percipitation():
    #start_timer = time.time()

    cnx = mysql.connector.connect(user=mysql_user_config.user, password=mysql_user_config.password, host=mysql_user_config.host, database="yelp_weather_db")
    cursor = cnx.cursor()
    
    cnx2 = mysql.connector.connect(user=mysql_user_config.user, password=mysql_user_config.password, host=mysql_user_config.host, database="yelp_db")
    cursor2 = cnx2.cursor()
        
    business_list = get_list_of_business()
        
    star_counter = [0,0,0,0,0,0]
    counter = 0

    frshtt_analysis_holder = temp_analysis.FRSHTTAnalysis()

    print("Review ID:             | Business ID:           | Date of Review      | * | Temperature: | State: |")
    print("-----------------------+------------------------+---------------------+---+--------------+--------+------------------------------")
        
        
    
    for individual_business in business_list:
        query = ("SELECT id, name, state FROM res_business WHERE (id='" + individual_business[1] +"')")
        cursor2.execute(query)
        
        for id, name, state in cursor2:
            query = ("SELECT myDate, frshtt FROM weather WHERE (state='" + str(state) + "') AND (myDate='" + individual_business[3] + "')")
            cursor.execute(query)

            for myDate, frshtt in cursor:
                #print(individual_business[0] + " | " + individual_business[1] + " | " + individual_business[3] + " | " + individual_business[2] + " |      " + str(frshtt) + "      |   " + str(state) + "   | " + str(name))
                
                counter = counter + 1
                
                if counter % 100 == 0:
                    print("-----------------------+------------------------+---------------------+---+--------------+--------+------------------------------")
                    print(str(counter) + " rows inputed!!!")
                    print("-----------------------+------------------------+---------------------+---+--------------+--------+------------------------------")
                
                if int(individual_business[2]) == 0:
                    star_counter[0] = star_counter[0] + 1
                if int(individual_business[2]) == 1:
                    star_counter[1] = star_counter[1] + 1
                if int(individual_business[2]) == 2:
                    star_counter[2] = star_counter[2] + 1
                if int(individual_business[2]) == 3:
                    star_counter[3] = star_counter[3] + 1
                if int(individual_business[2]) == 4:
                    star_counter[4] = star_counter[4] + 1 
                if int(individual_business[2]) == 5:
                    star_counter[5] = star_counter[5] + 1
                    
                frshtt_analysis_holder.add_rating(individual_business[2], frshtt)
                        
               
    end_timer = time.time()
    global start_timer
    
    print("\n=================================================================================================================================\n")
         
    print("Overall star breakdown: Anaylisis Speed: " + str(round((end_timer - start_timer),2)) + " seconds")
    print("-------------------------")  
    print("Count: " + str(counter))

    if star_counter[0] == 0:
        print("0 Stars: 0.00%")
    else:
        print("0 Stars: " + str(round((star_counter[0] / (counter * 1.0)), 4) * 100) + "%")
       
    if star_counter[1] == 0:
        print("1 Stars: 0.00%")
    else:
        print("1 Stars: " + str(round((star_counter[1] / (counter * 1.0)), 4) * 100) + "%")
        
    if star_counter[2] == 0:
        print("2 Stars: 0.00%")
    else:
        print("2 Stars: " + str(round((star_counter[2] / (counter * 1.0)), 4) * 100) + "%")
        
    if star_counter[3] == 0:
        print("3 Stars: 0.00%")
    else:
        print("3 Stars: " + str(round((star_counter[3] / (counter * 1.0)), 4) * 100) + "%")
        
    if star_counter[4] == 0:
        print("4 Stars: 0.00%")
    else:
        print("4 Stars: " + str(round((star_counter[4] / (counter * 1.0)), 4) * 100) + "%")
        
    if star_counter[5] == 0:
        print("5 Stars: 0.00%")
    else:
        print("5 Stars: " + str(round((star_counter[5] / (counter * 1.0)), 4) * 100) + "%")
        
    print("\n\n")

    print(str(frshtt_analysis_holder))
    
    
def chose_which_anaylitics():
    anaylitic_choice = raw_input("Which anaylisis to run:\n1. Temperature (t)\n2. Percipitation(p)\n")
    
    print("")
    
    if anaylitic_choice.lower() == 'p':
        anaylitic_percipitation()
    else:
        anaylize_temperature()
       
'''
Start of program
'''

chose_which_anaylitics()
