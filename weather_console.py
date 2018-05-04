import datetime
import mysql_user_config
import mysql.connector
import sys
import unicodedata

class TempHolder:
    range_start = 0
    range_end = 0
    
    star_count_lst = [0,0,0,0,0,0]
    counter = 0
    
    def __init__(self, in_range_start, in_range_end):
        self.range_start = in_range_start
        self.range_end = in_range_end
        self.counter = 0
        self.star_count_lst = [0,0,0,0,0,0]
        
    def is_in_temp_range(self, temp):
        #print("test0: " + str(temp) + " | " + str(self.range_start) + " | " + str(self.range_end))
        if self.range_start <= temp and temp < self.range_end:
            return True
        else:
            return False
            
    def add_rating(self, rating):
        #print("test1")
        if int(rating) == 0:
            self.star_count_lst[0] += 1
        if int(rating) == 1:
            self.star_count_lst[1] += 1
        if int(rating) == 2:
            self.star_count_lst[2] += 1
        if int(rating) == 3:
            self.star_count_lst[3] += 1
        if int(rating) == 4:
            self.star_count_lst[4] += 1
        if int(rating) == 5:
            self.star_count_lst[5] += 1
        
        self.counter += 1
        
    def __str__(self):
        '''
        if self.range_start == 0:
            return "Temp: " + str(self.range_start) + "-" + str(self.range_end) + "    Total: " + str(self.counter) + " | " + str(self.star_count_lst)
        if self.range_start >= 10 and self.range_start <= 80:
            return "Temp: " + str(self.range_start) + "-" + str(self.range_end) + "   Total: " + str(self.counter) + " | " + str(self.star_count_lst)
        if self.range_start == 90:
            return "Temp: " + str(self.range_start) + "-" + str(self.range_end) + "  Total: " + str(self.counter) + " | " + str(self.star_count_lst)
        
        return "Temp: " + str(self.range_start) + "-" + str(self.range_end) + " Total: " + str(self.counter) + " | " + str(self.star_count_lst)
        '''
        
        return_str = ""
        
        return_str += "Temp: " + str(self.range_start) + "-" + str(self.range_end) + "\n"
        return_str += "Count: " + str(self.counter) + "\n"

        if self.star_count_lst[0] == 0:
            return_str += "0 Stars: 0.00%\n" 
        else:
            return_str += "0 Stars: " + str(round((self.star_count_lst[0] / (self.counter * 1.0)), 4) * 100) + "%\n"
           
        if self.star_count_lst[1] == 0:
            return_str += "1 Stars: 0.00%\n"
        else:
            return_str += "1 Stars: " + str(round((self.star_count_lst[1] / (self.counter * 1.0)), 4) * 100) + "%\n"
            
        if self.star_count_lst[2] == 0:
            return_str += "2 Stars: 0.00%\n"
        else:
            return_str += "2 Stars: " + str(round((self.star_count_lst[2] / (self.counter * 1.0)), 4) * 100) + "%\n"
            
        if self.star_count_lst[3] == 0:
            return_str += "3 Stars: 0.00%\n"
        else:
            return_str += "3 Stars: " + str(round((self.star_count_lst[3] / (self.counter * 1.0)), 4) * 100) + "%\n"
            
        if self.star_count_lst[4] == 0:
            return_str += "4 Stars: 0.00%\n"
        else:
            return_str += "4 Stars: " + str(round((self.star_count_lst[4] / (self.counter * 1.0)), 4) * 100) + "%\n"
            
        if self.star_count_lst[5] == 0:
            return_str += "5 Stars: 0.00%\n"
        else:
            return_str += "5 Stars: " + str(round((self.star_count_lst[5] / (self.counter * 1.0)), 4) * 100) + "%\n"
        
        return return_str
        
class TempAnalysis:
    temp_holder_lst = list()
    
    def __init__(self):
        temp_counter = 0
        
        while temp_counter < 110:
            self.temp_holder_lst.append(TempHolder(temp_counter, temp_counter + 10))
            temp_counter += 10
    
    def add_rating(self, rating, temp):
        for temp_holder in self.temp_holder_lst:
            if temp_holder.is_in_temp_range(temp):
                temp_holder.add_rating(rating)
                return True
        
        return False
        
    def __str__(self):
        return_str = "Breakdown by Temperature:\n"
        return_str += "-------------------------\n"
        
        for temp_holder in self.temp_holder_lst:
            return_str += str(temp_holder) + "\n"
    
        return return_str

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
    
star_counter = [0,0,0,0,0,0]
counter = 0

temp_analysis = TempAnalysis()

print("Review ID:             | Business ID:           | Date of Review      | * | Temperature: | State: |")
print("-----------------------+------------------------+---------------------+---+--------------+--------+------------------------------")
    
for individual_business in business_list:
    query = ("SELECT id, name, state FROM res_business WHERE (id='" + individual_business[1] +"')")
    cursor.execute(query)
    
    for id, name, state in cursor:

        query = ("SELECT state, myDate, temp FROM weather WHERE (state='" + str(state) + "') AND (myDate='" + individual_business[3] + "')")
        weather_cursor.execute(query)

        for state, myDate, temp in weather_cursor:
            #print(individual_business[0] + " | " + unicodedata.normalize('NFKD', id).encode('ascii','ignore') + " | " + individual_business[3] + " | " + individual_business[2] + " |      " + str(temp) + "      |   " + str(state) + "   | " + unicodedata.normalize('NFKD', name).encode('ascii','ignore'))
            
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
                
            temp_analysis.add_rating(individual_business[2], temp)
                    
           
print("\n====================================================================================================================================\n")
     
print("Overall star breakdown:")
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

print(str(temp_analysis))
            
            
