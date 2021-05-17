from flask import Flask, render_template, request, redirect, url_for,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import date,timedelta
import re

app=Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'nursery_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


#----------------default page when the server gets loaded------------------------------------------
@app.route('/')
@app.route('/index')
def index():
    msg=''
    return render_template('index.html')


#---------------for the error page----------------------------------------------------------------
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


#--------------signin-----------------------------------------------------------------------------
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
            if touple['category'] == 'P@55word#admin#':
                return redirect(url_for('adminhome'))
            if touple['category'] == 'P@55word#manager#':
                return redirect(url_for('managerhome'))
            if touple['category'] == 'P@55word#delboy#':
                return redirect(url_for('delboyhome'))
            if touple['category'] == 'P@55word#bankmanager#':
                return redirect(url_for('bankmanagerhome'))
            return redirect(url_for('userhome'))
        msg = 'incorrect username or password'
        return render_template('signin.html',msg=msg)
    msg = 'please fill out form'
    return render_template('signin.html',msg=msg)

#---------------adminhome----------------
@app.route('/adminhome',methods=['GET'])
def adminhome():
    msg='successfully logged in'
    return render_template('adminhome.html',msg=msg)

#---------------managerhome----------------
@app.route('/managerhome',methods=['GET'])
def managerhome():
    msg='successfully logged in'
    return render_template('managerhome.html',msg=msg)

#---------------bankmanagerhome----------------
@app.route('/bankmanagerhome',methods=['GET'])
def bankmanagerhome():
    msg='successfully logged in'
    return render_template('bankmanagerhome.html',msg=msg)

#---------------delboyhome----------------
@app.route('/delboyhome',methods=['GET'])
def delboyhome():
    msg='successfully logged in'
    return render_template('delboyhome.html',msg=msg)

#---------------userhome----------------
@app.route('/userhome',methods=['GET'])
def userhome():
    msg='successfully logged in'
    return render_template('userhome.html',msg=msg)

#-----------------signup-------------------------------------------------------------
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
        cursor.execute('insert into users values (%s,%s,%s,%s,%s,%s)',(name,user_id,gender,password,'##',address,))
        mysql.connection.commit()
        session['user_id']=user_id
        msg = 'successfully registered'   
        return redirect(url_for('userhome'))
    msg = 'please fill out form'
    return render_template('signup.html',msg=msg)


#----------------logout---------------------------------------------------------------
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))
    return render_template('index.html')


#---------------shop by search--------------------------------------------------------
@app.route('/shopbysearch',methods=['GET','POST']) 
def shopbysearch():
    msg = ''
    if 'product_type' in request.form:
        product_type = request.form['product_type']
        if product_type == "plant" or product_type =="seeds" or product_type == "fertilizers" or product_type == "accessories":
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('select * from products where product_type = (%s)',(product_type,))
            products = cursor.fetchall()
            if products:
                return render_template('shop.html',products=products)
            msg=str(product_type)+ ' are out of stock'
            render_template('shop.html',msg = msg)
        msg = "no such services avaliable"
        return render_template('exists.html',msg=msg)
    msg = "please fill details"
    return render_template('shop.html',msg=msg)


#------------shop---------------------------------------------------------------------------
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


