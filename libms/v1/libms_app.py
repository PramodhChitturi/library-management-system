from flask import Flask, render_template, redirect, url_for, request, session
from db.libms_ops import inventory_handler
import json_data
from datetime import datetime
from db.globals import *
from user.login import user_login_manager
from flask_session import Session


app = Flask('__name__')
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
# app.jinja_env.filters['zip'] = zip

@app.route('/')
def welcomepage():
    return render_template('welcomepage.html')

@app.route('/logout')
def logout():
    if session.get('user'):
        session['user'] = None
        return redirect(url_for('login'))
    else:
        session['wrong_credentials'] = 'Login First'
        return redirect(url_for('/login/user'))
        
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/user')
def user():
    return render_template('user.html')

@app.route('/userlogin', methods = ['POST'])
def userlogin():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
        is_exists, record = user_login_manager.is_user_exists(email)
        if is_exists:
            give_access = user_login_manager.check_credentials(email, password)
            if give_access:
                session['user'] = record
                session['wrong_credentials'] = ''
                return redirect(url_for('index'))
            else:
                session['wrong_credentials'] = 'Wrong Email or Password'
                return redirect(url_for('user'))
        else:
            session['wrong_credentials'] = 'User doens\'t exist'
            return redirect(url_for('user'))
@app.route('/index')
def index():
    if session.get('user'):
        return render_template('user_home.html')
    else:
        session['wrong_credentials'] = 'Login First'
        return redirect(url_for('login'))
@app.route('/forgotpassword')
def resetpass():
    return render_template('reset.html')

@app.route('/verifyotp', methods = ['POST'])
def verifyotp():
    if request.method == 'POST':
        email = request.form['email']
        otp = user_login_manager.generate_otp(email)
        if otp:
            return render_template('verifyotp.html',email = email, otp_generated = otp)
        else:
            return '''<!doctype html>
                        <html>
                            <head><title>user not found</title>
                            </head>
                            <body>
                                <h1>Library Management System</h1>
                                <h2>user not found</h2>
                            </body>
                            </html>'''
                    
@app.route('/resetpassword', methods = ['POST'])
def resetpassword():
    if request.method == 'POST':
        email = request.form['email']
        otp =  request.form['otp']
        otp_value = request.form['otp_value']
        if str(otp) == str(otp_value):
            return render_template('resetpassword.html', email = email)
        else:
            return render_template('verifyotp.html',email = email, otp_generated = otp, error = "OTP doesn't match")
@app.route('/resetoldpassword', methods = ['POST'])
def resetoldpassword():
    if request.method == 'POST':
        email = request.form['email']
        new_pass = request.form['password']
        user_login_manager.change_password(email, new_pass)
    return redirect(url_for('user'))

@app.route('/create')
def create_account():
    return render_template('createaccount.html') 
  
@app.route('/createaccount', methods = ['POST']) 
def createaccount():
    try:
        if request.method == 'POST':
            username =request.form['username']
            email = request.form['email']
            password = request.form['password']
            user_exists = user_login_manager.create_user(username, email, password)
            if user_exists:
                session['wrong_credentials'] = 'Account already exists'
                return redirect(url_for('create_account'))
            else:
                session['wrong_credentials'] = ''
                return redirect(url_for('user'))
    except Exception as e:
        print(e)
        
@app.route('/home')
def home():
    return render_template('home.html')

#returns data in json format
@app.route('/allbooks')
def books():
    data = inventory_handler.get_allbooks(INVENTORY_TABLE,result_dict= True)
    return data

@app.route('/showallbooks')
def render_all_book():
    # data = json_data.get_inventory_data()
    data = inventory_handler.get_allbooks(INVENTORY_TABLE,result_dict= True)
    record = data
    if data != []:
        headings = data[0].keys()
        values = [item.values() for item in data]
    else:
        headings = ['No boosk found']
        values = []
    return render_template('allbooks.html',title = 'List of books', headings = headings, zip = zip,record = data, data = values)

@app.route('/search', methods = ['GET'])
def search():
    try:
        if session.get('user'):
            if request.method == 'GET':
                search = request.args.get('search')
                table = request.args.get('table')
                _filter = request.args.get('filter')
                user_id = session['user']['id']
                titlereturn = request.args.get('title')
                records = inventory_handler.search(search, _filter, table, user_id)
                print(records)
                if records != []:
                    headings = records[0].keys()
                    data = [item.values() for item in records]
                else:
                    headings = ['NO RECORD FOUND']
                    data = []
                if table == INVENTORY_TABLE:
                    title = 'List of books'
                elif table == BORROW_TABLE:
                    title = 'Borrowed books info'
            if titlereturn == 'return':
                return render_template('returnbookdata.html',headings = headings, data = data, zip = zip,record = records, search = True)
            return render_template('allbooks.html',title = title, headings = headings, data = data, search = True)
        else:
            return redirect(url_for('login'))
    except Exception as e:
        print(e)

