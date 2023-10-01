# 所有チーム
import sqlite3

# データベースとの接続を確立
dbpath = "fifa23.db"
conn = sqlite3.connect(dbpath)

# カーソルを取得
cursor = conn.cursor()


# 変数SQLにSQL分を設定
sql = """DROP TABLE team_players"""

# SQLを実行
cursor.execute(sql)

# データベースへ反映
conn.commit()

# カーソルを閉じる
cursor.close()

# データベースとの接続を切断
conn.close()
