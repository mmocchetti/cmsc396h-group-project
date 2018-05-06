import datetime
import mysql.connector
import mysql_user_config
import unicodedata	
import os
import sys
import xlsxwriter

# Gets a list of all the data about all businesses
def get_list_of_business(cursor):
	query = ("SELECT id, business_id, stars, date FROM review LIMIT 1000")	# For testing: Limit the amount of data read
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

def safe_str_convert(convert_val):
	if type(convert_val) == unicode:
		return unicodedata.normalize('NFKD', convert_val).encode('ascii','ignore')
	elif type(convert_val) == int:
		return str(convert_val)
	elif type(convert_val) == datetime.datetime:
		return str(convert_val)
	else:
		return "None"

#########################
# Execution Starts Here #
#########################

# NOTE: If this file already exists it will be overwritten

# Setup SQL connector for yelp_db
cnx = mysql.connector.connect(user=mysql_user_config.user, password=mysql_user_config.password, host=mysql_user_config.host, database="yelp_db")
cursor = cnx.cursor()

# Setup SQL connector for yelp_weather_db
weather_cnx = mysql.connector.connect(user=mysql_user_config.user, password=mysql_user_config.password, host=mysql_user_config.host, database="yelp_weather_db")
weather_cursor = weather_cnx.cursor()

# Gets list of all businesses
business_list = get_list_of_business(cursor)

# Sets up xlswriter for the excel file
workbook = xlsxwriter.Workbook('tempData.xlsx')
worksheet = workbook.add_worksheet()#'TempData')
row = 0

sys.stdout.write("Progress: [")

for individual_business in business_list:
	query = ("SELECT id, name, state FROM res_business WHERE (id='" + individual_business[1] +"')")
	cursor.execute(query)

	for id, name, state in cursor:

		query = ("SELECT state, myDate, temp FROM weather WHERE (state='" + str(state) + "') AND (myDate='" + individual_business[3] + "')")
		weather_cursor.execute(query)

		for state, myDate, temp in weather_cursor:
			worksheet.write(row, 0, int(individual_business[2]))
			worksheet.write(row, 1, int(temp))
			row += 1
			sys.stdout.write('#')

print "]"
print "All Data has been uploaded to the excel file!"

# Creates the Scatter Plot
chart1 = workbook.add_chart({'type': 'scatter'})

safe_row = safe_str_convert(row)

chart1.add_series({
    'name': '',
    'categories': '=Sheet1!$A$0:$A$' + safe_row,
    'values': '=Sheet1!$B$0:$B$' + safe_row,
})

chart1.set_title ({'name': 'Temperature vs. Star Rating'})
chart1.set_x_axis({'name': 'Star Rating'})
chart1.set_y_axis({'name': 'Temperature (F)'})

chart1.set_style(2)	# GUESS AND CHECK WITH SMALL DATA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

worksheet.insert_chart('D2', chart1, {'x_offset': 25, 'y_offset': 10})

print "The Scatter Plot Has been Created!"

workbook.close()