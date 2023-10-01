import sqlite3

# import requests

# import pandas as pd

# import numpy as np
from flask import Flask, render_template, request, g

app = Flask(__name__)


def get_db():
    if "db" not in g:
        # データベースをオープンしてFlaskのグローバル変数に保存
        g.db = sqlite3.connect("fifa23.db")
    return g.db


def get_players(con):
    # データベースを開く
    # con = get_db()

    # 選手一覧を読み込み
    cur = con.execute("SELECT * FROM players ORDER BY name")
    data = cur.fetchall()

    return data


def get_playersname(con):
    # データベースを開く
    # con = get_db()

    # 選手一覧を読み込み
    cur = con.execute("SELECT name FROM players ORDER BY name")
    data = cur.fetchall()
    for i in range(len(data)):
        data[i] = data[i][0]
    data.sort()

    return data


def get_clublist(con):
    # データベースを開く
    # con = get_db()

    # クラブ名を読み込み(重複なし)
    cur = con.execute("SELECT DISTINCT club FROM players")
    data = cur.fetchall()
    for i in range(len(data)):
        data[i] = data[i][0]
    data.sort()

    return data


def get_cardlist(con):
    # データベースを開く
    # con = get_db()

    # カード名を読み込み(重複なし)
    cur = con.execute("SELECT DISTINCT card FROM players")
    data = cur.fetchall()
    for i in range(len(data)):
        data[i] = data[i][0]
    data.sort()

    return data


@app.route("/")
def index():
    # print("index")
    # データベースを開く
    con = get_db()

    # 選手一覧を読み込み
    cur = con.execute("SELECT * from teams order by team_name")
    data = cur.fetchall()
    con.close()

    return render_template("index.html", data=data)


@app.route("/players", methods=["GET"])
def players():
    print("players")
    # データベースを開く
    con = get_db()

    # 選手一覧を読み込み
    cur = con.execute("SELECT * FROM players ORDER BY name")
    data = cur.fetchall()

    # クラブ名を読み込み(重複なし)
    cur = con.execute("SELECT DISTINCT club FROM players")
    clubdata = cur.fetchall()
    for i in range(len(clubdata)):
        clubdata[i] = clubdata[i][0]
    clubdata.sort()

    # カード名を読み込み(重複なし)
    cur = con.execute("SELECT DISTINCT card FROM players")
    carddata = cur.fetchall()
    for i in range(len(carddata)):
        carddata[i] = carddata[i][0]
    carddata.sort()
    con.close()

    # print("data={}".format(data))
    # print("club={}".format(clubdata))
    # print("card={}".format(carddata))
    return render_template(
        "players.html", data=data, clubdata=clubdata, carddata=carddata
    )


