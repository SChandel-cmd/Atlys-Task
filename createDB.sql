create database if not exists `weather`;

use `weather`;

CREATE TABLE if not exists `daily_weather_data` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    city VARCHAR(100) NOT NULL,
    sunrise TIME,
    sunset TIME,
    moonrise TIME,
    moonset TIME,
    moon_phase VARCHAR(50),
    moon_illumination INT,
    mintemp DECIMAL(5, 2),
    maxtemp DECIMAL(5, 2),
    avgtemp DECIMAL(5, 2),
    totalsnow DECIMAL(5, 2),
    sunhour DECIMAL(5, 2),
    uv_index INT,
    UNIQUE KEY (date, city)

);

CREATE TABLE if not exists `hourly_weather_data`(
    id SERIAL PRIMARY KEY,
    daily_id int,
    time TIME,
    temperature DECIMAL(5, 2),
    wind_speed DECIMAL(5, 2),
    wind_degree INT,
    weather_code INT,
    weather_description VARCHAR(100),
    humidity INT,
    visibility INT,
    pressure INT,
    foreign key (daily_id) references daily_weather_data(id)
);

CREATE INDEX idx_daily_min_temp ON daily_weather_data (city, mintemp);

CREATE INDEX idx_daily_max_temp ON daily_weather_data (city, maxtemp);

CREATE INDEX idx_daily_sunset ON daily_weather_data (city, sunset);

CREATE INDEX idx_daily_sunrise ON daily_weather_data (city, sunrise);

CREATE INDEX idx_hourly_temp ON hourly_weather_data (daily_id, temperature);

