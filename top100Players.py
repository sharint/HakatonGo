import requests
import json

def getPlayers():

    # Запрос на данные из сайта топ 100 игроков ГО
    req = requests.get("https://www.gokgs.com/top100.jsp")
    players = req.text.split("user")
    mas = []
    ranks = []
    #print(players)
    for i in range(1,len(players)):
        tmp = ''
        cursor = ''
        j = 1
        while cursor != '"':
            tmp+= players[i][j]
            cursor = players[i][j]
            j+=1
        tmp = tmp[0:len(tmp)-1]
        if players[i][len(tmp)*2+43] == "?":
            rank = players[i][len(tmp)*2+43]
        else:
            rank = players[i][len(tmp)*2+43]+players[i][len(tmp)*2+44]
        mas.append(tmp)
        ranks.append(rank)

    return mas,ranks
