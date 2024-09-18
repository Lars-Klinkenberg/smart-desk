DROP DATABASE IF EXISTS standing_desk;
CREATE DATABASE standing_desk;


USE standing_desk;
CREATE USER 'deskController'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON standing_desk.* to "deskController"@"localhost";

CREATE TABLE heights(
    id INT AUTO_INCREMENT PRIMARY KEY,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    start_height INT,
    end_time TIMESTAMP,
    end_height INT
);

CREATE TABLE daily_avg(
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

DELIMITER //

CREATE PROCEDURE saveStartHeight(
    IN height INT
)
BEGIN
	INSERT INTO heights (start_height) VALUES (height);
END //


CREATE PROCEDURE saveEndHeight(
    IN height INT
)
BEGIN
	UPDATE heights SET end_time = CURRENT_TIMESTAMP(), end_height = height ORDER BY id DESC LIMIT 1;
END //


CREATE PROCEDURE getLatestHeight()
BEGIN
	SELECT * FROM heights ORDER BY id DESC LIMIT 1;
END //


CREATE PROCEDURE getAllHeights(
    IN `lim_val` INT
)
BEGIN
	SELECT * FROM heights ORDER BY id DESC LIMIT lim_val;
END //

CREATE PROCEDURE getAllHeightsOfDay(
    IN day DATE
)
BEGIN
	SELECT * FROM heights  WHERE DATE(start_time) = day ORDER BY id DESC;
END //

CREATE PROCEDURE getTotalsOfDay(
    IN day DATE
)
BEGIN
    SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(TIMEDIFF(end_time, start_time)))) as total_time, start_height as height FROM heights WHERE DATE(start_time) = day GROUP BY height;
END //

CREATE PROCEDURE getMonthlyTotals()
BEGIN
    SELECT height, Month(day) as id_of_month, SEC_TO_TIME(SUM(TIME_TO_SEC(total_time))) as total_time FROM daily_avg GROUP BY height, Month(day);
END //

CREATE PROCEDURE getWeeklysTotals()
BEGIN
    SELECT height, DAYOFWEEK(day) as id_of_day, SEC_TO_TIME(SUM(TIME_TO_SEC(total_time))) as total_time FROM daily_avg GROUP BY height, id_of_day SORT BY ;
END //

DELIMITER ;