#-------------order and payment-----------------------------------------------------------------
@app.route('/orders/<product_id>',methods=['GET','POST'])
def orders(product_id):
    msg=''
    if 'user_id' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from products where product_id = (%s)',(product_id,))
        product = cursor.fetchone()
        p= int( str(product['product_quantity']) )
        cursor.execute('select sum(order_quantity) as quantity from orders where product_id=(%s) and status<>(%s)',(product_id,'return',))
        already_ordered = cursor.fetchone()
        q=0
        if str(already_ordered['quantity'])=='None':
            q=0
        else :
            q=int(  str(already_ordered['quantity'])   )
        avaliable_product_quantity = p-q
        if request.method == 'GET':
            return render_template('discription.html',product=product,avaliable_product_quantity=avaliable_product_quantity)
        if 'cvv' in request.form and 'card_number' in request.form and 'quantity' in request.form:
            quantity = request.form['quantity']
            cvv = request.form['cvv']
            card_number = request.form['card_number']
            ordered_date=date.today()
            received_date=date.today()+timedelta(days=+10)
            cursor.execute('select * from cards where card_number=(%s) and cvv=(%s) and user_id=(%s)',(card_number,cvv,session['user_id'],))
            credentials=cursor.fetchone()
            if credentials:
                cursor.execute('select * from account where user_id=(%s)',(session['user_id'],))
                cre=cursor.fetchone()
                if cre:
                    m = (  int(quantity)  )*( int(product['cost']) )
                    n=(int(cre['balance']))
                    if n>=m:
                        if int(quantity)<=avaliable_product_quantity:
                            cursor.execute('insert into orders values (%s,%s,%s,%s,%s,%s,%s)',(session['user_id'],product_id,'pending',quantity,ordered_date,m,received_date,))
                            mysql.connection.commit()
                            cursor.execute('update account set balance=(%s) where user_id=(%s)',(n-m,session['user_id']))
                            mysql.connection.commit()
                            avaliable_product_quantity = avaliable_product_quantity - int(quantity)
                            msg = 'successfully ordered'
                            return render_template('discription.html',product=product,avaliable_product_quantity=avaliable_product_quantity,msg=msg)
                        msg = 'quantity is more than avaliability'
                        return render_template('discription.html',product=product,avaliable_product_quantity=avaliable_product_quantity,msg=msg)
                    msg = "you dont have enough money"
                    return render_template('discription.html',product=product,avaliable_product_quantity=avaliable_product_quantity,msg=msg)
                msg='you may not have banl account'
                return render_template('discription.html',product=product,avaliable_product_quantity=avaliable_product_quantity,msg=msg) 
            msg = 'incorrect card number or cvv'
            return render_template('discription.html',product=product,avaliable_product_quantity=avaliable_product_quantity,msg=msg)    
        msg = 'fill out details'
        return render_template('discription.html',product=product,avaliable_product_quantity=avaliable_product_quantity,msg=msg)
    msg = 'please signin before ordering'
    return render_template('signin.html',msg=msg)



#--------------delivaring product to customer--------------------------------------------------------------
@app.route('/delivery',methods=['GET','POST'])
def delivery():
    msg=''
    if 'user_id' in session:
        if request.method=='GET':
            return render_template('delivery.html',msg=msg)
        if 'product_id' in request.form and 'user_id' in request.form and 'date_booked' in request.form and 'quantity' in request.form:
            product_id=request.form['product_id']
            user_id=request.form['user_id']
            date_booked=request.form['date_booked']
            quantity = request.form['quantity']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('select * from orders where product_id=(%s) and user_id=(%s) and order_quantity=(%s) and ordered_date=(%s) and status=(%s)',(product_id,user_id,quantity,date_booked,'pending',))
            exists=cursor.fetchone()
            if exists:
                today=date.today()
                cursor.execute('update orders set status=(%s),received_date=(%s)  where product_id=(%s) and user_id=(%s) and order_quantity=(%s) and ordered_date=(%s) and status=(%s)',('received',today,product_id,user_id,quantity,date_booked,'pending',))
                mysql.connection.commit()
                msg='sucessful'
                return render_template('delivery.html',msg=msg)
            msg='in valid order'
            return render_template('delivery.html',msg=msg) 
        msg='fill details'
        return render_template('delivery.html',msg=msg)
    msg='login to deliver products'
    return render_template('signin.html')


#------------myorders-------------------------------------------------------------------------------
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


#----------------checking reviews-----------------------------------------------------------
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


#------------give review------------------------------------------------------------------------------
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
            if int(rating)<=5:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('insert into reviews values(%s,%s,%s,%s)',(product_id,session['user_id'],rating,discription,))
                mysql.connection.commit()
                msg = 'successfully reviewed'
                return render_template('givereview.html',product = product,msg=msg)
            msg='rating cant be greater than 5'
            return render_template('givereview.html',product = product,msg=msg)
        msg = 'fil out form'
        return render_template('givereview.html',product = product,msg=msg)
    msg = 'signin to give review'
    return render_template('signin.html',msg=msg)


