import csv
import sqlite3

dbpath = "fifa23.db"
conn = sqlite3.connect(dbpath)
cursor = conn.cursor()
sql = """
CREATE TABLE IF NOT EXISTS players(
    player_id INTEGER PRIMARY KEY,
    name TEXT,
    card TEXT,
    level INTEGER,
    country TEXT,
    league TEXT,
    club TEXT,
    position TEXT,
    pace INTEGER,
    shoot INTEGER,
    pass INTEGER,
    dribble INTEGER,
    defence INTEGER,
    physical INTEGER
)"""

cursor.execute(sql)
conn.commit()

with open("FIFA23Switch_players.csv", "r", encoding="utf-8") as f:
    rows = csv.reader(f)
    header = next(rows)
    data = []
    for row in rows:
        data.append(row)

sql = """
INSERT INTO players
(PLAYER_ID, NAME, CARD, LEVEL, COUNTRY, LEAGUE, CLUB, POSITION, PACE, SHOOT, PASS, DRIBBLE, DEFENCE, PHYSICAL)
VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""

cursor.executemany(sql, data)
conn.commit()
cursor.close()
conn.close()