def membersFromTop():
    # value = request.form["update"]
    value = request.form.get("update", None)
    print("value={}".format(value))
    # if request.form["update"] == "update":
    print("requestMethod={}".format(request.method))
    if request.method == "POST":
        print("Members update")
    else:
        print("MEMBERS")
    initdata = [None, "", "", None, "", "", "", "", None, None, None, None, None, None]

    # データベースを開く
    con = get_db()
    tname = request.args.get("teamname")
    print("teamname={}".format(tname))

    # 一致する選手一覧を読み込み
    names = []  # teamsに登録されている選手一覧
    cards = []  # teamsに登録されている選手のカード種類一覧

    for i in range(23):
        if i < 18:
            sql = "SELECT member" + str(i + 1).zfill(2)
        else:
            sql = "SELECT reserve" + str(i + 1 - 18).zfill(2)
        sql += " FROM teams WHERE teams.teamname=" + "'" + tname + "'"
        sqlcards = (
            "SELECT card"
            + str(i + 1).zfill(2)
            + " FROM teams WHERE teams.teamname="
            + "'"
            + tname
            + "'"
        )
        # print(sqlcards)

        cur = con.execute(sql)
        data = cur.fetchall()  # teams登録選手の選手データ
        # print(data)
        names.append(data[0][0])
        cur = con.execute(sqlcards)
        data = cur.fetchall()  # teams登録選手の選手データ
        cards.append(data[0][0])

    # for i in range(5):
    #     sql = (
    #         "SELECT reserve"
    #         + str(i + 1).zfill(2)
    #         + " FROM teams WHERE teams.teamname="
    #         + "'"
    #         + tname
    #         + "'"
    #     )
    #     cur = con.execute(sql)
    #     data = cur.fetchall()  # teams登録選手の選手データ
    #     names.append(data[0][0])
    # print("names={}".format(names))

    sql = "SELECT * FROM players WHERE (name, card) IN ("
    # print(sql)
    for i in range(len(names)):
        sql += "('" + names[i] + "', '" + cards[i] + "'), "
        # print("sql{}={}".format(i,sql))

    sql = sql.rstrip(", ") + ")"
    # print("sql= {}".format(sql))

    cur = con.execute(sql)
    data = cur.fetchall()  # playersから取り出した、teams登録選手の選手データ
    # print("data1={}".format(data))
    # datalen = len(data)
    # for i in range(len(names)):
    #     if i < datalen:
    #         continue
    #     else:
    #         data.append(initdata)
    # # data = np.array(data)
    # print("data2={}".format(data))
    nameslist = [None] * len(names)

    # teams登録順にdata内の選手を並び替える
    # for i in range(len(data)):
    #     try:
    #         pos = names.index(data[i][1])
    #         nameslist[i] = pos
    #         # print("nameslist1[{}]= {} {}".format(i, pos, data[i][1]))
    #     except:
    #         pass
    # print("nameslist2[{}]= Nodata, {}".format(i, names[i]))

    # print("nameslist=", nameslist, len(nameslist))
    # print("data4={}".format(data))
    # data2 = [initdata] * len(names)
    # for i in range(len(data)):
    # if nameslist[i]!:
    # data2[nameslist[i]] = data[i]
    # print("data2[{}]={}".format(nameslist[i], data[i][1]))

    # playersdata = get_playersname(con)
    # carddata = get_cardlist(con)

    con.close()

    return render_template(
        "members.html",
        data=data,
        # playersdata=playersdata,
        # carddata=carddata,
        teamname=tname,
    )