#------------add_to_cart----------------------------------------------------------------------
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


#------------my_cart-----------------------------------------------------------------------
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


#-----------remove_from_cart-------------------------------------------------------------
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


#------------profile--------------------------------------------------------------------------
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

#----------updateprofile-------------------------------------------------------------------------
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

#----------------wallet---------------------------------------------------------------------------
@app.route('/wallet')
def wallet():
    msg=''
    if 'user_id' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from account where user_id=(%s)',(session['user_id'],))
        person=cursor.fetchone()
        if person:
            if person['balance']=='null':
                return render_template('wallet.html',balance=0)
            return render_template('wallet.html',balance = person['balance'])
        msg='you dont have account'
        return render_template('wallet.html',msg=msg)
    msg='signin to check wallet'
    return render_template('signin',msg=msg)

#------------mycards------------------------------------------------------------------------
@app.route('/mycards')
def mycards():
    msg=''
    if 'user_id' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from cards where user_id=(%s)',(session['user_id'],))
        cards = cursor.fetchall()
        if cards:
            msg='your cards'
            return render_template('mycards.html',cards=cards,msg=msg)
        msg='no cards yet'
        return render_template('mycards.html',msg=msg)
    msg='signin to check cards'
    return render_template('signin',msg=msg)




#-------------addbalance----------------------------------------------------------------------
@app.route('/addbalance',methods=['GET','POST'])
def addbalance():
    msg=''
    if 'user_id' in session:
        if request.method=='GET':
            return render_template('addbalance.html',msg=msg)
        if 'user_id' in request.form and 'balance' in request.form:
            user_id=request.form['user_id']
            balance=request.form['balance']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('select * from users where user_id=(%s)',(user_id,))
            person = cursor.fetchone()
            if person:
                cursor.execute('select * from account where user_id=(%s)',(user_id,))
                exists = cursor.fetchone()
                if exists:
                    x=int(exists['balance'])+ int(balance)
                    cursor.execute('update account set balance=(%s) where user_id=(%s)',(x,user_id,))
                    mysql.connection.commit()
                    msg='successfully added balance'
                    return render_template('addbalance.html',msg=msg)
                cursor.execute('insert into account values(%s,%s)',(balance,user_id,))
                mysql.connection.commit()
                msg='successfully added balance'
                return render_template('addbalance.html',msg=msg)
            msg='person doesnt exists'
            return render_template('addbalance.html',msg=msg)
        msg='fill details'
        return render_template('addbalance.html',msg=msg)
    msg="login first"
    return render_template('signin.html',msg=msg)
        

#----------------add card------------------------------------------------------------------------
@app.route('/addcard',methods=['GET','POST'])
def addcard():
    msg=''
    if 'user_id' in session:
        if request.method=='GET':
            return render_template('addcard.html',msg=msg)
        if 'card_number' in request.form and 'user_id' in request.form and 'cvv' in request.form:
            user_id = request.form['user_id']
            card_number=request.form['card_number']
            cvv=request.form['cvv']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('select * from users where user_id=(%s)',(user_id,))
            person = cursor.fetchone()
            if person:
                cursor.execute('insert into cards values(%s,%s,%s)',(card_number,cvv,user_id,))
                mysql.connection.commit()
                msg='successfully added card'
                return render_template('addcard.html',msg=msg)
            msg='person doesnt exists'
            return render_template('addcard.html',msg=msg) 
        msg='fill details'
        return render_template('addcard.html',msg=msg)
    msg="login first"
    return render_template('signin.html',msg=msg)


