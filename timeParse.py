from datetime import datetime

def convertTime(timeStamp):
    
    timeStamp = timeStamp.split('.')
    time = datetime.strptime(timeStamp[0], '%Y-%m-%dT%H:%M:%S')
    result = str(time.hour)+':'+str(time.minute)+':'+str(time.second)+' '+str(time.year)+'-'+str(time.month)+'-'+str(time.day)
    return result

print(convertTime('2021-03-22T06:57:33.967Z'))

