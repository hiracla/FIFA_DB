from my_functions import open_database
from my_functions import close_database

conn, cursor = open_database("fifa23.db")
# sql = """
# UPDATE players SET name='HAYDEN' WHERE name='HYDEN'
# """
# cursor.execute(sql)

sql = """
UPDATE teams SET card02=? WHERE teamname=?
"""
params = ["レア", "YouyizENG"]
cursor.execute(sql, params)

conn.commit()
close_database(cursor, conn)
