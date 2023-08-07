--Create Database
CREATE TABLE Public."bike_share"(
	ride_id VARCHAR(100),
	rideable_type VARCHAR(50),
	started_at timestamp,
	ended_at timestamp,
	start_station_name VARCHAR(100),
	start_station_id VARCHAR(100),
	end_station_name VARCHAR(100),
	end_station_id VARCHAR(100),
	start_lat float,
	start_lng float,
	end_lat float,
	end_lng float,
	member_casual VARCHAR(50)
	)

--Import data to database from CSV file
COPY Public."bike_share" 
FROM 'C:\Users\Huawei\Downloads\Bike-Share data\Data\cylic\bike_share.csv' DELIMITER ',' CSV HEADER;

SELECT * 
FROM bike_share
LIMIT 50

-- Annual Member have trip 61% more than casual ride 39%
SELECT member_casual, COUNT(*) total
FROM bike_share
GROUP BY member_casual


--Different Time perTrip
SELECT 
	DISTINCT (member_casual),
	AVG(EXTRACT(HOUR from ended_at)*60 + EXTRACT(MINUTE from ended_at)-
	(EXTRACT(HOUR from started_at)*60)+EXTRACT(MINUTE from started_at)
	)*60 AS avg_time_Pertrip,
	max(EXTRACT(HOUR from ended_at)*60 + EXTRACT(MINUTE from ended_at)-
	(EXTRACT(HOUR from started_at)*60)+EXTRACT(MINUTE from started_at)
	) AS max_time_Pertrip
FROM bike_share
GROUP BY member_casual
	
-- Average, Minimun and Maximum Time per trip with Cyclistic Bike Share
-- Note: Terdapat filter bahwa minimum data waktu perperjalanan adalah menit,
-- hal ini digunakan agar data lebih relevant, namun tidak mempengaruhi data secara keseluruhan (Rata-rata waktu tiap perjalanan tidak berubah significant)
SELECT 
	member_casual,
	AVG(time_ride),
	MIN(time_ride),
	MAX(time_ride)
FROM
	(SELECT 
		ride_id,
	 	member_casual,
		avg(ended_at-started_at) time_ride
	FROM bike_share
	WHERE ended_at > started_at
	GROUP BY ride_id, member_casual
	HAVING 
	 avg(ended_at-started_at) < '1 day 15:09:21' AND 
	 avg(ended_at-started_at) > '00:01:00'
	) as time_data
GROUP BY member_casual


--Top 5 Start Station Annual Member
SELECT member_casual, start_station_name, count(*) total
FROM bike_share
WHERE member_casual = 'annual_member'
GROUP BY member_casual, start_station_name
ORDER BY total DESC
limit 5
	
--Top 5 Start Station Casual Ride
SELECT member_casual, start_station_name, count(*) total
FROM bike_share
WHERE member_casual = 'casual_ride'
GROUP BY member_casual, start_station_name
ORDER BY total DESC
limit 5
	
--Total Trip perWeek
SELECT DISTINCT(member_casual), EXTRACT(ISODOW from started_at) week, count(*) total
FROM bike_share
GROUP BY week, member_casual
ORDER BY member_casual ASC
						  
--Different Trip PerMonth
SELECT DISTINCT(member_casual), EXTRACT(MONTH from started_at) Month_total, count(*) total
FROM bike_share
GROUP BY Month_total, member_casual
ORDER BY member_casual ASC
	
--Different Trip PerDay
select member_casual, count(*), extract(hour from started_at) as hours 
from bike_share
group by member_casual, extract(hour from started_at) 
ORDER BY hours

--Top 10 Start-End Station for Annual Member before 11.59 AM
SELECT CONCAT(start_station_name,'-', end_station_name) as station_trip, count(*) total_trip
from bike_share
WHERE member_casual = 'annual_member' AND EXTRACT(hour from started_at) > 12
group by station_trip
ORDER BY total_trip DESC
LIMIT 10
	
--Top 10 Start-End Station for Annual Member after 12.00 AM	
SELECT CONCAT(start_station_name,'-', end_station_name) as station_trip, count(*) total_trip
from bike_share
WHERE member_casual = 'annual_member' AND EXTRACT(hour from started_at) > 12
group by station_trip
ORDER BY total_trip DESC
LIMIT 10