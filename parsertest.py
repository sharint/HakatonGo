alphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t']

# Получение ходов и запись их в SGF file
def addTurnsToSGFwithTime(turns,count):

    # Созддаем пустой SGF файл
    f = open('static/game'+str(count)+'.sgf','a')
    #print(turns)
    for i in range(len(turns)):
        # Присваивание значений
        Color =str( turns[i][0])
        if turns[i][1] == "PASS":
            string = ';'+Color[0].upper()+"[]"
        else:
            setx= turns[i][1]['x']
            sety=turns[i][1]['y']
            string = ';'+Color[0].upper()+"[{0}{1}]".format(alphabet[setx],alphabet[sety])
        # Запись значений в SGF файл
        f.write(string+'\n')
    f.write(')')
    f.close()
