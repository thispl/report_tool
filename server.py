'''
Created on Jan 10, 2017

@author: hanif
'''

from flask import Flask, flash, render_template, redirect, url_for, request, session
from module.database import Database
import requests
from datetime import date,time
# from frappeclient import FrappeClient


app = Flask(__name__)
app.secret_key = "mys3cr3tk3y"
db = Database()

@app.route('/')
def index():
    data = db.read(None)
    return render_template('index.html', data = data)

@app.route('/add/')
def add():
    return render_template('add.html')

@app.route('/synctoserver/')
def synctoserver():
    url = "http://192.9.200.162"
    timeout = 10
    try:
        request = requests.get(url, timeout=timeout)
        print("Connected to the Internet")
        # from frappeclient import FrappeClient
        # mydb = mysql.connector.connect(
        # host="localhost",
        # user="root",
        # passwd="Pa55w0rd@",
        # database="biotime"
        # )
        # mycursor = mydb.cursor(dictionary=True)
        # client = FrappeClient("http://192.9.200.162", "Administrator", "Tpl@1234")
        # query = "SELECT id,emp_code as biometric_pin,punch_time as log_time,terminal_alias as log_type,date(punch_time) as log_date,checkin_marked FROM `iclock_transaction` where emp_code is not null and checkin_marked = 0 and date(punch_time) = '%s'" % date.today()
        # mycursor.execute(query)
        # devicelog = mycursor.fetchall()
        # # print(devicelog)
        # in_list = ["HCD IN","LAB IN","PO IN"]
        # out_list = ["HCD OUT","LAB OUT","PO OUT"]
        # # print(devicelog)
        # if devicelog:
        #     if client:
        #         for d in devicelog:
        #             if d["biometric_pin"]:
        #                 employee = client.get_value("Employee","name",{"biometric_pin": d["biometric_pin"]})
        #                 if employee:
        #                     time = str((d["log_time"]).replace(second=0))
        #                     check = client.get_value("Employee Checkin",{"biometric_pin": d["biometric_pin"],"time":time})
        #                     if not check:
        #                         print(d["log_time"])
        #                         doc = {"doctype":"Employee Checkin"}
        #                         doc["log_date"] = str(d["log_date"])
        #                         doc["biometric_pin"] = str(d["biometric_pin"])
        #                         doc["employee"] = employee['name']
        #                         doc["device_area"] = str(d["log_type"])
        #                         doc["time"] = str((d["log_time"]).replace(second=0))
        #                         if d["log_type"] in in_list:
        #                             doc['log_type'] = 'IN'
        #                         if d["log_type"] in out_list:
        #                             doc['log_type'] = 'OUT'
        #                         client.insert(doc)
        #                         update_query = "update `iclock_transaction` set checkin_marked='1' where id = %s" % str(d["id"])
        #                         mycursor.execute(update_query)
        #                         mydb.commit()
        #                     else:
        #                         update_query = "update `iclock_transaction` set checkin_marked='1' where id = %s" % str(d["id"])
        #                         mycursor.execute(update_query)
                                # mydb.commit()

    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No internet connection.")
    finally:
        return redirect(url_for('index'))

@app.route('/addphone', methods = ['POST', 'GET'])
def addphone():
    if request.method == 'POST' and request.form['save']:
        if db.insert(request.form):
            flash("A new Order has been Placed")
        else:
            flash("A new Order cannot be Placed")

        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/update/<int:id>/')
def update(id):
    data = db.read(id);

    if len(data) == 0:
        return redirect(url_for('index'))
    else:
        session['update'] = id
        return render_template('update.html', data = data)

@app.route('/updatephone', methods = ['POST'])
def updatephone():
    if request.method == 'POST' and request.form['update']:

        if db.update(session['update'], request.form):
            flash('A phone number has been updated')

        else:
            flash('A phone number can not be updated')

        session.pop('update', None)

        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/delete/<int:id>/')
def delete(id):
    data = db.read(id);

    if len(data) == 0:
        return redirect(url_for('index'))
    else:
        session['delete'] = id
        return render_template('delete.html', data = data)

@app.route('/deletephone', methods = ['POST'])
def deletephone():
    if request.method == 'POST' and request.form['delete']:

        if db.delete(session['delete']):
            flash('A phone number has been deleted')

        else:
            flash('A phone number can not be deleted')

        session.pop('delete', None)

        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')

if __name__ == '__main__':
    app.run(port=8181, host="0.0.0.0")
