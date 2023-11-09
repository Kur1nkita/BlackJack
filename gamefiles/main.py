import datetime
import time

from table import Table
from deck import Deck
from player import Player
from os import system
import psycopg2


def convert_data_to_game_data(data: str) -> tuple:
    players = []
    bets = []
    hands = []
    game_state, game_date = data
    player_data, bet_data, hand_data = game_state.split("_")
    for x in player_data.split(";"):
        user_id, username, money = x.split(",")
        player = Player(int(user_id), username, int(money))
        players.append(player)
    for x in bet_data.split(";"):
        double = False
        if x[-1] == "T":
            double = True
        bets.append([int(x[:-1]), double])
    for x in hand_data.split(";"):
        hand = []
        for y in x:
            if y == "1":
                hand.append("10")
            else:
                hand.append(y)
        hands.append(hand)
    return players, hands, bets, game_date


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
                # TODO: play
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
                    VALUES (%s, 1000, %s)
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
                cur.execute("UPDATE players SET money = 1000 WHERE username = %s", (name,))
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
                print("\nEnter a table_id you want to look at, or else Enter when done")
                condition = False
                number = None
                while True:
                    try:
                        number_str = input().strip()
                        if number_str == "":
                            condition = True
                            break
                        number = int(state)
                        break
                    except ValueError:
                        print("Not a number")
                if condition:
                    break
                system("cls")
                cur.execute("""
                SELECT game_state, game_date
                FROM table_record
                WHERE table_id = %s
                """, (number,))
                data = cur.fetchone()
                if data is None:
                    print("Could not find the game replay, try a different table_id")
                    input("\nPress Enter when done\n")
                    break
                players, hands, bets, game_date = convert_data_to_game_data(data[0])
                table = Table(players, hands, bets, game_date)
                print(table)
                input("\nPress Enter when done\n")
                break
            elif command == "replay player":
                name = input("Name of the player:\n").strip().capitalize()
                cur.execute("""
                SELECT p.username, tp.table_id, game_date
                FROM table_record as tr INNER JOIN table_player_id_record as tp ON (tr.table_id = tp.table_id) 
                    INNER JOIN players as p ON (tp.user_id = p.user_id)
                WHERE p.username = %s
                ORDER BY game_date DESC 
                """, (name,))
                data = cur.fetchall()
                if not data:
                    print("No data from player")
                    input("\nPress Enter when done")
                    break
                temp = f'Game records (username, Table_id, Date):\n'
                for username, table_id, date in data:
                    temp += f'{username} : {table_id}   PLAYED: {date}'
                print(temp)
                print("\nEnter a table_id you want to look at, or else Enter when done")
                condition = False
                number = None
                while True:
                    try:
                        number_str = input().strip()
                        if number_str == "":
                            condition = True
                            break
                        number = int(state)
                        break
                    except ValueError:
                        print("Not a number")
                if condition:
                    break
                system("cls")
                cur.execute("""
                                SELECT game_state, game_date
                                FROM table_record
                                WHERE table_id = %s
                                """, (number,))
                data = cur.fetchone()
                if data is None:
                    print("Could not find the game replay, try a different table_id")
                    input("\nPress Enter when done\n")
                    break
                players, hands, bets, game_date = convert_data_to_game_data(data[0])
                table = Table(players, hands, bets, game_date)
                print(table)
                input("\nPress Enter when done\n")
                break
            elif command == "reset":
                cur.execute(open("blackjack_table_reset.sql", "r").read())
                conn.commit()
                print("SUCCESSFUL")
                input("\nPress Enter when done\n")
                break
            elif command == "play":
                print("Write in player name. Max 8 seats. Player can have multiple seats.\n"
                      "(No empty seats in between though! Press Enter when done)")
                players = []
                bets = []
                table_seat_index = {}
                condition = False
                for x in range(1, 9):
                    if condition:
                        break
                    print(f'\nTable {x}')
                    while True:
                        print("Name: ", end="")
                        name = input().strip().capitalize()
                        if name == "":
                            condition = True
                            break
                        if name not in table_seat_index:
                            cur.execute("""
                            SELECT user_id, username, money
                            FROM players
                            WHERE username = %s AND money >= 100
                            """, (name,))
                            data = cur.fetchone()
                            if data is None:
                                print("No player with that name, or player has not enough money. "
                                      "Money must be bigger or equal 100")
                                continue
                            user_id, username, money = data
                            player = Player(user_id, username, money)
                            table_seat_index[username] = player
                            players.append(player)
                        else:
                            temp = table_seat_index[name].getMoney()
                            if temp < 100:
                                print(f'Not enough money on the player. Balance: {temp}')
                                continue
                            players.append(table_seat_index[name])
                        player = table_seat_index[name]
                        bet = None
                        while True:
                            try:
                                print("Bet: ", end="")
                                bet = int(input().strip().capitalize())
                                if bet < 100:
                                    print("Too low bet size. Min bet = 100")
                                    continue
                                elif bet > player.getMoney():
                                    print(f'Too high bet. Not enough money on the player. Balance: {player.getMoney()}')
                                    continue
                            except ValueError:
                                print("Not a number")
                                continue
                            break
                        player.money -= bet
                        bets.append([bet, False])
                        break
                system("cls")
                if deck.getAmount() <= 20:
                    deck.shuffle()
                    print("DECK NEEDS A SHUFFLE")
                    time.sleep(2)
                system("cls")
                table = Table(players, bets)
                table.game_start()
                input("\nPress Enter when done\n")
                data = table.get_data()
                # TODO: Finish processing data
                conn.commit()
            else:
                break


    cur.close()
    conn.close()
    system("cls")


if __name__ == "__main__":
    main()
