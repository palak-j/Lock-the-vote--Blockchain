CREATE DATABASE votingdata;

USE votingdata;

CREATE TABLE users(
	username varchar(25) PRIMARY KEY,
	password varchar(25) NOT NULL
);


CREATE TABLE candidates(
	name varchar(25) PRIMARY KEY
);
  
  
CREATE TABLE nodes(
	port int PRIMARY KEY,
	blockchain TEXT
);


INSERT INTO users(username, password)
VALUES
	('A', 'abc'),
	('B', 'bcd'),
	('C', 'cde'),
    ('D', 'def'),
    ('E', 'efg'),
    ('F', 'fgh'),
    ('G', 'ghi'),
    ('H', 'hij'),
    ('I', 'ijk'),
    ('J', 'jkl'),
    ('K', 'klm'),
    ('L', 'lmn'),
    ('M', 'mno'),
    ('N', 'nop'),
    ('O', 'opq'),
    ('P', 'pqr');
    

INSERT INTO candidates(name)
VALUES
	  ('Z'),
    ('Y'),
    ('X'),
    ('W'),
    ('V');
    
    
