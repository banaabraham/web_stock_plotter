from flask import Flask, render_template,request,jsonify
import pandas as pd
import urllib
import calendar
import html
from google_read import google_read

def getprice(ticker):

    url="https://www.google.com/finance/historical?output=csv&q="+ticker
    stock = ticker+".csv"
    urllib.request.urlretrieve(url,stock)
    df = pd.read_csv(stock).iloc[::-1].iloc[-30:]
    l = list(df['Close'])
    abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
    tanggal = df['Date']
    date = []
    c = 0
    for i in tanggal:
        temp = i.split("-")
        date.append(int(temp[0]))
    return l,date


application = Flask(__name__)
l = []
dat = []
@application.route('/',methods=['GET','POST'])
def index():
    global l,dat
    if request.method =='POST':
        req = str(request.form['ticker'])       
        l,dat = getprice(req)
        ob = google_read(req)
        ob.get_text()
        pe = ob.get_pe_ratio()
        eps = ob.get_eps()
        div_yield = ob.get_div_yield()
        return render_template('index.html',title=req.upper(),data=l,date=dat,pe=pe,eps=eps,div_yield=div_yield)
    else:
        return render_template('index.html',data=[])

@application.route('/data')
def data():
    global l,dat
    return jsonify({'labels':dat,'series':l})


if __name__ == '__main__':
    application.run(host='192.168.137.1',debug=True,port=80)
