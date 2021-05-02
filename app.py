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

#---------------shop by search---------------
@app.route('/shopbysearch/<product_type>',methods['GET']) 
def shopbysearch(product_type):
    msg = ''
    if product_type == 'plants' or product_type =='seeds' or product_type == 'fertilizers' or product_type == 'accessories':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from products where product_type = (%s)',(product_type,))
        products = cursor.fetchall()
        if products:
            return render_template('shop.html',products=products)
        msg=str(product_type)+ ' are out of stock'
        render_template('shop.html',msg = msg)
    msg = "no such services avaliable"
    return render_template('shop.html',msg=msg)

#------------shop---------------------
@app.route('/shop',methods=['GET'])
def shop():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select * from products')
    products = cursor.fetchall()
    if products:
        return render_template('shop.html',products=products)
    msg='All types of products are out of stock'
    render_template('shop.html',msg = msg) 

#-------------order and payment-----------------
@app.route('/orders/<product_id>'methods=['GET','POST'])
def orders(product_id):
    msg=''
    if 'user_id' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.Dictcursor)
        cursor.execute('select * from products where product_id = (%s)',(product_id,))
        product = cursor.fetchone()
        cursor.execute('select sum(order_quantity) as quantity from orders where product_id=(%s)',(product_id,))
        already_ordered = cursor.fetchone()
        avaliable_product_quantity = int(product['quantity'])-int(already_ordered['quantity'])
        if request.method == 'GET':
            return render_template('discription.html',product=product,avaliable_product_quantity=avaliable_product_quantity)
        if 'cvv' in request.form and 'card_number' in request.form and 'amount' in request.form and 'quantity' in request.form:
            ordered_date=date.today()
            cursor.execute(select * from payment where card_number=(%s) and cvv=(%s) and user_id=(%s),(card_number,cvv,session['user_id'],))
            credentials=cursor.fetchone()
            if credentials:
                m = (  int(quantity)  )*( int(product['cost']) )
                if (int(credentials['balance']))>=m
                    if quantity<=avaliable_product_quantity:
                        cursor.execute('insert into orders values (%s,%s,%s,%s)',(session['user_id'],product_id,quantity,ordered_date,))
                        mysql.connection.commit()
                        balance = int(credentials['balance'])-m
                        cursor.execute('update payment set balance=(%s) where user_id=(%s) and card_number=(%s)',(balance,session['user_id'],card_number,))
                        avaliable_product_quantity = avaliable_product_quantity - int(quantity)
                        msg = 'successfully ordered'
                        return render_template('discription.html',product=product,avaliable_product_quantity=avaliable_product_quantity,msg=msg)
                    msg = 'quantity is more than avaliability'
                    return render_template('discription.html',product=product,avaliable_product_quantity=avaliable_product_quantity,msg=msg)
                msg = "you dont have enough money"
                return render_template('discription.html',product=product,avaliable_product_quantity=avaliable_product_quantity,msg=msg)
            msg = 'incorrect card number or cvv'
            return render_template('discription.html',product=product,avaliable_product_quantity=avaliable_product_quantity,msg=msg)    
        msg = 'fill out details'
        return render_template('discription.html',product=product,avaliable_product_quantity=avaliable_product_quantity,msg=msg)
    msg = 'please signin before ordering'
    return render_template('signin.html',msg=msg)
#------------myorders---------------
@app.route('/myorders')
def myorders():
    msg=''
    if 'user_id' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from orders where user_id = (%s)',(session['user_id'],))
        my_orders = cursor.fetchall()
        if my_orders:
            msg='your orders'
            return render_template('myorders.html',msg=msg)
        msg='no orders yet'
        return render_template('myorders.html',msg=msg)
    msg = 'please signin to check orders'
    return render_template('signin.html',msg = msg)
#------------add_to_cart------------
#------------my_cart----------------
#-----------remove_from_cart--------
#----------reviews
    

    

