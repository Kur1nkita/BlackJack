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
            if command == "help":
                system("cls")
                # TODO: replays, replay player, play
                print("Commands:\n"
                      "play : starts the BlackJack game\n"
                      "players : Shows all the players in the database\n"
                      "add player : adds a player to the database\n"
                      "delete player : removes a player from the database\n"
                      "restart player : restarts a player balance\n"
                      "replays : shows a list of previous games\n"
                      "replay player : show a list of replays from a spesific player\n"
                      "quit : quits the game")
                input("\nPress Enter when done\n")
                break
            elif command == "players":
                cur.execute("""
                SELECT user_id, username, money, join_date
                FROM players""")
                system("cls")
                temp = f'Player list:\n'
                for id, name, money, join_date in cur.fetchall():
                    temp += f'{id} : {name}, Balance ({money})    JOINED: {join_date}\n'
                temp += "\nPress Enter when done"
                print(temp)
                input()
                break
            elif command == "add player":
                system("cls")
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
            elif command == "delete player":
                system("cls")
                name = input("Name of the player:\n").strip().capitalize()
                cur.execute("DELETE FROM players WHERE username = %s", (name,))
                conn.commit()
                print("SUCCESSFUL")
                input("\nPress Enter when done\n")
                break

    cur.close()
    conn.close()
    system("cls")


if __name__ == "__main__":
    main()
