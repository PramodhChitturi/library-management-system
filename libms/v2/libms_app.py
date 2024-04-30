from flask import Flask, render_template, redirect, url_for, request, session
from flask_session import Session
from user.login import user_login
from user.user_ops import user
from db.libms_ops import inventory_handler
from json_data import *
from remindersystem import reminder
from graphs import graph
from datetime import datetime


app = Flask(__name__)
app.config['SESSIOIN_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')
def welcomepage():
    session['load_url'] = request.url
    session['wrong_credentials'] = ''
    return render_template('welcome_page.html')

@app.route('/profile')
def profile():
    if session.get('user'):
        return render_template('profile.html')
    else:
        return redirect(url_for('login'))
        
@app.route('/login')
def login():
    if not session.get('user'):
        return render_template('login.html')
    else:
        return redirect(url_for('profile'))

@app.route('/logout')
def logout():
    if session.get('user'):
        session['user'] = None
        return redirect(session['load_url'])
        # return redirect(request.url)
    else:
        return redirect('/home')
    
@app.route('/authentication', methods = ['POST'])
def authentication():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_exists = user.is_user_exists(email)
        print('user_exists =', user_exists)
        if user_exists:
            verfied, record = user_login.user_verfication(email, password)
            if verfied:
                session['user'] = record
                print('record =',record)
                session['wrong_credentials'] = ''
                return redirect(session['load_url'])
            else:
                session['wrong_credentials'] = 'Wrong Email and Password'
                return redirect(url_for('login'))
        else:
            session['wrong_credentials'] = 'User doesn\'t exists'
            return redirect(url_for('login'))

@app.route('/createaccount')
def createaccount():
        return render_template('createaccount.html')

@app.route('/createuser', methods = ['POST'])
def createuser():
    if request.method == 'POST':
        session['wrong_account'] = ''
        username = request.form['name']
        email = request.form['email']
        if session['user'] and session['user']['role'] == 'ADMIN':
            password = 'libms@123'
        else:
            password = request.form['password']
        is_exists = user.is_user_exists(email)
        if is_exists:
            session['wrong_account'] = 'Account already exist'
            return redirect(url_for('createaccount'))
        else:
            session['wrong_account'] = ''
            user_login.create_user(username, email, password)
            if session['user'] and session['user']['role'] == 'ADMIN':
                reminder.send_libms_pass(email)
        if session['user']:
            if session['user']['role'] == 'ADMIN':
                return redirect(session['load_url'])
        else:
            return redirect(url_for('login'))
    
@app.route('/reset')
def reset():
    return render_template('forgot_password.html')

@app.route('/generateotp', methods = ['POST'])
def generate_otp():
    if request.method == 'POST':
        session['wrong_otp'] = ''
        email = request.form['email']
        session['email'] = email
        otp = user_login.forgot_password(email)
        if otp :
            print('otp =', otp)
            session['wrong_email'] = ''
            session['otp'] = otp
            return render_template('verify_otp.html')
        else:
            session['wrong_email'] = 'Account doesn\'t exist'
            return redirect(url_for('reset'))
        

@app.route('/forgotpassword', methods = ['POST'])
def forgot_password():
    if request.method == 'POST':
        session['wrong_otp'] = ''
        user_otp = request.form['otp']
        print('user_otp =', user_otp)
        if int(session['otp']) == int(user_otp):
            return render_template('change_password.html')
        else:
            session['wrong_otp'] = 'OTP doesn\'t match'
            return render_template('verify_otp.html')

@app.route('/changepassword', methods = ['POST'])
def change_password():
    if request.method == 'POST':
        new_password = request.form['new_password']
        email = session['email']
        print('email =', email)
        user_login.change_password(email, new_password)
        return redirect(url_for('login'))

@app.route('/home')
def home():
    session['load_url'] = request.url
    print('session[load_url] =', session['load_url'])
    session['wrong_credentials'] = ''
    return render_template('home.html')

@app.route('/allbooksdata')
def allbooksdata():
    data = inventory_handler.get_all_books()
    return data
    # if session.get('user'):
    #     if session['user']['role'] == 'ADMIN':
    #         return data
    #     else:
    #         return ('''         <!doctype html>
    #                             <html>
    #                             <head>
    #                             <title>All books data</title>
    #                             </head>
    #                             <body>
    #                             <h3>Permission denied</h3>
    #                             </body>
    #                             </html>
    #                             ''')
    # else:
    #     return '''<!doctype html>
    #                            <html>
    #                            <head>
    #                            <title>All books data</title>
    #                            </head>
    #                            <body>
    #                            <h3>Need permission</h3>
    #                            <a href = '/login'>Login</a> first
    #                            </body>
    #                            </html>
    #                            '''
