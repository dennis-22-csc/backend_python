-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS sms_api_dev_db;
CREATE USER IF NOT EXISTS 'sms_api_dev'@'localhost' IDENTIFIED BY 'sms_api_dev_pwd';
GRANT ALL PRIVILEGES ON `sms_api_dev_db`.* TO 'sms_api_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'sms_api_dev'@'localhost';
FLUSH PRIVILEGES;
