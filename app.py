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
@app.route('/index')
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
            session['loggedin'] = True
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
        cursor.execute('select * from users where user_id = (%s)',(user_id,))
        exists = cursor.fetchone()
        if exists:
            msg = 'this phone number is already in use'
            return render_template('signup.html',msg=msg)
        cursor.execute('insert into users values (%s,%s,%s,%s,%s)',(name,user_id,gender,password,address,))
        mysql.connection.commit()
        session['user_id']='user_id'
        msg = 'successfully registered'
        if password == 'P@55word#admin#':
            return render_template('adminhome.html',msg=msg)
           
        if password == 'P@55word#manager#':
            return render_template('managerhome.html',msg=msg)
        return render_template('userhome.html',msg=msg)
        
    msg = 'please fill out form'
    return render_template('signup.html',msg=msg)


#----------------logout----------------------
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))
    return render_template('index.html')


#---------------shop by search---------------
@app.route('/shopbysearch',methods=['POST']) 
def shopbysearch():
    msg = ''
    if 'product_type' in request.form:
        product_type = request.form['product_type']
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
    msg = "please fill details"
    return render_template('shop.html',msg=msg)


#------------shop---------------------
@app.route('/shop',methods=['GET'])
def shop():
    msg=''
    if 'user_id' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from products')
        products = cursor.fetchall()
        if products:
            return render_template('shop.html',products=products,msg=msg)
        msg='All types of products are out of stock'
        render_template('shop.html',products=products,msg = msg) 
    msg='login '
    return render_template('shop.html',products=products,msg=msg)


#-------------order and payment-----------------
@app.route('/orders/<product_id>',methods=['GET','POST'])
def orders(product_id):
    msg=''
    if 'user_id' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from products where product_id = (%s)',(product_id,))
        product = cursor.fetchone()
        p= int( str(product['product_quantity']) )
        cursor.execute('select sum(order_quantity) as quantity from orders where product_id=(%s)',(product_id,))
        already_ordered = cursor.fetchone()
        q=0
        if already_ordered['quantity']=='null':
            q=0
        q=int(  str(already_ordered['quantity'])   )
        avaliable_product_quantity = p-q
        if request.method == 'GET':
            return render_template('discription.html',product=product,avaliable_product_quantity=avaliable_product_quantity)
        if 'cvv' in request.form and 'card_number' in request.form and 'quantity' in request.form:
            quantity = request.form['quantity']
            cvv = request.form['cvv']
            card_number = request.form['card_number']
            ordered_date=date.today()
            cursor.execute('select * from payment where card_number=(%s) and cvv=(%s) and user_id=(%s)',(card_number,cvv,session['user_id'],))
            credentials=cursor.fetchone()
            if credentials:
                m = (  int(quantity)  )*( int(product['cost']) )
                if (int(credentials['balance']))>=m:
                    if int(quantity)<=avaliable_product_quantity:
                        cursor.execute('insert into orders values (%s,%s,%s,%s)',(session['user_id'],product_id,quantity,ordered_date,))
                        mysql.connection.commit()
                        balance = int(credentials['balance'])-m
                        cursor.execute('update payment set balance=(%s) where user_id=(%s) and card_number=(%s)',(balance,session['user_id'],card_number,))
                        mysql.connection.commit()
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
            return render_template('myorders.html',my_orders=my_orders,msg=msg)
        msg='no orders yet'
        return render_template('myorders.html',msg=msg)
    msg = 'please signin to check orders'
    return render_template('signin.html',msg = msg)


#----------------checking reviews-------------------
@app.route('/checkreview/<product_id>',methods=['GET'])
def checkreview(product_id):
    msg = ''
    if 'user_id' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from products where product_id=(%s)',(product_id,))
        product = cursor.fetchone()
        cursor.execute('select * from reviews where product_id=(%s)',(product_id,))
        reviews = cursor.fetchall()
        if reviews:
            msg='these are the reviews given by the users on this product'
            return render_template('checkreview.html',product=product,reviews = reviews,msg= msg)
        msg = 'no reviews yet on this product'
        return render_template('checkreview.html',product=product,reviews = reviews,msg= msg)
    msg='signin to check reviews'
    return render_template('signin.html',msg=msg)


#------------give review------------
@app.route('/givereview/<product_id>',methods = ['GET','POST'])
def givereview(product_id):
    msg = ''
    if 'user_id' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from products where product_id = (%s)',(product_id,))
        product = cursor.fetchone()
        if request.method=='GET':
            return render_template('givereview.html',product = product,msg=msg)
        if 'discription' in request.form and 'rating' in request.form :
            discription = request.form['discription']
            rating = request.form['rating']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('insert into reviews values(%s,%s,%s,%s)',(product_id,session['user_id'],rating,discription,))
            mysql.connection.commit()
            msg = 'successfully reviewed'
            return render_template('givereview.html',product = product,msg=msg)
        msg = 'fil out form'
        return render_template('givereview.html',product = product,msg=msg)
    msg = 'signin to give review'
    return render_template('signin.html',msg=msg)


