from flask import Flask, render_template,redirect,request
import top100Players
import requesting
import timeParse
import time

app = Flask(__name__)

@app.route('/',methods = ['POST','GET'])
def startt():
    return render_template('start.html')

@app.route('/start',methods = ['POST','GET'])
def main():
    return render_template('start.html')

@app.route('/SGF',methods = ['POST','GET'])
def start():

    result = ''
    if request.method == 'POST':
        result = list(request.form.to_dict().keys())[0]
        result = result.split(" ")
        timeStamp1,timeStamp2 = requesting.getSGFFile(result[0])
        time.sleep(2)
        startTime1 = timeParse.convertTime(timeStamp1)
        startTime2 = timeParse.convertTime(timeStamp2)
        return render_template("jgoboard-master/demoSGF"+str(result[1])+".html",result = result,game1 = startTime1,game2 = startTime2)

@app.route('/index',methods = ['POST','GET'])
def index():
    players100,ranks = top100Players.getPlayers()
    #name = 'name'
    result = ''
    return render_template('index.html',players=players100, ranks = ranks, result = result)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == "__main__":
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)
