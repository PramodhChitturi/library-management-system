from db.mysql_ops import *
from db.globals import *
from random import randint
import os
from dotenv import find_dotenv, load_dotenv
import smtplib

load_dotenv(find_dotenv())
db_config = { 'host':os.environ['DB_SERVER'], 
                 'user' : os.environ['DB_USER_NAME'], 
                 'password'  : os.environ['DB_PASSWORD'],
                 'database': os.environ['DB_DATABASE']} 
 
class User(MySQLDBHandler):
    
    def get_users(self, result_dict = ''):
        query = SELECT_ALL_USERS
        data = self.fetch(query, result_dict)
        return data
    
    def is_user_exists(self, email):
        data = self.get_users(result_dict=True)
        is_exists = False
        record = None
        for item in data:
            if item['email'] == email:
                is_exists = True
                record = item
        return is_exists, record
    
    def check_credentials(self,email, password):
        data = self.get_users(result_dict = True)
        give_access = False
        for user in data:
            if user['email'] == email and user['password'] == password:
                give_access = True
        return give_access
    
    def create_user(self, name, email, password):
        is_exists = self.is_user_exists(email)
        if not is_exists:
            self.insert_into_user(name, email, password)
        else:
            return is_exists
        
    def generate_otp(self, email):
        
        is_exists = self.is_user_exists(email)
        if is_exists:
            otp = randint(11111, 99999)
            smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_obj.ehlo()
            smtp_obj.starttls()
            smtp_obj.login('pramodhkumarchitturilspk@gmail.com', 'vlbm dkqh muej wazo')
            subject = 'OTP'
            message = f'Your one time password (OTP) is {otp}'
            msg = 'Subject: '+subject+'\n'+message
            from_address = 'pramodhkumarchitturilspk@gmail.com'
            to_address = email
            smtp_obj.sendmail(from_address, to_address, msg)
            smtp_obj.quit()
            return otp
        else:
            return is_exists
    
    def change_password(self, email, password):
        try:
            changes = f"password = '{password}'"
            condition = f"email = '{email}'"
            query = update(USER_TABLE, changes, condition)
            print('email =', email)
            print('password =', password)
            print('query =', query)
            self.get_connection()
            self.execute_query(query)
            print('password changed')
        except Exception as e:
            print(e)
        finally:
            self.close_connection()
        
user_login_manager = User(db_config)