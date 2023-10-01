from my_functions import open_database
from my_functions import close_database

conn, cursor = open_database("fifa23.db")
params = [
    (77, "VITOLO", "Spain", "ESP2", "UDラス・パルマス", "LM", 72, 76, 76, 76, 411, 70),
    (76, "OLISE", "France", "ENG1", "クリスタル・パレス", "RW", 80, 70, 76, 80, 50, 53),
]

sql = """
INSERT INTO players( LEVEL, NAME, COUNTRY, LEAGUE, CLUB, POSITION, PACE, SHOOT, PASS, DRIBBLE, DEFENSE, PHYSICAL )
VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
"""
# INSERT INTO players( level, name, country, league, club, position, pace, shoot, pass, dribble, deffense, physical )

cursor.executemany(sql, params)

conn.commit()
close_database(cursor, conn)
