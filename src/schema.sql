DROP TABLE if EXISTS users;

CREATE TABLE users (
uid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
username VARCHAR(20) NOT NULL,
password VARCHAR(50) NOT NULL,
email VARCHAR (50) NOT NULL);
