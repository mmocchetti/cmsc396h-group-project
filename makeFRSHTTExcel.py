#!/usr/bin/env python
import datetime
import mysql.connector
import mysql_user_config
import unicodedata	
import os
import sys
import matplotlib.pyplot as plt
import plotly.plotly as py

# Gets a list of all the data about all businesses
def get_list_of_business(cursor):
	query = ("SELECT id, business_id, stars, date FROM review")# LIMIT 10000")	# For testing: Limit the amount of data read
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

def arrToStr(arr):
	toRet = ""
	for s in arr:
		toRet += str(s) + ", "
	return toRet


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

nReviews = 0

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
	cursor.execute("SELECT state FROM res_business WHERE (id='" + individual_business[1] +"')")

	for state in cursor:
		weather_cursor.execute("SELECT frshtt FROM weather WHERE state='" + state[0] + "' AND myDate='" + individual_business[3] + "'")

		for frshtt in weather_cursor:
			curr_frshtt = list(frshtt[0])
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

			nReviews += 1
			if nReviews % 10000 == 0:
				sys.stdout.write('#')

print "]"
print safe_str_convert(nReviews) + " reviews have been processed!"
print "All Data has been uploaded!"
	
# Makes graph for each of the data
rng = [1,2,3,4,5]
width = 1/1.5
plt.bar(rng, arr_fog, width, color="blue")
fig = plt.gcf()
plot_url = py.plot_mpl(fig, filename='mpl-test-bar.png')
print "Fog:"
print arr_fog
fig.savefig("fog.png")

plt.bar(rng, arr_rain, width, color="blue")
fig = plt.gcf()
plot_url = py.plot_mpl(fig, filename='mpl-test-bar.png')
print "Rain:"
print arr_rain
fig.savefig("rain.png")

plt.bar(rng, arr_snow, width, color="blue")
fig = plt.gcf()
plot_url = py.plot_mpl(fig, filename='mpl-test-bar.png')
print "Snow:"
print arr_snow
fig.savefig("snow.png")

plt.bar(rng, arr_hail, width, color="blue")
fig = plt.gcf()
plot_url = py.plot_mpl(fig, filename='mpl-test-bar.png')
print "Hail:"
print arr_hail
fig.savefig("hail.png")

plt.bar(rng, arr_thunder, width, color="blue")
fig = plt.gcf()
plot_url = py.plot_mpl(fig, filename='mpl-test-bar.png')
print "Thunder:"
print arr_thunder
fig.savefig("thunder.png")

plt.bar(rng, arr_rain, width, color="blue")
fig = plt.gcf()
plot_url = py.plot_mpl(fig, filename='mpl-test-bar.png')
print "Tornado:"
print arr_tornado
fig.savefig("Tornado.png")

# Prints final data to a text file, if it is needed later
data = open("weatherData.txt", "w")
data.write("Fog: ")
data.write(arrToStr(arr_fog) + "\n")
data.write("Rain: ")
data.write(arrToStr(arr_rain) + "\n")
data.write("Snow: ")
data.write(arrToStr(arr_snow) + "\n")
data.write("Hail: ")
data.write(arrToStr(arr_hail) + "\n")
data.write("Thunder: ")
data.write(arrToStr(arr_thunder) + "\n")
data.write("Tornado: ")
data.write(arrToStr(arr_tornado) + "\n")
data.close()

print "All Graphs Made and All Data Collected"
