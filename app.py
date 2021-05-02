from flask import Flask, render_template, request, redirect, url_for,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import date,timedelta
import re

app=Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1320476'
app.config['MYSQL_DB'] = 'nursery_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

#----------------default page when the server gets loaded-----------------
@app.route('/')
def index():
    msg=''
    return render_template('index.html')

#---------------for the error page-----------
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

#--------------signin----------------------
@app.route('/signin',methods=['GET','POST'])
def signin():
    msg=''
    if request.method == 'GET':
        return render_template('signin.html')
    if 'user_id' in request.form and 'password' in request.form:
        user_id = request.form['user_id']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from users where user_id = (%s) and password = (%s)',(user_id,password,))
        touple = cursor.fetchone()
        if touple:
            session['user_id']=touple['user_id']
            msg = 'successfully logged in'
            if password == 'P@55word#admin#':
            return render_template('adminhome.html',msg=msg)
           
            if password == 'P@55word#manager#':
                return render_template('managerhome.html',msg=msg)
            return render_template('userhome.html',msg=msg)
        msg = 'incorrect username or password'
        return render_template('signin.html',msg=msg)
    msg = 'please fill out form'
    return render_template('signin.html',msg=msg)

#-----------------signup------------------
@app.route('/signup',methods=['GET','POST'])
def signup():
    msg=''
    if request.method == 'GET':
        return render_template('signup.html')
    if 'user_id' in request.form and 'name' in request.form and 'gender' in request.form and 'address' in request.form and 'password' in request.form:
        name = request.form['name']
        user_id = request.form['user_id']
        gender = request.form['gender']
        password = request.form['password']
        address = request.form['address']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * for users where user_id = (%s)',(user_id))
        exists = cursor.fetchone()
        if exists:
            msg = 'this phone number is already in use'
            return render_template('signup.html',msg=msg)
        cursor.execute('insert into users values (%s,%s,%s,%s,%s)',(name,user_id,gender,password,address,))
        mysql.connection.commit()
        msg = 'successfully registered'
        if password == 'P@55word#admin#':
            return render_template('adminhome.html',msg=msg)
           
        if password == 'P@55word#manager#':
             return render_template('managerhome.html',msg=msg)
        return render_template('userhome.html',msg=msg)
        
    msg = 'please fill out form'
    return render_template('signup.html',msg=msg)
    
             

