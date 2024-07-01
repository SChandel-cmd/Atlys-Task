import requests
import json
import pymysql
from datetime import datetime, timedelta
from configparser import ConfigParser

API_KEY = 'e53790cf314e3a3d61d2cb30c8d465d0'

cities = ["Delhi", "Mumbai", "Bangalore", "Kolkata", "Chennai", "Hyderabad", "Pune"]

start_date = datetime.strptime("2010-01-01", "%Y-%m-%d")
end_date = datetime.now()

def config(filename='DBConnection.properties'):
	config = ConfigParser()
	config.read(filename)
	host = config.get('mysql', 'host')
	database = config.get('mysql', 'database')
	user = config.get('mysql', 'user')
	password = config.get('mysql', 'password')
	return {'host': host, 'database': database, 'user': user, 'password': password}
    
def insert_daily_weather_data(cursor, data):
    sql = """
    INSERT INTO daily_weather_data (date, city, sunrise, sunset, moonrise, moonset, moon_phase, moon_illumination, mintemp, maxtemp, avgtemp, totalsnow, sunhour, uv_index)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (
        data["date"], data["city"], data["sunrise"], data["sunset"], data["moonrise"],
        data["moonset"], data["moon_phase"], data["moon_illumination"], data["mintemp"],
        data["maxtemp"], data["avgtemp"], data["totalsnow"], data["sunhour"], data["uv_index"]
    ))
    return cursor.lastrowid

def insert_hourly_weather_data(cursor, daily_id, hourly_data):
    sql = """
    INSERT INTO hourly_weather_data (daily_id, time, temperature, wind_speed, wind_degree, weather_code, humidity, visibility, pressure)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for hour in hourly_data:
        cursor.execute(sql, (
            daily_id, hour.get("time"), hour.get("temperature"), hour.get("wind_speed"),
            hour.get("wind_degree"), hour.get("weather_code"),
            hour.get("humidity"), hour.get("visibility"), hour.get("pressure")
        ))

def time_converter(time_str):
	try:
		time_obj = datetime.strptime(time_str, '%I:%M %p')
		return time_obj.strftime('%H:%M:%S')
	except Exception:
		return None

params = config()
conn = pymysql.connect(host=params['host'], user=params['user'], password=params['password'], database=params['database'],cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()

date_ranges = []
current_start = start_date

while current_start < end_date:
	current_end = min(current_start + timedelta(days=59), end_date)
	date_ranges.append((current_start, current_end))
	current_start = current_end + timedelta(days=1)
        
try:
	for city in cities:
		url = f"https://api.weatherstack.com/historical?access_key={API_KEY}"
		for start, end in date_ranges:
			querystring = {
			    "query": city,
			    "historical_date_start": start.strftime("%Y-%m-%d"),
			    "historical_date_end": end.strftime("%Y-%m-%d"),
			    "hourly": 1
			}
			response = requests.get(url, params=querystring)
			data = response.json()
			
			if 'historical' in data:
			    historical_data = data['historical']
			for date in historical_data.keys():
			    date_data = historical_data[date]
			    
			    daily_data = {
				"date": date,
				"city": city,
				"sunrise": time_converter(date_data["astro"].get("sunrise")),
				"sunset": time_converter(date_data["astro"].get("sunset")),
				"moonrise": time_converter(date_data["astro"].get("moonrise")),
				"moonset": time_converter(date_data["astro"].get("moonset")),
				"moon_phase": date_data["astro"].get("moon_phase"),
				"moon_illumination": date_data["astro"].get("moon_illumination"),
				"mintemp": date_data.get("mintemp"),
				"maxtemp": date_data.get("maxtemp"),
				"avgtemp": date_data.get("avgtemp"),
				"totalsnow": date_data.get("totalsnow"),
				"sunhour": date_data.get("sunhour"),
				"uv_index": date_data.get("uv_index")
			    }
			    try:
			    	daily_id = insert_daily_weather_data(cursor, daily_data)
			    	hourly_data = date_data.get("hourly", [])
			    	insert_hourly_weather_data(cursor, daily_id, hourly_data)
			    except Exception as err:
			    	print("Error occurred in loading-", err)

	conn.commit()
except Exception as err:
	print("Oops, something went wrong! - ", err)
finally:
	conn.close()
