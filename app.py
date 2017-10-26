from flask import Flask, render_template,request
import pandas as pd
import urllib

def getprice(ticker):

    url="https://www.google.com/finance/historical?output=csv&q="+ticker
    stock = ticker+".csv"
    urllib.request.urlretrieve(url,stock)
    df = pd.read_csv(stock)
    l = list(df['Close'][::-1])
    return l

application = Flask(__name__)

@application.route('/',methods=['GET','POST'])
def index():
    if request.method =='POST':
        l = getprice(str(request.form['ticker']))
        return render_template('index.html',data=l)
    else:
        return render_template('index.html',data=[])

if __name__ == '__main__':
    application.run(host='127.0.0.1',debug=True,port=80)