@app.route("/members", methods=["GET", "POST"])
def members():
    # データベースを開く
    con = get_db()

    tname = request.args.get("teamname", None)
    # teamnameがないときは更新ボタンから来た
    if tname is None:
        print("Members update")
        tname = request.args.get("update", None)
        # playerslist = requests.get("http://127.0.0.1:5000/members.html")
        url = "http://127.0.0.1:5000/members.html?teamname=" + tname
        # playerslist = requests.get(url)
        # playerslist = request.form.getlist("player3")

        try:
            player_data = request.form.get("playername").split(",")
            print("Player_data={}".format(player_data))
            player_name = player_data[0]
            player_no = player_data[1]
        except:
            player_name = ""
            player_no = "0"

        card_name = request.form.get("card")
        # playerslist = requests.get("members.html")
        # playerslist = td.getvalue.text("pname")
        # playerslist = request.form['update']

        # team_idを取得
        sql = "SELECT team_id FROM teams WHERE team_name='"
        sql += tname + "'"
        print("sql1={}".format(sql))
        cur = con.execute(sql)
        team_id = cur.fetchall()  # playersから取り出した該当選手のplayer_id

        # player_idを取得
        if player_name is not None and card_name is not None:
            sql = "SELECT player_id FROM players WHERE name='"
            sql += str(player_name) + "' AND card='"
            sql += str(card_name) + "'"
            print("sql2={}".format(sql))
            try:
                cur = con.execute(sql)
                player_id = cur.fetchall()  # playersから取り出した該当選手のplayer_id
                # print("player_id={}".format(player_id))
            except:
                print("No Player name={}, id={}".format(player_name, player_id))

            print(
                "url={}\nteamname={}\nplayername={},{},selected={}".format(
                    url, tname, player_name, player_no, card_name
                )
            )

            # team_idを取得
            sql="SELECT team_id FROM teams WHERE team_name='"
            sql+=str(tname)+"'"
            print("sql3={}".format(sql))
            cur = con.execute(sql)
            team_id = cur.fetchall()  # playersから取り出した、teams登録選手の選手データ

            # print("team_id({})={}".format(tname, team_id))

            # 変更を反映
            sql = "UPDATE team_players SET player_id="
            sql += str(player_id[0][0]) + " "
            sql += " WHERE team_id=" + str(team_id[0][0]) + " AND "
            sql += "player_id=" + str(player_no)
            print("sql4={}".format(sql))

            cur = con.execute(sql)
            data = cur.fetchall()  # playersから取り出した、teams登録選手の選手データ

        # df = pd.read_html("members.html")[0]
        # print(df)

    else:
        print("MEMBERS")

    # players_name = request.form["players"]
    # card_name = request.form["card"]

    # print("players={}, card={}".format(players_name, card_name))
    # print("requestMethod={}".format(request.method))

    initdata = [None, "", "", None, "", "", "", "", None, None, None, None, None, None]

    # 一致する選手一覧を読み込み
    # names = []  # teamsに登録されている選手一覧
    cards = []  # teamsに登録されている選手のカード種類一覧

    # スタメン
    sql = """
            SELECT p1.* FROM teams t
            INNER JOIN team_players tp1 ON t.team_id=tp1.team_id AND tp1.role='main'
            INNER JOIN players p1 ON tp1.player_id=p1.player_id
            WHERE t.team_name = 
        """
    sql += "'" + tname + "'"

    cur = con.execute(sql)
    data = cur.fetchall()  # playersから取り出した、teams登録選手の選手データ
    # print("member={}".format(data))

    # サブメンバー
    sql = """
            SELECT p2.* FROM teams t
            INNER JOIN team_players tp2 ON t.team_id=tp2.team_id AND tp2.role='sub'
            INNER JOIN players p2 ON tp2.player_id=p2.player_id
            WHERE t.team_name = 
        """
    sql += "'" + tname + "'"

    cur = con.execute(sql)
    data.extend(cur.fetchall())  # playersから取り出した、teams登録選手の選手データ
    # print("member={}".format(data))

    # 控えメンバー
    sql = """
            SELECT p3.* FROM teams t
            INNER JOIN team_players tp3 ON t.team_id=tp3.team_id AND tp3.role='reserve'
            INNER JOIN players p3 ON tp3.player_id=p3.player_id
            WHERE t.team_name = 
        """
    sql += "'" + tname + "'"

    cur = con.execute(sql)
    data.extend(cur.fetchall())  # playersから取り出した、teams登録選手の選手データ
    # print("member={}".format(data))

    # for i in range(len(data)):
    #     data[i] = data[i][1:]
    # print("member={}".format(data))

    # nameslist = [None] * len(names)

    # teams登録順にdata内の選手を並び替える
    # for i in range(len(data)):
    #     try:
    #         pos = names.index(data[i][1])
    #         nameslist[i] = pos
    #         # print("nameslist1[{}]= {} {}".format(i, pos, data[i][1]))
    #     except:
    #         pass
    # print("nameslist2[{}]= Nodata, {}".format(i, names[i]))

    # print("nameslist=", nameslist, len(nameslist))
    # print("data4={}".format(data))
    # data2 = [initdata] * len(names)
    # for i in range(len(data)):
    # if nameslist[i]!:
    # data2[nameslist[i]] = data[i]
    # print("data2[{}]={}".format(nameslist[i], data[i][1]))

    playersdata = get_playersname(con)
    carddata = get_cardlist(con)

    con.close()

    return render_template(
        "members.html",
        data=data,
        playersdata=playersdata,
        carddata=carddata,
        teamname=tname,
    )


