CREATE USER 'deskController'@'localhost' IDENTIFIED BY 'password';
CREATE DATABASE standing_desk;

USE standing_desk;

CREATE TABLE desk (
    id INT AUTO_INCREMENT PRIMARY KEY,
    height INT,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
);

GRANT INSERT, SELECT ON standing_desk.desk TO 'deskController'@'localhost';