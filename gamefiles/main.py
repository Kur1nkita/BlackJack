import datetime
from table import Table
from deck import Deck
from player import Player
from os import system
import psycopg2


def convert_data_to_metadata(data: int) -> tuple[list]:
    ...


def main():
    conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="123")
    cur = conn.cursor()
    deck = Deck()
    state = True
    while state:
        system("cls")
        print("Welcome to the BlackJack game! (If you are stuck, write help)")
        while True:
            command = input().strip().lower()
            system("cls")
            if command == "help":
                # TODO: replays, replay player, reset, play
                print("Commands:\n"
                      "play : starts the BlackJack game\n"
                      "players : Shows all the players in the database\n"
                      "add player : adds a player to the database\n"
                      "restart player : restarts a player balance\n"
                      "replays : shows a list of previous games\n"
                      "replay player : show a list of replays from a spesific player\n"
                      "reset : resets the database and removes everything\n"
                      "quit : quits the game")
                input("\nPress Enter when done\n")
                break
            elif command == "players":
                cur.execute("""
                SELECT user_id, username, money, join_date
                FROM players""")
                temp = f'Player list:\n'
                for id, name, money, join_date in cur.fetchall():
                    temp += f'{id} : {name}, Balance ({money})    JOINED: {join_date}\n'
                print(temp)
                input("\nPress Enter when done\n")
                break
            elif command == "add player":
                name = input("Name of the player:\n").strip().capitalize()
                temp = datetime.datetime.now()
                date = f'{temp.year}-{temp.month}-{temp.day}'
                try:
                    cur.execute("""
                    INSERT INTO players (username, money, join_date)
                    VALUES (%s, 500, %s)
                    """, (name, date))
                except psycopg2.errors.UniqueViolation:
                    conn.rollback()
                    print("Name already in database")
                    input("\nPress Enter when done\n")
                    break
                conn.commit()
                print("SUCCESSFUL")
                input("\nPress Enter when done\n")
                break
            elif command == "quit":
                state = False
                break
            elif command == "restart player":
                name = input("Name of the player:\n").strip().capitalize()
                cur.execute("UPDATE players SET money = 500 WHERE username = %s", (name,))
                conn.commit()
                print("SUCCESSFUL")
                input("\nPress Enter when done\n")
                break
            elif command == "replays":
                cur.execute("""
                SELECT p.username, tp.table_id, game_date
                FROM table_record as tr INNER JOIN table_player_id_record as tp ON (tr.table_id = tp.table_id) 
                    INNER JOIN players as p ON (tp.user_id = p.user_id)
                ORDER BY game_date DESC 
                """)
                temp = f'Game records (username, Table_id, Date):\n'
                for username, table_id, date in cur.fetchall():
                    temp += f'{username} : {table_id}   PLAYED: {date}'
                print(temp)
                state = input("\nEnter a table_id you want to look at, or else Enter when done\n")
                if state == "":
                    break
                # TODO: Finish this command
            else:
                print("Welcome to the BlackJack game! (If you are stuck, write help)")


    cur.close()
    conn.close()
    system("cls")


if __name__ == "__main__":
    main()