#----------------adding fresh colleges---------------------------------------------------
@app.route('/addadmin',methods=['GET','POST'])
def addadmin():
    msg=''
    if 'user_id' in session:
        if request.method=='GET':
            return render_template('addadmins.html',msg=msg)
        if 'user_id' in request.form and 'name' in request.form and 'gender' in request.form and 'password' in request.form and 'category' in request.form and 'address' in request.form:
            cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            if request.form['category']=='manager':
                cursor.execute('insert into users values(%s,%s,%s,%s,%s,%s)',(request.form['name'],request.form['user_id'],request.form['gender'],request.form['password'],'P@55word#manager#',request.form['address'],))
                mysql.connection.commit()
                msg='sucessfully added manager'
                return render_template('managerhome.html',msg=msg)
            elif request.form['category']=='admin':
                cursor.execute('insert into users values(%s,%s,%s,%s,%s,%s)',(request.form['name'],request.form['user_id'],request.form['gender'],request.form['password'],'P@55word#admin#',request.form['address'],))
                mysql.connection.commit()
                msg='sucessfully added admin'
                return render_template('managerhome.html',msg=msg)
            elif request.form['category']=='delivery boy':
                cursor.execute('insert into users values(%s,%s,%s,%s,%s,%s)',(request.form['name'],request.form['user_id'],request.form['gender'],request.form['password'],'P@55word#delboy#',request.form['address'],))
                mysql.connection.commit()
                msg='sucessfully added delivary'
                return render_template('managerhome.html',msg=msg)
            else:
                msg='invalid proffesion'
                return render_template('addadmins.html',msg=msg)
        msg='fill details'
        return render_template('addadmins.html',msg=msg)
    msg='signin first'
    return render_template('signin.html',msg=msg)


#----------------add products to ware house-----------------------------------------------------
@app.route('/addproducts_',methods=['GET','POST'])
def addproducts_():
    msg=''
    if 'user_id' in session:
        if request.method=='GET':
            return render_template('addproducts_.html',msg=msg)
    if  'a' in request.form and 'b' in request.form and 'c' in request.form:
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from warehouse where product_id=(%s) and ware_house_address=(%s) and date_added=(%s) and quantity=(%s)',(request.form['a'],request.form['b'],date.today(),request.form['c'],))
        exists=cursor.fetchone()
        cursor.execute('insert into warehouse values(%s,%s,%s,%s,%s)',(request.form['a'],request.form['b'],request.form['c'],session['user_id'],date.today(),))
        mysql.connection.commit()
        msg='successfully added'
        return render_template('adminhome.html',msg=msg)
    msg='fill the form'
    return render_template('addproducts_.html',msg=msg)
    msg='signin to addproducts_'
    return render_template('signin.html',msg=msg)

#-----------------add products to web---------------------------------------------------
@app.route('/addproducts',methods=['GET','POST'])
def addproducts():
    msg=''
    if 'user_id' in session:
        if request.method=='GET':
            return render_template('addproducts.html',msg=msg)
    if  'a' in request.form and 'b' in request.form and 'c' in request.form and 'd' in request.form and 'e' in request.form:
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from warehouse where product_id=(%s) and quantity=(%s) and date_added=(%s)',(request.form['a'],request.form['b'],date.today(),))
        exists=cursor.fetchone()
        if exists:
            cursor.execute('select * from products where product_id=(%s)',(request.form['a'],))
            exists=cursor.fetchone()
            if exists:
                quantity = int(request.form['b']) + int(exists['product_quantity'])
                cursor.execute('update products set product_quantity=(%s)',(quantity,))
                mysql.connection.commit()
                msg='successfully added'
                return render_template('managerhome.html',msg=msg)
            cursor.execute('insert into products values(%s,%s,%s,%s,%s)',(request.form['a'],request.form['b'],request.form['c'],request.form['d'],request.form['e'],))
            mysql.connection.commit()
            msg='successfully added'
            return render_template('managerhome.html',msg=msg)
        msg='no such products exists in warehouse'
        return render_template('managerhome.html',msg=msg)
    msg='fill the form'
    return render_template('addproducts.html',msg=msg)
    msg='signin to add products'
    return render_template('signin.html',msg=msg)



if __name__ == '__main__':
    app.run(debug=True)
    app.run(host ="localhost", port = int("5000"))

    

    

