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

from gamefiles.table import Table
from gamefiles.player import Player

table = Table([Player(1, "Emil", 500), Player(2, "Emily", 500)],
              bets=[[100, False], [100, False]])
table.game_start()
print(table)