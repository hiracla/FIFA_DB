from my_functions import print_players_prettytable

sql = """ SELECT * FROM players WHERE level ==76 """
print_players_prettytable(sql)
