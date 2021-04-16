'''
Created on Jan 10, 2017

@author: hanif
'''

from flask import Flask, flash, render_template, redirect, url_for, request, session
from module.database import Database
import requests
from datetime import date,time
import datetime
from waitress import serve



app = Flask(__name__)
app.secret_key = "mys3cr3tk3y"
db = Database()

@app.route('/')
def index():
    data = db.read(None)
    datalist = [list(i) for i in data]
    for dlist in datalist:
        shift = 'NA'
        punchdate = dlist[1]
        punchtime = dlist[1].time()
        logtype = dlist[2]
        if logtype == 'HDC In':
            if punchtime > time(7, 00, 0) and punchtime < time(10, 00,00):
                shift = 'I'
            if punchtime > time(16, 00, 00) and punchtime < time(19, 00,00):
                shift = 'II'
            if punchtime > time(00, 00, 1) and punchtime < time(4, 00,00):
                shift = u'III'
                punchdate = dlist[1] - datetime.timedelta(1)
        dlist[1] = punchdate 
        dlist.append(shift)
    datatuple = tuple(datalist)
    
    return render_template('index.html', data = datatuple)

serve(app, host='0.0.0.0', port=8080, threads=1) #WAITRESS!

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')

if __name__ == '__main__':
    app.run(port=8181, host="0.0.0.0")
