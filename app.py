from flask import Flask,render_template, request
import requests
import quandl
import numpy as np
import pandas as pd
import datetime
from bokeh.plotting import figure, output_file, show
from bokeh.embed import file_html
from bokeh.resources import CDN
app_lulu = Flask(__name__)
app_lulu.vars = {}
def dateFormat(aDatetime):
    return ("%s-%s-%s" % (aDatetime.year, aDatetime.month, aDatetime.day))

@app_lulu.route('/mile', methods =['GET', 'POST'])
def index_lulu():
    if request.method == 'GET':
    	return render_template('input.html')
    else:
        app_lulu.vars['ticker'] = request.form['TickerChoice']
        print("User Requested: "+request.form['TickerChoice'])
        now = datetime.datetime.now()
        stockDF = quandl.get("WIKI/"+app_lulu.vars['ticker'], returns='pandas', end_date=dateFormat(now), start_date=dateFormat(now-datetime.timedelta(days = 30)))
        
        p = figure(plot_width=400, plot_height=400, 
            x_axis_type = 'datetime', x_axis_label="The past Month",
            y_axis_label=app_lulu.vars["ticker"]+" Price")
        p.line(stockDF.index.values.tolist(), stockDF['Close'].values.tolist())
        return file_html(p, CDN, "myplot")
if __name__ == "__main__":
    app_lulu.run(debug=True)