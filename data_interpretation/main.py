from mysql import connector as sql

connection = sql.connect(user='bober', password='2211', host='127.0.0.1', database='mystic_quest', port='2211')
# result = connection.cursor().execute("SELECT * FROM players LIMIT 5")
# print(result)

