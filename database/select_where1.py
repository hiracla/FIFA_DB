from my_functions import open_database
from my_functions import close_database
from prettytable import PrettyTable

conn, cursor = open_database("fifa23db.db")
sql = """SELECT name,club FROM fifa23db"""

cursor.execute(sql)
data = cursor.fetchall()
table = PrettyTable(["name", "club"])
for name, club in data:
    table.add_row([name, club])
print(table)
close_database(cursor, conn)
