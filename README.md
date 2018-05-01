# cmsc396h-group-project

In order to get the program weather_console.py working you need a few things:
1. a file named 'mysql_user_config' with the variables user, password, database, and host all equal to what you would use to log into your msql server
2. you need mysql-connector installed for your python
3. you need to have your mysql server running
4. you need to have python2.7.14 running

To get the uploadData.py script working do this:
1. Open mysql top level
2. In the top level run "create database yelp_db;"
3. Then run "show databases;" and make sure that yelp_db is there
4. Then leave the mysql top level
5. Go to your mysql folder (Mac's need to be in bin)
6. Inside that folder run "mysql -u root -p yelp_db < /path/to/yelp_db.sql"

Then you can run the script by running the command
$ /path/to/python2.7.14/python /path/to/path/script/weather_console.py
if your on windows
$ /path/to/python2.7.14/python.exe /path/to/path/script/weather_console.py

Lastly, before you run weather_console.py you should run upload_data.py

Note: Check in-code file extensions given to change based off of operating systems
  Windows: Make sure it is "\\wordsHere\\"
  Mac/Linux: Make sure it is "wordsHere/"
