DROP TABLE IF EXISTS url_record;
DROP TABLE IF EXISTS user;


CREATE TABLE url_record (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    url TEXT NOT NULL,
    remark TEXT NOT NULL,
    tag TEXT NOT NULL,
    status INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (user_id) );


CREATE TABLE user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name TEXT NOT NULL,
    password TEXT NOT NULL );