@app.route('/showallbooks')
def showallbooks():
    session['load_url'] = request.url
    headings = ['ID', 'Book name', 'Author', 'Edition', 'Category', 'Description', 'Created at', 'Count', 'Book available', 'Availability']
    data = get_all_books()
    return render_template('showallbooks.html', headings = headings, data = data)

@app.route('/addbook')
def addbook():
    session['load_url'] = request.url
    if session['user']:
        if session['user']['role'] == 'ADMIN':
            return render_template('addbook.html')
        else:
            return ('''<!doctype html>
                       <html>
                       <head>
                       <title>add book</title>
                       </head>
                       <body>
                       <h3>Permission denied</h3>
                       <a href = '/home'>Home</a>
                       </body>
                       </html>''')
    else:
        return '''<!doctype html>
                    <html>
                    <head>
                    <title>add book</title>
                    </head>
                    <body>
                    <h3>Need permission</h3>
                    <a href = '/login'>Login</a> first
                    </body>
                    </html>'''

@app.route('/add', methods = ['POST'])
def add():
    if session['user']:
        if session['user']['role'] == 'ADMIN':
            if request.method == 'POST':
                book_name = request.form['book_name']
                author = request.form['author']
                edition = request.form['edition']
                category = request.form['category']
                description = request.form['description']
                is_added = inventory_handler.addbook(book_name, author, edition, category, description)
                if is_added:
                    record = inventory_handler.get_book(book_name, edition)
                    book_id = record[0]['id']
                    reminder.send_mail_to_reserved(book_id)
            return redirect(url_for('home'))
        else:
            return '''<!doctype html>
                        <html>
                        <head>
                        <title>add book</title>
                        </head>
                        <body>
                        <h3>Permission denied</h3>
                        <a href = '/home'>Home</a>
                        </body>
                        </html>'''
    else:
        return '''<!doctype html>
                        <html>
                        <head>
                        <title>add book</title>
                        </head>
                        <body>
                        <h3>Need permission</h3>
                        <a href = '/login'>login</a> first
                        </body>
                        </html>'''
                    
@app.route('/deletebook')
def deletebook():
    session['load_url'] = request.url
    if session['user']:
        if session['user']['role'] == 'ADMIN':
            return render_template('delbook.html')
        else:
            return ('''<!doctype html>
                       <html>
                       <head>
                       <title>add book</title>
                       </head>
                       <body>
                       <h3>Permission denied</h3>
                       <a href = '/home'>Home</a>
                       </body>
                       </html>''')
    else:
        return '''<!doctype html>
                    <html>
                    <head>
                    <title>delete book</title>
                    </head>
                    <body>
                    <h3>Need permission</h3>
                    <a href = '/login'>Login</a> first
                    </body>
                    </html>'''
                    
@app.route('/delete', methods = ['POST'])
def delete():
    if session['user']:
        if session['user']['role'] == 'ADMIN':
            if request.method == 'POST':
                book_id = request.form['book_id']
                is_exists = inventory_handler.isbook_existsbyid(book_id)
                if is_exists:
                    is_deleted = inventory_handler.delbook(book_id)
                    if is_deleted:
                        return redirect(url_for('home'))
                    else:
                        return '''<!doctype html>
                            <html>
                            <head>
                            <title>delete book</title>
                            </head>
                            <body>
                            <h3>Delete book is not successful</h3>
                            <a href = '/home'>Home</a>
                            </body>
                            </html>'''
                else:
                        return '''<!doctype html>
                            <html>
                            <head>
                            <title>delete book</title>
                            </head>
                            <body>
                            <h3>Book doesn't exist</h3>
                            <a href = '/home'>Home</a>
                            </body>
                            </html>'''
        else:
            return '''<!doctype html>
                        <html>
                        <head>
                        <title>delete book</title>
                        </head>
                        <body>
                        <h3>Permission denied</h3>
                        <a href = '/home'>Home</a>
                        </body>
                        </html>'''
    else:
            return '''<!doctype html>
                        <html>
                        <head>
                        <title>delete book</title>
                        </head>
                        <body>
                        <h3>Need permission</h3>
                        <a href = '/login'>login</a> first
                        </body>
                        </html>'''

