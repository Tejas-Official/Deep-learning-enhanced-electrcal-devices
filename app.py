from flask import Flask, render_template, request, redirect, url_for, flash, session
#import mysql.connector as mq
#from mysql.connector import Error
from markupsafe import Markup
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import main2
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

def dbconnection():
    con = mq.connect(host='localhost', database='latecomers',user='root',password='root')
    return con

@app.route('/')
def home():
    return render_template('index.html', title='home')

@app.route('/loginpage')
def loginpage():
    return render_template('login.html',title='login')

@app.route('/login',methods=['GET','POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    if email=='admin@gmail.com' and password=='123':
        return render_template('home.html',title='home')
    else:
        message = Markup("<h3>Denied! Invalid Credentials! </h3>")
        flash(message)
        return redirect(url_for('loginpage'))
@app.route('/startdetection')
def startdetection():
    threading.Thread(target=main2.human_detection).start()
    return render_template('home.html',title='home')




if __name__ == '__main__':
    app.run(debug=True)
