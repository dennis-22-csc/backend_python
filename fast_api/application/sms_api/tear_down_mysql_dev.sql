REVOKE ALL PRIVILEGES ON `sms_api_dev_db`.* FROM 'sms_api_dev'@'localhost';
REVOKE SELECT ON `performance_schema`.* FROM 'sms_api_dev'@'localhost';
DROP USER IF EXISTS 'sms_api_dev'@'localhost';
DROP DATABASE IF EXISTS sms_api_dev_db;

