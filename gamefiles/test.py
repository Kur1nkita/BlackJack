# import psycopg2
#
# conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="123")
#
# cur = conn.cursor()
#
# #do something
#
# cur.execute("""
# SELECT * FROM players WHERE user_id = 1;
# """)
#
# print(cur.fetchone())
#
# conn.commit()
#
# cur.close()
# conn.close()

from table import Table
from player import Player
from deck import Deck

player1 = Player(1, "Dumbass", 500)
player2 = Player(2, "Dumbass2", 500)
deck = Deck()

table = Table([player1, player2],
              bets=[[100, False], [100, False]])
table.game_start()
