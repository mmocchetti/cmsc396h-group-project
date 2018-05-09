import datetime
import mysql.connector
import mysql_user_config
import unicodedata	
import os
import sys
import xlsxwriter

# Gets a list of all the data about all businesses
def get_list_of_business(cursor):
	query = ("SELECT id, business_id, stars, date FROM review LIMIT 50000")	# For testing: Limit the amount of data read
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
workbook = xlsxwriter.Workbook('weatherData.xlsx')

# Adds a sheet for each type of weather
ws_fog = workbook.add_worksheet('Fog')
ws_rain = workbook.add_worksheet('Rain')
ws_snow = workbook.add_worksheet('Snow')
ws_hail = workbook.add_worksheet('Hail')
ws_thunder = workbook.add_worksheet('Thunder')
ws_tornado = workbook.add_worksheet('Tornado')

row = 0

# Arrays for the star count for each type of weather
arr_fog = [0,0,0,0,0]
arr_rain = [0,0,0,0,0]
arr_snow = [0,0,0,0,0]
arr_hail = [0,0,0,0,0]
arr_thunder = [0,0,0,0,0]
arr_tornado = [0,0,0,0,0]

sys.stdout.write("Progress: [")

# Adds data for each type of weather
for individual_business in business_list:
	query = ("SELECT id, name, state FROM res_business WHERE (id='" + individual_business[1] +"')")
	cursor.execute(query)

	for id, name, state in cursor:

		query = ("SELECT state, myDate, temp, frshtt FROM weather WHERE (state='" + str(state) + "') AND (myDate='" + individual_business[3] + "')")
		weather_cursor.execute(query)

		for state, myDate, temp, frshtt in weather_cursor:
			curr_frshtt = list(frshtt)
			curr_ratingIndex = int(individual_business[2]) - 1
			
			if curr_frshtt[0] == u'1':		# Fog
				arr_fog[curr_ratingIndex] += 1

			if curr_frshtt[1] == u'1':		# Rain or Drizzle
				arr_rain[curr_ratingIndex] += 1

			if curr_frshtt[2] == u'1': 	# Snow or Ice Pellets
				arr_snow[curr_ratingIndex] += 1

			if curr_frshtt[3] == u'1': 	# Hail
				arr_hail[curr_ratingIndex] += 1

			if curr_frshtt[4] == u'1': 	# Thunder
				arr_thunder[curr_ratingIndex] += 1

			if curr_frshtt[5] == u'1': 	# Tornado or Funnel Cloud
				arr_tornado[curr_ratingIndex] += 1

			row += 1
			if row % 100 == 0:
				sys.stdout.write('#')

# Adds all data to their respective worksheet
for x in range(0,5):
	ws_fog.write(x, 0, x+1)
	ws_fog.write(x, 1, arr_fog[x])
	
	ws_rain.write(x, 0, x+1)
	ws_rain.write(x, 1, arr_rain[x])
	
	ws_snow.write(x, 0, x+1)
	ws_snow.write(x, 1, arr_snow[x])
	
	ws_hail.write(x, 0, x+1)
	ws_hail.write(x, 1, arr_hail[x])
	
	ws_thunder.write(x, 0, x+1)
	ws_thunder.write(x, 1, arr_thunder[x])
	
	ws_tornado.write(x, 0, x+1)
	ws_tornado.write(x, 1, arr_tornado[x])
	
print "]"
print "All Data has been uploaded to the excel file!"

# Creates the Column graph charts
chart_fog = workbook.add_chart({'type': 'column'})
chart_rain = workbook.add_chart({'type': 'column'})
chart_snow = workbook.add_chart({'type': 'column'})
chart_hail = workbook.add_chart({'type': 'column'})
chart_thunder = workbook.add_chart({'type': 'column'})
chart_tornado = workbook.add_chart({'type': 'column'})

# Sets Axis' for each of the weather type graphs
# Fog
chart_fog.add_series({
    'name': '',
    'categories': '=Fog!$A$1:$A$5',
    'values': '=Fog!$B$1:$B$5',
})
chart_fog.set_title ({'name': 'Fog vs. Star Rating'})
chart_fog.set_x_axis({'name': 'Star Rating'})
chart_fog.set_y_axis({'name': 'Fog'})

# Rain
chart_rain.add_series({
    'name': '',
    'categories': '=Rain!$A$1:$A$5',
    'values': '=Rain!$B$1:$B$5',
})
chart_rain.set_title ({'name': 'Rain vs. Star Rating'})
chart_rain.set_x_axis({'name': 'Star Rating'})
chart_rain.set_y_axis({'name': 'Rain'})

# Snow
chart_snow.add_series({
    'name': '',
    'categories': '=Snow!$A$1:$A$5',
    'values': '=Snow!$B$1:$B$5',
})
chart_snow.set_title ({'name': 'Snow vs. Star Rating'})
chart_snow.set_x_axis({'name': 'Star Rating'})
chart_snow.set_y_axis({'name': 'Snow'})

# Hail
chart_hail.add_series({
    'name': '',
    'categories': '=Hail!$A$1:$A$5',
    'values': '=Hail!$B$1:$B$5',
})
chart_hail.set_title ({'name': 'Hail vs. Star Rating'})
chart_hail.set_x_axis({'name': 'Star Rating'})
chart_hail.set_y_axis({'name': 'Hail'})

# Thunder
chart_thunder.add_series({
    'name': '',
    'categories': '=Thunder!$A$1:$A$5',
    'values': '=Thunder!$B$1:$B$5',
})
chart_thunder.set_title ({'name': 'Thunder vs. Star Rating'})
chart_thunder.set_x_axis({'name': 'Star Rating'})
chart_thunder.set_y_axis({'name': 'Thunder'})

# Tornado
chart_tornado.add_series({
    'name': '',
    'categories': '=Tornado!$A$1:$A$5',
    'values': '=Tornado!$B$1:$B$5',
})
chart_tornado.set_title ({'name': 'Tornado vs. Star Rating'})
chart_tornado.set_x_axis({'name': 'Star Rating'})
chart_tornado.set_y_axis({'name': 'Tornado'})

# Sets the style for each of the charts
chart_fog.set_style(2)
chart_rain.set_style(2)
chart_snow.set_style(2)
chart_hail.set_style(2)
chart_thunder.set_style(2)
chart_tornado.set_style(2)

# Inserts all the charts into their respective sheet
ws_fog.insert_chart('D2', chart_fog, {'x_offset': 25, 'y_offset': 10})
ws_rain.insert_chart('D2', chart_rain, {'x_offset': 25, 'y_offset': 10})
ws_snow.insert_chart('D2', chart_snow, {'x_offset': 25, 'y_offset': 10})
ws_hail.insert_chart('D2', chart_hail, {'x_offset': 25, 'y_offset': 10})
ws_thunder.insert_chart('D2', chart_thunder, {'x_offset': 25, 'y_offset': 10})
ws_tornado.insert_chart('D2', chart_tornado, {'x_offset': 25, 'y_offset': 10})

print "All Graphs Made"

workbook.close()