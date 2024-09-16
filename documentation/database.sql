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

CREATE PROCEDURE getAllHeights()
BEGIN
	SELECT * FROM your_table ORDER BY id DESC LIMIT 1;
END //

DELIMITER ;