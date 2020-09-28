-- $ sqlite3 users.db < users.sql

PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    username VARCHAR primary key,
    email VARCHAR,
    password VARCHAR
);
INSERT INTO users(username, email, password) VALUES('Anna', 'Anna@gmail.com', 'ajwsh@ksdc.com');
COMMIT;
