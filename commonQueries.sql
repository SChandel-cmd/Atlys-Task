-- Daily Min Temp (by city)
SELECT city, date, mintemp
FROM daily_weather_data
WHERE city = 'Delhi'
ORDER BY mintemp
LIMIT 1;

-- Daily Max Temp (by city)
SELECT city, date, maxtemp
FROM daily_weather_data
WHERE city = 'Delhi'
ORDER BY maxtemp DESC
LIMIT 1;

-- Daily Sunset (by city)
SELECT city, date, sunset
FROM daily_weather_data
WHERE city = 'Delhi';

-- Daily Sunrise (by city)
SELECT city, date, sunrise
FROM daily_weather_data
WHERE city = 'Delhi';

-- Hourly Temp (by city)
SELECT d.city, d.date, h.time, h.temperature
FROM hourly_weather_data h
JOIN daily_weather_data d ON h.daily_id = d.id
WHERE d.city = 'Delhi'
ORDER BY d.date, h.time;

