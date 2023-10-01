# 所有チーム
import sqlite3

# データベースとの接続を確立
dbpath = "fifa23.db"
conn = sqlite3.connect(dbpath)

# teamsテーブル作成
sql = """
CREATE TABLE IF NOT EXISTS team_players(
    id INTEGER PRIMARY KEY,
    team_id INTEGER,
    player_id INTEGER,
    role TEXT
)"""

# カーソルを取得
cursor = conn.cursor()
# SQLを実行
cursor.execute(sql)
# データベースへ反映
conn.commit()
# カーソルを閉じる
cursor.close()

# team-players中間テーブル作成
sql = """
CREATE TABLE IF NOT EXISTS team_players(
    team_id INTEGER,
    player_id INTEGER,
    role TEXT,
    PRIMARY KEY(team_id, player_id)
)"""

# カーソルを取得
cursor = conn.cursor()
# SQLを実行
cursor.execute(sql)
# データベースへ反映
conn.commit()
# カーソルを閉じる
cursor.close()

# playersテーブル作成
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

# カーソルを取得
cursor = conn.cursor()
# SQLを実行
cursor.execute(sql)
# データベースへ反映
conn.commit()
# カーソルを閉じる
cursor.close()

# # card_levelテーブル作成
# sql = """
# CREATE TABLE IF NOT EXISTS card_level(
#     id  INTEGER PRIMARY KEY,
#     player_id INTEGER,
#     name TEXT,
#     card TEXT,
#     level INTEGER
# )"""
# # カーソルを取得
# cursor = conn.cursor()
# # SQLを実行
# cursor.execute(sql)
# # データベースへ反映
# conn.commit()
# # カーソルを閉じる
# cursor.close()

# # countryテーブル作成
# sql = """
# CREATE TABLE IF NOT EXISTS country(
#     name TEXT PRIMARY KEY,
#     country TEXT
# )"""
# # カーソルを取得
# cursor = conn.cursor()
# # SQLを実行
# cursor.execute(sql)
# # データベースへ反映
# conn.commit()
# # カーソルを閉じる
# cursor.close()

# データベースとの接続を切断
conn.close()
