DROP DATABASE IF EXISTS standing_desk;
CREATE DATABASE standing_desk;


USE standing_desk;
CREATE USER IF NOT EXISTS 'deskController'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON standing_desk.* to "deskController"@"localhost";

CREATE TABLE heights(
    id INT AUTO_INCREMENT PRIMARY KEY,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    start_height INT,
    end_time TIMESTAMP,
    end_height INT
);

CREATE TABLE daily_totals(
    id INT AUTO_INCREMENT PRIMARY KEY,
    height INT,
    total_time TIME,
    day TIMESTAMP
);

CREATE TABLE monthly_avg(
    id INT AUTO_INCREMENT PRIMARY KEY,
    height INT,
    total_time TIME,
    id_of_month ENUM("1","2","3","4","5","6","7","8","9","10","11","12"),
    year INT
);

CREATE TABLE settings(
    id INT AUTO_INCREMENT PRIMARY KEY,
    presetName VARCHAR(50),
    heatmap_steps FLOAT,
    daily_goal TIME,
    standing_height INT,
    sitting_height INT
);

INSERT INTO heights (start_time, start_height) VALUES (CURRENT_TIMESTAMP(), 74);

-- Insert data into the daily_totals table to set limit at when calculating values of past
INSERT INTO daily_totals (height, total_time, day) VALUES (0, '00:00:00', '2024-01-01 00:00:00');

-- Insert data into the monthly_avg table to set limit at when calculating values of past
INSERT INTO monthly_avg (height, total_time, id_of_month, year) VALUES (0, '00:00:00', '1', 2024);


DELIMITER //

-- Save height as start_height in heights
CREATE PROCEDURE saveStartHeight(
    IN height INT
)
BEGIN
	INSERT INTO heights (start_height) VALUES (height);
END //

-- save heigt as end_height and current time as end_time in latest entry of heights 
CREATE PROCEDURE saveEndHeight(
    IN height INT
)
BEGIN
	UPDATE heights SET end_time = CURRENT_TIMESTAMP(), end_height = height ORDER BY id DESC LIMIT 1;
END //

-- get the latest entry of table heights
CREATE PROCEDURE getLatestHeight()
BEGIN
	SELECT * FROM heights ORDER BY id DESC LIMIT 1;
END //

-- Get the latest x entries of table heights
CREATE PROCEDURE getAllHeights(
    IN `lim_val` INT
)
BEGIN
	SELECT * FROM heights ORDER BY id DESC LIMIT lim_val;
END //

-- get all entries of table height of given day
CREATE PROCEDURE getAllHeightsOfDay(
    IN day DATE
)
BEGIN
	SELECT * FROM heights  WHERE DATE(start_time) = day ORDER BY id DESC;
END //

-- get the total times of all entries of day in table heights
CREATE PROCEDURE getTotalsOfDay(
    IN day DATE
)
BEGIN
    SELECT 
        TIME_FORMAT(SEC_TO_TIME(SUM(TIME_TO_SEC(
            CASE 
                -- Case 1: The entire period is within the same day
                WHEN DATE(start_time) = day AND DATE(end_time) = day THEN 
                    TIMEDIFF(end_time, start_time)
                
                -- Case 2: The period starts on the given day but ends on another day
                WHEN DATE(start_time) = day AND DATE(end_time) > day THEN 
                    TIMEDIFF(CONCAT(day, ' 23:59:59'), start_time)
                
                -- Case 3: The period starts before the given day and ends on the given day
                WHEN DATE(start_time) < day AND DATE(end_time) = day THEN 
                    TIMEDIFF(end_time, CONCAT(day, ' 00:00:00'))
                
                -- Case 4: The period spans the given day (starts before and ends after the given day)
                WHEN DATE(start_time) < day AND DATE(end_time) > day THEN 
                    TIMEDIFF(CONCAT(day, ' 23:59:59'), CONCAT(day, ' 00:00:00'))
                
                -- Case 5: The end_time is NULL (ongoing period), so calculate up to the end of the specified day
                WHEN DATE(start_time) = day AND end_time IS NULL THEN 
                    TIMEDIFF(CONCAT(day, ' 23:59:59'), start_time)
                
                -- Case 6: The start_time is before the given day and the period is ongoing (NULL end_time)
                WHEN DATE(start_time) < day AND end_time IS NULL THEN 
                    TIMEDIFF(CONCAT(day, ' 23:59:59'), CONCAT(day, ' 00:00:00'))
                
                ELSE '00:00:00'
            END
        ))), '%H:%i:%s') as total_time, 
        start_height as height 
    FROM heights 
    WHERE 
        -- Include rows where the start_time or end_time falls on the given day
        DATE(start_time) <= day AND (DATE(end_time) >= day OR end_time IS NULL)
    GROUP BY height;
END //

-- Get the avg of each height for each Month by id of month and year
CREATE PROCEDURE getMonthAvgs(
    IN month INT,
    IN year INT
)
BEGIN
    SELECT height , SEC_TO_TIME(AVG(TIME_TO_SEC(total_time))) as avg_time FROM daily_totals WHERE Month(day) = month AND Year(day) = year GROUP BY height, Month(day) ORDER BY Month(day);
END //

-- Get the avg of each day of the week
CREATE PROCEDURE getWeekAvgs()
BEGIN
    SELECT height, DAYOFWEEK(day) as id_of_day, SEC_TO_TIME(AVG(TIME_TO_SEC(total_time))) as avg_time FROM daily_totals GROUP BY height, id_of_day ORDER BY id_of_day;
END //

--  get entries of daily_totals of given day
CREATE PROCEDURE getDailyTotalsEntriesOfDay(
    IN selectedDay DATE
)
BEGIN
    SELECT * FROM daily_totals WHERE DATE(day) = selectedDay;
END //

-- saves day, height and total_time to table daily_totals
CREATE PROCEDURE saveDailyTotal(
    IN day_in DATE,
    IN height_in INT,
    IN total_time_in TIME
)
BEGIN
    INSERT INTO daily_totals (height, total_time, day) VALUES (height_in, total_time_in, day_in);
END //

--  get entries of monthly_avg of given day
CREATE PROCEDURE getMonthlyAvgEntriesOfMonth(
    IN month INT,
    IN year_in INT
)
BEGIN
    SELECT * FROM monthly_avg WHERE id_of_month = month AND year = year_in;
END //

-- saves the height, total_time, id_of_month, year to the table monthly_avg
CREATE PROCEDURE saveMonthlyAvg(
    IN height_in INT,
    IN total_time_in TIME,
    IN id_of_month_in INT,
    IN year_in INT
)
BEGIN
    INSERT INTO monthly_avg (height, total_time, id_of_month, year) VALUES (height_in, total_time_in, id_of_month_in, year_in);
END //

CREATE PROCEDURE getDailyTotalsOfYear(
    IN year INT
)
BEGIN
    SELECT * FROM daily_totals WHERE Year(day) = year;
END //

DELIMITER ;