@app.route('/borrowbook')
def borrowbook():
    session['load_url'] = request.url
    if session['user']:
        if session['user']['role'] == 'ADMIN':
            return render_template('borrowbook.html')
        else:
            return '''<!doctype html>
                        <html>
                        <head>
                        <title>borrow book</title>
                        </head>
                        <body>
                        <h3>Permission denied</h3>
                        <a href = '/home'>Home</a>
                        </body>
                        </html>'''
    else:
        return '''<!doctype html>
                        <html>
                        <head>
                        <title>borrow book</title>
                        </head>
                        <body>
                        <h3>Need permission</h3>
                        <a href = '/login'>login</a> first
                        </body>
                        </html>'''
@app.route('/borrow', methods = ['POST'])
def borrow():
    if session['user']:
        if session['user']['role'] == 'ADMIN':
            if request.method == 'POST':
                user_id = int(request.form['user_id'])
                book_id = request.form['book_id']
                is_userexists = user.is_user_existsbyid(user_id) 
                is_bookexists = inventory_handler.isbook_existsbyid(book_id)
                if is_userexists:
                    if is_bookexists:
                        borrowed = inventory_handler.borrowbook(user_id, book_id)
                        if borrowed:
                            return redirect(url_for('home'))
                        else:
                            return '''<!doctype html>
                            <html>
                            <head>
                            <title>borrow book</title>
                            </head>
                            <body>
                            <h3>Book not available</h3>
                            <a href = '/home'>Home</a>
                            </body>
                            </html>'''
                    else:
                        return '''<!doctype html>
                            <html>
                            <head>
                            <title>borrow book</title>
                            </head>
                            <body>
                            <h3>Book doesn't exists</h3>
                            <a href = '/home'>Home</a>
                            </body>
                            </html>'''
                else:
                    session['load_url'] = url_for('borrowbook')
                    return '''<!doctype html>
                        <html>
                        <head>
                        <title>borrow book</title>
                        </head>
                        <body>
                        <h3>User doesn't exists</h3>
                        <a href = '/createaccount'>create pass</a>
                        </body>
                        </html>'''
        else:
            return '''<!doctype html>
                        <html>
                        <head>
                        <title>borrow book</title>
                        </head>
                        <body>
                        <h3>Permission denied</h3>
                        <a href = '/home'>Home</a>
                        </body>
                        </html>'''
    else:
        return '''<!doctype html>
                        <html>
                        <head>
                        <title>borrow book</title>
                        </head>
                        <body>
                        <h3>Need permission</h3>
                        <a href = '/login'>login</a> first
                        </body>
                        </html>'''
                        
@app.route('/borrowedbooksdata')
def borrowedbooksdata():
    data = inventory_handler.get_all_borrowedbooks()
    return data

@app.route('/allborrowedbooksdata')
def allborrowedbooksdata():
    if session['user'] and session['user']['role'] == 'ADMIN':
        data = get_all_borrowed_book()
        return render_template('allborrowedbooks.html', data = data)
    else:
        return '''<!doctype html>
                        <html>
                        <head>
                        <title>borrow book</title>
                        </head>
                        <body>
                        <h3>Permission denied</h3>
                        <a href = '/home'>Home</a>
                        </body>
                        </html>'''

@app.route('/returnbook')
def returnbook():
    if session['user'] and session['user']['role'] == 'ADMIN':
        return render_template('returnbook.html')
    else:
        return '''<!doctype html>
                        <html>
                        <head>
                        <title>borrow book</title>
                        </head>
                        <body>
                        <h3>Permission denied</h3>
                        <a href = '/home'>Home</a>
                        </body>
                        </html>'''
          
@app.route('/getreturnbooks', methods = ['GET'])              
def getreturnbooks():
    if session['user'] and session['user']['role'] == 'ADMIN':
        if request.method == 'GET':
            user_id = request.args.get('user_id')
            is_exists = user.is_user_existsbyid(user_id)
            if is_exists:
                data = inventory_handler.get_all_borrowedbooks_byuserid(user_id)
                return render_template('showreturnbooks.html', data = data)
            else:
                return '''<!doctype html>
                        <html>
                        <head>
                        <title>return book</title>
                        </head>
                        <body>
                        <h3>User doens't exists</h3>
                        <a href = '/home'>Home</a>
                        </body>
                        </html>''' 
            
    else:
        return '''<!doctype html>
                        <html>
                        <head>
                        <title>return book</title>
                        </head>
                        <body>
                        <h3>Permission denied</h3>
                        <a href = '/home'>Home</a>
                        </body>
                        </html>'''
                        
