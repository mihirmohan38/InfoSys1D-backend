DROP TABLE IF EXISTS users; 
DROP TABLE IF EXISTS activities; 
DROP TABLE IF EXISTS registered; 

CREATE TABLE users (

    username TEXT  , 
    password TEXT NOT NULL , 
    telegram TEXT, 
    preference TEXT

);

CREATE TABLE activities (
    unq_id INTEGER PRIMARY KEY ,
    title TEXT NOT NULL,
    category TEXT , 
    date_created DATE NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    date_activity INT,
    creator TEXT,
    venue TEXT, 
    ppl INT, 
    image_uri IMAGE, 
    descrip TEXT, 
    max_ppl INT, 
    telegram_group TEXT
);

CREATE TABLE registered (
    username TEXT , 
    unq_id INTEGER
);



INSERT INTO users VALUES ("mihir", "skydiving", "mihir00", "sports"); 
INSERT INTO activities VALUES (1,"sucba diving", 'adventure', DATE(), 201912031600 , "mihir","nyx",3,NULL,"fun",4,"television group") ; 
INSERT INTO activities VALUES (2, "NLP in rock and roll", "education", DATE(), 201912051500, "Rahul",'ISH',300,NULL, "motivational", 500, "geek") ; 
INSERT INTO registered VALUES ("mihir", 1) ; 
INSERT INTO registered VALUES ("mihir", 2);
INSERT INTO registered values ("josh", 2); 
--SELECT TOP 5 * FROM activites WHERE creator = NULL ; 