@app.route('/addbook')
def addbooks():
    return render_template('addbook.html')

@app.route('/add', methods = ['POST'])
def add():
    if request.method == 'POST':
        # id = request.form['id']
        book_name = request.form['book_name']
        author = request.form['author']
        edition = request.form['edition']
        category = request.form['category']
        description = request.form['description']
        inventory_handler.add_book_to_inventory(book_name, author, edition, category, description)
    return redirect(url_for('home'))

@app.route('/deletebook')
def delbook():
    return render_template('delbook.html')

@app.route('/delete', methods = ['POST'])
def delete():
    if request.method == 'POST':
        _id = request.form['_id']
        delete = inventory_handler.delete_record_book_inventory_table(INVENTORY_TABLE, _id)
    if delete:
        return redirect(url_for('home'))
    else:
        return '''<!doctype html>
                    <html>
                        <head>
                            <title>record not found</title>
                        </head>
                        <body>
                            <h1>record not found</h1>
                            <a href = '/home'>Go home</a>
                        </body>
                    </html>'''
                    
@app.route('/borrowbook')
def borrowbook():
    if not session.get('user'):
        return redirect(url_for('login'))
    else:
        return render_template('borrowbook.html')

@app.route('/borrow', methods = ['POST', 'GET'])
def borrow():
    if not session['user']:
        if request.method == 'POST':
            user_id = request.form['user_id']
            person = request.form['p_name']
            email = request.form['email']
            book_id = request.form['_id']
    else:
        if request.method == 'POST':
            user_id = session['user']['id']
            person = session['user']['username']
            email = session['user']['email']
            book_id = request.form['_id']
        borrow = inventory_handler.add_book_to_borrow(user_id= user_id, person = person, email = email, book_id = book_id)
        if borrow:
            return redirect(url_for('home'))
        else:
            return '''<!doctype html>
                    <html>
                        <head>
                            <title>book not available</title>
                        </head>
                        <body>
                            <h1>Book not available</h1>
                            <a href = '/home'>Go home</a>
                        </body>
                    </html>'''

@app.route('/borrowedbooksdata')
def borrowedbooks():
    if not session.get('user'):
        # return render_template('borrowbookrecord.html')
        return redirect(url_for('login'))
    else:
        return redirect(url_for('render_borrowed_books_data'))

@app.route('/booksborrowed')
def booksborrowed():
    data = inventory_handler.get_allbooks(BORROW_TABLE, result_dict = True)
    return data

@app.route('/renderborrowbooks', methods = ['GET','POST'])
def render_borrowed_books_data():
    # data = json_data.get_borrowed_data()
    if not session.get('user'):
        email = request.form['email']
    else:
        email = session['user']['email']
        data = inventory_handler.get_borrowed_books(email, result_dict = True) 
        record = data
        if data != []:
            headings = data[0].keys()
            values = [item.values() for item in data]
        else:
            headings = ['NO BOOKS FOUND']
            values = []
        return render_template('allbooks.html',title = 'Borrowed books info', headings = headings, zip = zip,record = data, data = values)

@app.route('/returnbook')
def returnbook():
    if session.get('user'):
        return redirect(url_for('returnbookdata'))
        # return render_template('returnform.html')
    else:
        return redirect(url_for('login'))
    
@app.route('/returnbookdata', methods = ['GET', 'POST'])
def returnbookdata():
    if not session.get('user'):
        if request.method == 'POST':
            email = request.form['email']
    else:
        email = session['user']['email']
        data = inventory_handler.get_borrowed_books(email, result_dict = True) 
        if data != []:
            headings = data[0].keys()
            values = [item.values() for item in data]
        else:
            headings = ['NO BOOKS FOUND']
            values = []
    return render_template('returnbookdata.html',headings = headings, data = values, zip = zip,record = data)

@app.route('/return', methods = ['GET'])
def _return():
    if request.method == 'GET':
        borrow_id = request.args.get('_id')
        book_id = request.args.get('book_id')
        returned = inventory_handler.returnbook(borrow_id, book_id)
        if returned:
            if session.get('user'):
                return redirect(url_for('index'))
            else:
                return redirect(url_for('home'))
        return '''<!doctype html>
                    <html>
                        <head>
                            <title>data not found</title>
                        </head>
                        <body>
                            <h1>data not found</h1>
                            <a href = '/home'>Go home</a>
                        </body>
                    </html>'''
                    
@app.route('/report')
def report():
    weekly_data, monthly_data = inventory_handler.report()
    headings = weekly_data[0].keys()
    weekly_data = [item.values() for item in weekly_data]
    monthly_data = [item.values() for item in monthly_data]
    return render_template('report.html', headings = headings, data_weekly = weekly_data, data_monthly = monthly_data )
    # return data

@app.route('/reservebook')
def reservebook():
    return render_template('reservebook.html')
app.run(debug = True)