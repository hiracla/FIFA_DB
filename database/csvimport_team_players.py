import csv
import sqlite3

dbpath = "fifa23.db"
conn = sqlite3.connect(dbpath)
cursor = conn.cursor()
sql = """
CREATE TABLE IF NOT EXISTS team_players(
    team_id INTEGER,
    player_id INTEGER,
    role TEXT
)"""

cursor.execute(sql)
conn.commit()

with open("team_players.csv", "r", encoding="utf-8") as f:
    rows = csv.reader(f)
    header = next(rows)
    data = []
    for row in rows:
        data.append(row)

sql = """
INSERT INTO team_players
(TEAM_ID, PLAYER_ID, ROLE)
VALUES(?,?,?)"""

cursor.executemany(sql, data)
conn.commit()
cursor.close()
conn.close()