@app.route('/return', methods = ['POST'])
def bookreturn():
    if session['user'] and session['user']['role']:
        if request.method == 'POST':
            borrow_id = request.form['borrow_id']
            user_id = request.form['user_id']
            book_id = request.form['book_id']
            returned = inventory_handler.return_book(book_id, borrow_id)
            if returned:
                reminder.send_mail_to_reserved(book_id)
                return redirect(f'/getreturnbooks?user_id={user_id}')
            else:
                return '''<!doctype html>
                        <html>
                        <head>
                        <title>return book</title>
                        </head>
                        <body>
                        <h3>Return request failed</h3>
                        <a href = '/home'>Home</a>
                        </body>
                        </html>'''
    else:
         return '''<!doctype html>
                        <html>
                        <head>
                        <title>return book</title>
                        </head>
                        <body>
                        <h3>Permission denied</h3>
                        <a href = '/home'>Home</a>
                        </body>
                        </html>'''

@app.route('/report')
def report():
    if session['user'] and session['user']['role'] == 'ADMIN':
        weekly_report, monthly_report = inventory_handler.report() 
        return render_template('report.html', weekly_report = weekly_report, monthly_report = monthly_report)
    else:
        return '''<!doctype html>
                        <html>
                        <head>
                        <title>report</title>
                        </head>
                        <body>
                        <h3>Permission denied</h3>
                        <a href = '/home'>Home</a>
                        </body>
                        </html>'''

@app.route('/reservebook')
def reservebook():
    return render_template('reserve.html')

@app.route('/reserve', methods = ['GET'])
def reserve():
    if request.method == 'GET':
        user_id = request.args.get('user_id')
        book_id = request.args.get('book_id')
        is_reserved, record = inventory_handler.is_book_reserved(user_id, book_id)
        print('record =', record)
        go_to_reserve = False
        if is_reserved :
            for item in record:
                if item['status'] == 'INACTIVE':
                    go_to_reserve = True
        if go_to_reserve or not is_reserved:
            book_record = inventory_handler.get_book_byid(int(book_id))
            book_record = book_record[0]
            print('book_record =', book_record)
            if book_record['status'] == 'AVAILABLE':
                return '''<!doctype html>
                            <html>
                            <head>
                            <title>reserve book</title>
                            </head>
                            <body>
                            <h3>Book available</h3>
                            <p>Visit library to borrow the book</p>
                            <a href = '/home'>Home</a>
                            </body>
                            </html>'''
            else:
                is_exists, user_record = user.is_user_existsbyid(int(user_id))
                print('user_record =', user_record)
                if is_exists:
                    inventory_handler.reserve_book(user_record, book_record)
                    return redirect(url_for('home'))
                else:
                    return '''<!doctype html>
                            <html>
                            <head>
                            <title>reserve book</title>
                            </head>
                            <body>
                            <h3>User doesn't exists</h3>
                            <a href = '/home'>Home</a>
                            </body>
                            </html>'''
        else:
            return '''<!doctype html>
                                <html>
                                <head>
                                <title>reserve book</title>
                                </head>
                                <body>
                                <h3>Status Active</h3>
                                <p>Wait until book is available</p>
                                <a href = '/home'>Home</a>
                                </body>
                                </html>'''
                                
@app.route('/report_graph')
def report_graph():
    if session['user'] and session['user']['role'] == 'ADMIN':
        weekly_report, monthly_report = inventory_handler.report() 
        date_obj = datetime.now()
        plt_html = graph.borrowAndReturn_VS_days(weekly_report, 7)
        return render_template('report_graph.html', graph = plt_html)
        return '''<!doctype html>
                        <html>
                        <head>
                        <title>report</title>
                        </head>
                        <body>
                        <h3>Permission denied</h3>
                        <a href = '/home'>Home</a>
                        </body>
                        </html>'''
    

@app.route('/get_graph', methods = ['GET'])
def get_graph():
    return redirect(url_for('report_graph'))


if __name__ == "__main__":
    app.run(debug = True)