DROP TABLE IF EXISTS table_player_id_record;
DROP TABLE IF EXISTS table_record;
DROP TABLE IF EXISTS players;


CREATE TABLE players (
    user_id serial PRIMARY KEY ,
    username varchar(50) NOT NULL UNIQUE ,
    money int NOT NULL ,
    join_date date NOT NULL
);

CREATE TABLE table_record (
    table_id serial PRIMARY KEY ,
    game_state text NOT NULL ,
    game_date date NOT NULL
);

CREATE TABLE table_player_id_record (
    user_id int UNIQUE ,
    table_id int UNIQUE ,
    PRIMARY KEY (user_id, table_id) ,
    FOREIGN KEY (user_id) REFERENCES players (user_id) ON DELETE CASCADE ,
    FOREIGN KEY (table_id) REFERENCES table_record (table_id)
);
