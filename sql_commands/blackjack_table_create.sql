CREATE TABLE players (
    user_id serial PRIMARY KEY ,
    username varchar(50) NOT NULL UNIQUE
);

CREATE TABLE player_money (
    user_id int PRIMARY KEY ,
    money int NOT NULL ,
    FOREIGN KEY (user_id) REFERENCES players (user_id)
);

CREATE TABLE table_record (
    table_id serial PRIMARY KEY ,
    game_state int NOT NULL ,
    game_date date NOT NULL
);

CREATE TABLE table_player_id_record (
    user_id int UNIQUE ,
    table_id int UNIQUE ,
    PRIMARY KEY (user_id, table_id),
    FOREIGN KEY (user_id) REFERENCES players (user_id),
    FOREIGN KEY (table_id) REFERENCES table_record (table_id)
);