#------------add_to_cart------------
@app.route('/add_to_cart/<product_id>',methods=['GET'])
def add_to_cart(product_id):
    msg=''
    if 'user_id' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from cart where user_id=(%s) and product_id=(%s)',(session['user_id'],product_id,))
        exists = cursor.fetchone()
        if not exists:
            cursor.execute('insert into cart values(%s,%s)',(session['user_id'],product_id,))
            mysql.connection.commit()
            msg = 'successfully added'
            return render_template('exists.html',msg=msg)
        msg='it already exists'
        return render_template('exists.html',msg=msg)
    msg='login to add to cart'
    return render_template('signin.html',msg=msg)        


#------------my_cart----------------
@app.route('/mycart',methods=['GET'])
def mycart():
    msg=''
    if 'user_id' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from cart where user_id=(%s)',(session['user_id'],))
        products = cursor.fetchall()
        if products:
            msg = 'your cart items'
            return render_template('mycart.html',products=products,msg=msg)
        msg='no items in your cart'
        return render_template('mycart.html',msg=msg)
    msg='signin to check cart'
    return render_template('signin.html',msg=msg)


#-----------remove_from_cart--------
@app.route('/remove/<product_id>',methods=['GET'])
def remove(product_id):
    msg=''
    if 'user_id' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('delete from cart where user_id=(%s) and product_id=(%s)',(session['user_id'],product_id))
        mysql.connection.commit()
        msg='removed from cart successfully'
        return render_template('exists.html',msg=msg)
    msg='singin to remove product from cart'
    return render_template('signin.html',msg=msg)


#------------profile------------------
@app.route('/profile',methods=['GET'])
def profile():
    msg=''
    if 'user_id' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from users where user_id=(%s)',(session['user_id'],))
        user = cursor.fetchone()
        return render_template('profile.html',user=user)
    msg = 'signin to display profile'
    return render_template('signin.html',msg=msg)

#----------updateprofile-------------
@app.route('/updateprofile',methods=['GET','POST'])
def updateprofile():
    msg=''
    if 'user_id' in session:
        if request.method=='GET':
            return render_template('updateprofile.html',msg=msg)
        if 'name' in request.form and 'gender' in request.form and 'password' in request.form and  'address' in request.form:
            name = request.form['name']
            gender = request.form['gender']
            password = request.form['password']
            address = request.form['address']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('update users set name=(%s) ,gender=(%s) ,password=(%s) ,address=(%s) where user_id=(%s)',(name,gender,password,address,session['user_id'],))
            mysql.connection.commit()
            msg = 'successfully updated'
            return redirect(url_for('profile'))
        msg='fillout form'
        return render_template('updateprofile.html',msg=msg)
    msg='login to update profile'
    return render_template('signin.html',msg=msg)

#----------------wallet----------
@app.route('/wallet')
def wallet():
    msg=''
    if 'user_id' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select sum(balance) as amount from payment where user_id=(%s)',(session['user_id'],))
        balance=cursor.fetchone()
        if balance['amount']=='null':
            return render_template('wallet.html',balance=0)
        return render_template('wallet.html',balance = balance['amount'])
        return render_template('wallet.html')
    msg='signin to check wallet'
    return render_template('signin',msg=msg)

#------------mycards-------------
@app.route('/mycards')
def mycards():
    msg=''
    if 'user_id' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from payment where user_id=(%s)',(session['user_id'],))
        cards = cursor.fetchall()
        if cards:
            msg='your cards'
            return render_template('mycards.html',cards=cards,msg=msg)
        msg='no cards yet'
        return render_template('mycards.html',msg=msg)
    msg='signin to check cards'
    return render_template('signin',msg=msg)
#-------------removecard------------------
#-------------addbalance--------------------
#if request.method=='GET':
#    return render_template('addbalance.html')
#if 'card_number' in request.form and 'cvv' in request.form and 'balance' in request.form:
#    card_number=request.form['card_number']
#    cvv = request.form['cvv']
#    balance = request.form['balance']
#   cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#  cursor.execute('select * from payment where user_id=(%s) and card_number=(%s) and cvv=(%s)',(session['user_id'],card_number,cvv,))
# exists = cursor.fetchone()
# if exists:
#msg='invald credentials'
#return render_template('addbalance.html',msg=msg)

#----------------add admins---------
#----------------add products to ware house---------
#-----------------add products to web------------

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host ="localhost", port = int("5000"))

    

    

