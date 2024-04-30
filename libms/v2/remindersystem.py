from db.libms_ops import inventory_handler
from db.mysql_ops import MySQLDBHandler
from db.globals import *
from dotenv import load_dotenv, find_dotenv
import os
import smtplib

load_dotenv(find_dotenv())

db_conf = {
            'host': os.environ['DB_SERVER'],
            'user': os.environ['DB_USER_NAME'],
            'password': os.environ['DB_PASSWORD'],
            'database': os.environ['DB_DATABASE']    
          }

mail_crdentials = {'from_adress': os.environ['EMAIL'],
                   'password': os.environ['APP_PASS']}

                   
class Reminder(MySQLDBHandler):
    
    def __init__(self, mail_crdentials):
        self.from_adress = mail_crdentials['from_adress']
        self.password = mail_crdentials['password']
        self.mail_obj = None
        super().__init__(db_conf)
        
    def create_mail_obj(self):
        try:
            self.mail_obj = smtplib.SMTP('smtp.gmail.com', 587)
            self.mail_obj.ehlo()
            self.mail_obj.starttls()
            self.mail_obj.login(self.from_adress, self.password)
        except Exception as e:
            print(f'create_mail_obj Error - {e}')

    def quit_mail_obj(self):
        try:
            self.mail_obj.quit()
        except Exception as e:
            print(f'quit_mail_obj Error - {e}')
    
    def send_libms_pass(self, email):
        try:
            self.create_mail_obj()
            subject = 'ACCOUNT CREATED SUCCESSFULLy'
            message = 'Your account has been created by library management Admin\nYou can login in our official website using below password\nPassword: libms@123\nYou can always change your account password using forgot password'
            msg = 'Subject: ' + subject + '\n' + message
            from_address = os.environ['EMAIL']
            to_address = email
            self.mail_obj.sendmail(from_address, to_address, msg)
            self.close_connection()
        except Exception as e:
            print(f'send_libms_pass Error - {e}')
            
    def send_mail_to_reserved(self, book_id):
        try: 
            query = GET_RESERVE_BOOK_BY_BOOK_ID(book_id)
            self.get_connection()
            record = self.fetch(query, result_dict = True)
            if record:
                self.create_mail_obj()
                subject = 'Reserved book available'
                for item in record:
                    if item['status'] == 'ACTIVE':
                        message = f'You reserved for book\nBook ID: {record[0]['book_id']}\nBook name: {record[0]['book_name']}\nBook author: {record[0]['author']}\nBook edition: {record[0]['book_edition']}\nIS AVAILABLE NOW IN LIBRARY\nVisit the library to get the book'                     
                        print('message =', message)
                        msg = 'Subject: '+ subject + '\n' + message
                        to_address = item['email']
                        self.mail_obj.sendmail(self.from_address, to_address, msg)
                        reserve_id = item['reserve_id']
                        changes = 'status = "INACTIVE"'
                        condition = f'reserve_id = {reserve_id}'
                        query = UPDATE(RESERVE_TABLE, changes, condition)
                        self.get_connection()
                        self.execute_query(query)
                        self.quit_mail_obj()
        except Exception as e:
            print(f'send_mail_to_reserved Error - {e}')
        
    def send_mail_to_defaulters(self):
        try:
            query = DEFAULTERS
            record = self.fetch(query, result_dict=True)
            if record:
                self.create_mail_obj()
                for data in record:
                    to_address = data['email']
                    subject = f"{data['book_name']} hasn't returned to library"
                    message = f"You borrowed book ({data['borrow_id']})\nBook ID: {data['book_id']}\nBook name: {data['book_name']}\nBook author: {data['author']}\nBook edition: {data['book_edition']}\nIS NOT RETURNED TO LIBRARY\nVisit the library with {data['book_name']} to return the book and also to avoid late fees "
                    msg = subject + '\n' + message
                    self.mail_obj.sendmail(self.from_adress, to_address, msg)
                self.quit_mail_obj()
        except Exception as e:
            print(f'send_mail_to_defaulters Error - {e}')
            
reminder = Reminder(mail_crdentials)
reminder.send_mail_to_defaulters()