# @app.route("/members", methods=["GET"])
# def members():
#     initdata = [None, "", "", None, "", "", "", "", None, None, None, None, None, None]

#     value = request.form.get("update", None)
#     print("value={}".format(value))

#     # データベースを開く
#     con = get_db()
#     tname = request.args.get("teamname")
#     print("teamname={}".format(tname))

#     # 一致する選手一覧を読み込み
#     names = []  # teamsに登録されている選手一覧

#     for i in range(18):
#         sql = (
#             "SELECT member"
#             + str(i + 1).zfill(2)
#             + " FROM teams WHERE teams.teamname="
#             + "'"
#             + tname
#             + "'"
#         )
#         cur = con.execute(sql)
#         data = cur.fetchall()  # teams登録選手の選手データ
#         names.append(data[0][0])
#     for i in range(5):
#         sql = (
#             "SELECT reserve"
#             + str(i + 1).zfill(2)
#             + " FROM teams WHERE teams.teamname="
#             + "'"
#             + tname
#             + "'"
#         )
#         cur = con.execute(sql)
#         data = cur.fetchall()  # teams登録選手の選手データ
#         names.append(data[0][0])

#     sql = "SELECT * FROM players WHERE name IN ("
#     for i in range(len(names)):
#         sql += "'" + names[i] + "', "

#     sql = sql.rstrip(", ") + ")"
#     # print("sql= {}".format(sql))

#     cur = con.execute(sql)
#     data = cur.fetchall()  # playersから取り出した、teams登録選手の選手データ
#     nameslist = [None] * len(names)

#     # teams登録順にdata内の選手を並び替える
#     for i in range(len(data)):
#         try:
#             pos = names.index(data[i][1])
#             nameslist[i] = pos
#             # print("nameslist1[{}]= {} {}".format(i, pos, data[i][1]))
#         except:
#             pass
#             # print("nameslist2[{}]= Nodata, {}".format(i, names[i]))

#     print("nameslist=", nameslist, len(nameslist))
#     # print("data4={}".format(data))
#     data2 = [initdata] * len(names)
#     for i in range(len(data)):
#         # if nameslist[i]!:
#         data2[nameslist[i]] = data[i]
#         # print("data2[{}]={}".format(nameslist[i], data[i][1]))

#     con.close()

#     return render_template("members.html", data=data2)


# @app.route("/updatemembers", methods=["GET"])
# def updatemembers():
#     print("***UPDATE MEMBERS***")
#     initdata = [None, "", "", None, "", "", "", "", None, None, None, None, None, None]

#     # データベースを開く
#     con = get_db()
#     tname = request.args.get("teamname")

#     sql = "UPDATE teams SET member01="

#     sql += "WHERE " + tname

#     print("tname={}, sql={}".format(tname, sql))

#     for i in range(len(names)):
#         sql += "('" + names[i] + "', '" + cards[i] + "'), "

#     sql = sql.rstrip(", ") + ")"

#     cur = con.execute(sql)
#     data = cur.fetchall()  # playersから取り出した、teams登録選手の選手データ
#     nameslist = [None] * len(names)

#     # teams登録順にdata内の選手を並び替える
#     for i in range(len(data)):
#         try:
#             pos = names.index(data[i][1])
#             nameslist[i] = pos
#         except:
#             pass

#     # print("nameslist=", nameslist, len(nameslist))
#     data2 = [initdata] * len(names)
#     for i in range(len(data)):
#         data2[nameslist[i]] = data[i]

#     playersdata = get_playersname(con)
#     carddata = get_cardlist(con)

#     con.close()
#     print("***UPDATE MEMBERS***")

#     return render_template(
#         "members.html", data=data2, playersdata=playersdata, carddata=carddata
#     )


