-- $ sqlite3 schema.db < schema.sql

PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS user_following;
DROP TABLE IF EXISTS Tweets;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    username VARCHAR primary key,
    email VARCHAR,
    password VARCHAR
);

CREATE TABLE user_following (
    username VARCHAR,
    usernameToFollow VARCHAR,
    FOREIGN KEY(username) REFERENCES users(username)
    FOREIGN KEY(usernameToFollow) REFERENCES users(username)
);

CREATE TABLE Tweets(
	username VARCHAR,
	text VARCHAR,
    timestamp DATETIME,
	FOREIGN KEY(username) REFERENCES users(username)
);
INSERT INTO users(username, email, password) VALUES('ProfAvery', 'bestprofessor@csu.fullerton.edu', 'KenyttCpSc449');
INSERT INTO users(username, email, password) VALUES('Anna', 'Anna@gmail.com', 'ajwsh@ksdm');
INSERT INTO users(username, email, password) VALUES('Pavani', 'nagisettipavani@gmail.com', 'aahd@g23!');
INSERT INTO users(username, email, password) VALUES('Sruthi', 'sruthi@gmail.com', '04sru@1994');
INSERT INTO users(username, email, password) VALUES('Sam', 'sam@gmail.com', 'samhash@akkineni');
INSERT INTO users(username, email, password) VALUES('Rushabh', 'rushabh@gmail.com', 'rushabh9348$3');
INSERT INTO user_following(username, usernameToFollow) VALUES('Pavani', 'Sam');
INSERT INTO user_following(username, usernameToFollow) VALUES('Pavani', 'ProfAvery');
INSERT INTO user_following(username, usernameToFollow) VALUES('Sruthi', 'Anna');
INSERT INTO Tweets(username, text, timestamp) VALUES('Sruthi', 'Hey! this is my first tweet', '2020-10-06 06:03:47.989280');
INSERT INTO Tweets(username, text, timestamp) VALUES('Anna', 'Super excited!', '2020-10-06 06:03:47.989280');
COMMIT;
