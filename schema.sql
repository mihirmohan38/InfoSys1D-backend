DROP TABLE IF EXISTS users; 
DROP TABLE IF EXISTS activities ; 
DROP TABLE IF EXISTS registered; 

CREATE TABLE users (

    username TEXT  , 
    password TEXT NOT NULL 

);

CREATE TABLE activities (
    unq_id INTEGER PRIMARY KEY ,
    category TEXT , 
    date_created DATE NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    date_activity DATE NOT NULL,
    creator TEXT,
    venue TEXT, 
    ppl INT, 
    image_uri IMAGE, 
    descrip TEXT, 
    max_ppl INT, 




);

CREATE TABLE registered (
    username TEXT , 
    unq_id INTEGER
);



INSERT INTO users VALUES ("mihir", "skydiving"); 
INSERT INTO activities VALUES (1, 'adventure', DATE(), DATE() , "mihir","nyx",3,NULL,"fun",4) ; 
INSERT INTO registered VALUES ("mihir", 1) ; 
INSERT INTO registered VALUES ("mihir", 2);
INSERT INTO registered values ("josh", 2); 
--SELECT TOP 5 * FROM activites WHERE creator = NULL ; 