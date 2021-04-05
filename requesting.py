# Имортируем нужные библиотеки
from requests_html import HTMLSession
import json
import parsertest

# Const url сервер Го для запосов
url = 'https://www.gokgs.com/json-cors/access' 

# Сессия для request запросов
session = HTMLSession() 

# GET request
def getData():
    req = session.get(url = url)
    return req

# POST request
def postData(data):
    req = session.post(url = url,data = data)
    return req

# Считывание с json файла
def readJson(path):
    return str(json.load(open(path)))

# Запись в json файл
def writeJson(fileName, jsonObject):
    with open(fileName, 'w', encoding='utf-8') as f:
        json.dump(jsonObject, f, ensure_ascii=False, indent=4)

# Считывание ходов с load room
def getTurns(game):
    id = 0
    # Поиск индекса для массива json
    for i in range(len(game['messages'])):
        a = str(game['messages'][i].keys())
        if 'sgfEvents' in a:
            id = i

    resullt = []
    # Присваивание значений
    for i in range(2,len(game['messages'][id]['sgfEvents']),2):
        loc = game['messages'][id]['sgfEvents'][i]['props'][0]['loc']
        if 'color' in str(game['messages'][id]['sgfEvents'][i]['props'][0]):
            color = game['messages'][id]['sgfEvents'][i]['props'][0]['color']
        else:
            color = 'U'
        #print(id,i)
        #time = game['messages'][id]['sgfEvents'][i]['props'][1]['float']
        resullt.append((color,loc))
    return resullt

# Получения двух последних игр по таймстампам
def getTwoLastGames(lastGameTimeStamp1,lastGameTimeStamp2):
    print(lastGameTimeStamp1,lastGameTimeStamp2)
    timeStamps = [lastGameTimeStamp1,lastGameTimeStamp2]
    result = []
    gameRes = []
    count = 1
    for timeStamp in timeStamps:
        #print(timeStamp)
    # Создаем json request для loadRoom
        jsonLoadRoom = {
            "type":"ROOM_LOAD_GAME",
            "timestamp":timeStamp,
            "private": "true",
            "channelId": "22"
        }

        # Записываем jsonLoadRoom в файл 
        writeJson('load_room.json',jsonLoadRoom)

        # Считываем json load room
        typeRoomLoadGame = readJson("load_room.json")

        # request запрос на две последние игры игрока
        #print(typeRoomLoadGame)
        postData(data = typeRoomLoadGame)
        response = getData()
        game = response.json()
        gameRes.append(game)

        # Записывам информацию об играх в файл json
        writeJson('gameData'+str(count)+'.json',game)

        count+=1
        # Считываем ходы игры
        result.append(getTurns(game))

    return result,gameRes


# Вывод в консоль ходов
def outputTurns(turns):
    for i in range(len(turns)):
        print(turns[i],i," - ход")

