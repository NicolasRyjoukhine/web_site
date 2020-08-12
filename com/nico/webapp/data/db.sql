ALTER TABLE register DROP COLUMN register_id;

ALTER TABLE register ADD register_id INTEGER autoincrement ;
-- register definition
 CREATE TABLE register (name varchar NOT NULL,
familly_name varchar NOT NULL,
age varchar NOT NULL,
birthday varchar NOT NULL,
hobby varchar NULL,
email varchar NULL,
password varchar NULL,
register_id INTEGER PRIMARY KEY autoincrement);

CREATE TABLE hobbies (name varchar NOT NULL,
hobby_id INTEGER PRIMARY KEY autoincrement);

CREATE TABLE register_hobby ( register_id INTEGER,
hobby_id INTEGER,
PRIMARY KEY (register_id,
hobby_id),
FOREIGN KEY (register_id) REFERENCES register (register_id),
FOREIGN KEY (hobby_id) REFERENCES hobbies (hobby_id) );

insert
	into
	hobbies (name)
values ('reading');

DROP TABLE register_hobby ;

CREATE TABLE IF NOT EXISTS register_hobby (register_id INTEGER,
hobby_id INTEGER,
PRIMARY KEY (register_id, hobby_id),
FOREIGN KEY (register_id) REFERENCES register (register_id),
FOREIGN KEY (hobby_id) REFERENCES hobbies (hobby_id));
