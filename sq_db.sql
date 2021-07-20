CREATE TABLE IF NOT EXISTS data (
id integer PRIMARY KEY AUTOINCREMENT,
user_id integer NOT NULL,
day text NOT NULL,
value_oks text NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY AUTOINCREMENT,
login text NOT NULL,
psw_hash text NOT NULL,
name text NOT NULL,
subname text NOT NULL,
cognomen text NOT NULL,
age integer NOT NULL,
weight text NOT NULL,
height text NOT NULL
);