# Получение двух SGF файлов из json
def getSGFFile(name):

    # Считываем json
    typeLogin = readJson('login.json')
    typeArchive = readJson('join_archive.json')

    # request логин
    postData(typeLogin)

    # request json
    typeArchive = {
        "type":"JOIN_ARCHIVE_REQUEST",
        "name": name
    }

    # Запись в файл для дальнейшего запроса
    writeJson('join_archive.json',typeArchive)
    typeArchive = readJson('join_archive.json')

    # (request) запрос для получение данных из архива пользователя
    postData(typeArchive)
    response = getData()
    jsonFileArchive = response.json()

    # Записываем jsonFileArchive в файл json
    writeJson('serverData.json',jsonFileArchive)

    # Ищем индекс в json массиве для нахождения timestamp игры
    for i in range(len(jsonFileArchive['messages'])):
        a = str(jsonFileArchive['messages'][i].keys())
        if 'type' in a:
            a =  str(jsonFileArchive['messages'][i]['type'])
            if a == 'ARCHIVE_JOIN':
                ID = i
    # Считываем две последние timestamp из json archive room
    lastGameTimeStamp1 = jsonFileArchive['messages'][ID]['games'][-1]['timestamp']
    lastGameTimeStamp2 = jsonFileArchive['messages'][ID]['games'][-2]['timestamp']
    #print(lastGameTimeStamp1,lastGameTimeStamp2)
    
    games,jsonGame = getTwoLastGames(lastGameTimeStamp1,lastGameTimeStamp2)
    print(jsonGame)
    # for на две иттерации(так как две последнии игры игры)
    for k in range(len(jsonGame)):

        # Ищем индекс в json массиве для нахождения параметров игроков в матче
        for i in range(len(jsonGame[k]['messages'])):
            a = str(jsonGame[k]['messages'][i].keys())
            if 'sgfEvents' in a:
                ID = i
        for i in range(len(jsonGame[k]['messages'])):
            a = str(jsonGame[k]['messages'][i].keys())
            if 'games' in a:
                IDgame = i
        
        # id нужных параметров (объявление)
        ID_DATE = 0
        ID_PLACE = 0
        ID_RESULT = 0
        ID_WHPLAYERNAME = 0
        ID_BLPLAYERNAME = 0

        # id нужных параметров (Поиск)
        for i in range(len(jsonGame[k]['messages'][ID]['sgfEvents'][0]['props'])):
            if 'DATE' in str(jsonGame[k]['messages'][ID]['sgfEvents'][0]['props'][i]):
                ID_DATE = i
            if 'PLACE' in str(jsonGame[k]['messages'][ID]['sgfEvents'][0]['props'][i]):
                ID_PLACE = i
            if 'RESULT' in str(jsonGame[k]['messages'][ID]['sgfEvents'][0]['props'][i]):
                ID_RESULT = i
            if 'PLAYERNAME' in str(jsonGame[k]['messages'][ID]['sgfEvents'][0]['props'][i]):
                ID_BLPLAYERNAME = i

        # Присваивание значений из json файла, параметры игроков
        ID_WHPLAYERNAME = ID_BLPLAYERNAME-1
        rules = jsonGame[k]['messages'][ID]['sgfEvents'][0]['props'][0]['rules']
        size = jsonGame[k]['messages'][ID]['sgfEvents'][0]['props'][0]['size']
        komi = jsonGame[k]['messages'][ID]['sgfEvents'][0]['props'][0]['komi']
        if "mainTime" in str(jsonGame[k]['messages'][ID]['sgfEvents'][0]['props'][0]):
            mainTime = jsonGame[k]['messages'][ID]['sgfEvents'][0]['props'][0]['mainTime']
        else:
            mainTime = ''
        if 'byoYomiPeriods' in str(jsonGame[k]['messages'][ID]['sgfEvents'][0]['props'][0]):
            byoYomiPeriods = jsonGame[k]['messages'][ID]['sgfEvents'][0]['props'][0]['byoYomiPeriods']
        else:
            byoYomiPeriods = ''
        if 'byoYomiTime' in str(jsonGame[k]['messages'][ID]['sgfEvents'][0]['props'][0]):
            byoYomiTime = jsonGame[k]['messages'][ID]['sgfEvents'][0]['props'][0]['byoYomiTime']
        else:
            byoYomiTime = ''
        byoTotal = str(byoYomiPeriods)+'X'+str(byoYomiTime)+' byo-yomi'
        playerWhite = jsonGame[k]['messages'][ID]['sgfEvents'][0]['props'][ID_WHPLAYERNAME]['text']
        playerBlack = jsonGame[k]['messages'][ID]['sgfEvents'][0]['props'][ID_BLPLAYERNAME]['text']

        if "rank" in str(jsonGame[k]['messages'][IDgame]['games'][0]['players']['white']):
            rankWhite = jsonGame[k]['messages'][IDgame]['games'][0]['players']['white']['rank']
        else:
            rankWhite = "?"

        if "rank" in str(jsonGame[k]['messages'][IDgame]['games'][0]['players']['black']):
            rankBlack = jsonGame[k]['messages'][IDgame]['games'][0]['players']['black']['rank']
        else:
            rankBlack = "?"
            
        date = jsonGame[k]['messages'][ID]['sgfEvents'][0]['props'][ID_DATE]['text']
        place = jsonGame[k]['messages'][ID]['sgfEvents'][0]['props'][ID_PLACE]['text']
        if 'text' in str(jsonGame[k]['messages'][ID]['sgfEvents'][0]['props'][ID_RESULT]):
            result = jsonGame[k]['messages'][ID]['sgfEvents'][0]['props'][ID_RESULT]['text']
        else:
            result = 'W+Resign'
        
        # Создание первой части SGF файла
        firstString = '(;GM[1]FF[4]CA[UTF-8]AP[CGoban:3]ST[2]'
        secondString = 'RU[{0}]SZ[{1}]KM[{2}]TM[{3}]OT[{4}]'.format(rules,size,komi,mainTime,byoTotal)
        thirdString = 'PW[{0}]PB[{1}]WR[{2}]BR[{3}]DT[{4}]PC[{5}]RE[{6}]'.format(playerWhite,playerBlack,rankWhite,rankBlack,date,place,result)
        strings = [firstString,secondString,thirdString]

        # Запись значений в SGF файл (параметры)
        f = open('static/game'+str(k+1)+'.sgf', 'w')
        for i in range(3):
            f.write(strings[i]+'\n')
        f.close()
        
        # Запись второй части SGF файла (ходы)
        parsertest.addTurnsToSGFwithTime(games[k],k+1)

    return lastGameTimeStamp1,lastGameTimeStamp2

# Запуск основного метода
#getSGFFile('RaksaRami')