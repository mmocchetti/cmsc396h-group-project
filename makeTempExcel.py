import datetime
import mysql.connector
import mysql_user_config
import unicodedata	
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py

# Gets a list of all the data about all businesses
def get_list_of_business(cursor):
	query = ("SELECT id, business_id, stars, date FROM review LIMIT 100")	# For testing: Limit the amount of data read
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

line = plt.figure()
x_values = []
y_values = []
nReviews = 0

sys.stdout.write("Progress: [")

for individual_business in business_list:
	query = ("SELECT state FROM res_business WHERE (id='" + individual_business[1] +"')")
	cursor.execute(query)

	for state in cursor:

		query = ("SELECT temp FROM weather WHERE (state='" + state[0] + "') AND (myDate='" + individual_business[3] + "')")
		weather_cursor.execute(query)

		for temp in weather_cursor:
			#plt.scatter(individual_business[2], temp, "x")
			x_values.append(individual_business[2])
			y_values.append(temp)

			nReviews += 1
			if nReviews % 10000 == 0:
				sys.stdout.write('#')

print "]"
print safe_str_convert(nReviews) + " reviews have been processed!"
print "All Data has been uploaded!"

fig = plt.gcf()
#plot_url = py.plot_mpl(line, filename='mplTempScatterPlot')
x_values = np.sort(x_values).flatten()
plt.scatter(x_values, y_values, marker='x', color='blue')
fig.savefig("tempScatterPlot.png")

print "Scatter Plot has been Created!"