@app.route("/register", methods=["POST"])
def register_post():
    print("登録開始")
    # テンプレートから新規登録する選手とパラメータを取得
    name = request.form["name"].upper()
    card = request.form["card"]
    level = request.form["level"]
    country = request.form["country"].title()
    league = request.form["league"].upper()
    club = request.form["club"]
    position = request.form["position"].upper()
    pac = request.form["pace"]
    sho = request.form["shoot"]
    pas = request.form["pass"]
    dri = request.form["dribble"]
    defe = request.form["defense"]
    phy = request.form["physical"]

    # データベースを開く
    con = get_db()

    if name:
        # 登録処理
        data = [
            name,
            card,
            level,
            country,
            league,
            club,
            position,
            pac,
            sho,
            pas,
            dri,
            defe,
            phy,
        ]
        sql = """INSERT INTO players(name, card, level, country, league, club, position, pace, shoot, pass, dribble, defense, physical)VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        # print(data)
        try:
            con.execute(sql, data)
            print("DB resist success")
        except:
            print("DB resister error")

        con.commit()

    playersdata = get_players()
    clubdata = get_clublist()
    carddata = get_cardlist()

    con.close()

    return render_template(
        "players.html", data=playersdata, clubdata=clubdata, carddata=carddata
    )


@app.route("/", methods=["POST"])
def team_register():
    # テンプレートから新規登録する選手とパラメータを取得
    team = request.form["team"]
    formation = request.form["formation"]
    director = request.form["director"]

    # データベースを開く
    con = get_db()

    if name:
        # 登録処理
        data = [
            team,
            formation,
            director,
        ]
        sql = """INSERT INTO teams(team, formation, director)VALUES(?,?,?)"""
        print(data)
        try:
            con.execute(sql, data)
        except:
            print("DB resister error")

        con.commit()

    # 一覧再読み込み
    cur = con.execute("SELECT * from teams order by team")
    data = cur.fetchall()
    con.close()

    print("team=", team)
    return render_template("index.html", data=data)


@app.route("/update", methods=["POST"])
def update_post():
    print("update")
    # テンプレートから新規登録する選手とパラメータを取得
    name = request.form["name"].upper()

    # 名前以外のパラメータ
    param = [None] * 12
    param[0] = request.form["level"]
    param[1] = request.form["card"]
    param[2] = request.form["country"].title()
    param[3] = request.form["league"].upper()
    param[4] = request.form["club"]
    param[5] = request.form["position"].upper()
    param[6] = request.form["pace"]
    param[7] = request.form["shoot"]
    param[8] = request.form["pass"]
    param[9] = request.form["dribble"]
    param[10] = request.form["defense"]
    param[11] = request.form["physical"]
    for i in range(len(param)):
        if (i >= 1 and i <= 5) and param[i]:
            param[i] = "'" + param[i] + "'"
    print(param)

    arr = [
        "level=",
        "card=",
        "country=",
        "league=",
        "club=",
        "position=",
        "pace=",
        "shoot=",
        "pass=",
        "dribble=",
        "defense=",
        "physical=",
    ]

    sql = """UPDATE players SET"""
    first = True
    for i in range(len(param)):
        if param[i]:
            if first:
                first = False
            else:
                sql += ","
            sql += " " + arr[i] + param[i]
        # else:
        #     print(arr[i])

    sql = sql + " WHERE name=" + "'" + name + "'"
    print("sql=", sql)

    # データベースを開く
    con = get_db()

    if name:
        print(param)
        print(sql)
        try:
            con.execute(sql)
            # print("DB update")
        except:
            print("DB update error")

        con.commit()

    playersdata = get_players(con)
    clubdata = get_clublist(con)
    carddata = get_cardlist(con)

    con.close()

    return render_template(
        "players.html", data=playersdata, clubdata=clubdata, carddata=carddata
    )


if __name__ == "__main__":
    app.debug = True
    app.run(host="localhost")
