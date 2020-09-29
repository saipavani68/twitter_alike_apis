-- $ sqlite3 schema.db < schema.sql

PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS user_following;

CREATE TABLE users (
    username VARCHAR primary key,
    email VARCHAR,
    password VARCHAR
);

CREATE TABLE user_following (
    username VARCHAR primary key,
    usernameToFollow VARCHAR,
    FOREIGN KEY(username) REFERENCES users(username)
);

INSERT INTO users(username, email, password) VALUES('Julie', 'Julie@gmail.com', 'sahdh@934@');
COMMIT;
