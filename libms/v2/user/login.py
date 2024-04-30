import os
from dotenv import load_dotenv, find_dotenv
from db.globals import *
import smtplib
from random import randint
from user.user_ops import User


load_dotenv(find_dotenv())

db_conf = {
            'host': os.environ['DB_SERVER'],
            'user': os.environ['DB_USER_NAME'],
            'password': os.environ['DB_PASSWORD'],
            'database': os.environ['DB_DATABASE']    
          }


class UserLoginManager(User):
    
    def user_verfication(self, email, password):
        try:
            record = 'No record found'
            query = GET_USER(email)
            record = self.fetch(query, result_dict = True)
            give_access = False
            print('record =', record)
            if record :
                if record[0]['password'] == password:
                    give_access = True
            return give_access, record[0]
        except Exception as e:
            print(f'user_verification Error - {e}')
    

    def create_user(self, name, email, password):
        try:
            values = (name, email, password, 'USER')
            query = INSERT(USER_TABLE, values)
            self.get_connection()
            self.execute_query(query)
        except Exception as e:
            print(f'create_user Error - {e}')
        finally:
            self.close_connection()
    
    def generate_otp(self, mail):
        is_exists = self.is_user_exists(mail)
        otp = ''
        if is_exists:
            otp = randint(100000, 999999)
        return otp
            
            
    def forgot_password(self, email):
        otp = self.generate_otp(email)
        if otp:
            smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_obj.ehlo()
            smtp_obj.starttls()
            smtp_obj.login(os.environ['EMAIL'], os.environ['APP_PASS'])
            subject = 'OTP'
            message = f'Your one time password(OTP) is {otp}'
            msg = 'Subject: '+ subject + '\n' + message
            from_address = os.environ['EMAIL']
            to_address = email
            smtp_obj.sendmail(from_address, to_address, msg)
            smtp_obj.quit()
            return otp
        
    def change_password(self, email, password):
        changes = f'password = "{password}"'
        condition = f"email = '{email}'"
        query = UPDATE(USER_TABLE, changes, condition)
        self.get_connection()
        self.execute_query(query)
        self.close_connection()
        
        
user_login = UserLoginManager(db_conf)