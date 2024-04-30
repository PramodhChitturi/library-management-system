from db.mysql_ops import MySQLDBHandler
import os
from dotenv import load_dotenv, find_dotenv
from db.globals import *


load_dotenv(find_dotenv())

db_conf = {
            'host': os.environ['DB_SERVER'],
            'user': os.environ['DB_USER_NAME'],
            'password': os.environ['DB_PASSWORD'],
            'database': os.environ['DB_DATABASE']    
          }

class User(MySQLDBHandler):

    def get_users(self):
        try:
            query = ALL_USERS
            data = self.fetch(query, result_dict=True)
            return data
        except Exception as e:
            print(f'get_user Error - {e}')
    
    def is_user_exists(self, email):
        try:
            data = self.get_users()
            is_exists = False
            record = ''
            for item in data:
                if item['email'] == email:
                    is_exists = True
                    record = item
            return is_exists, record
        except Exception as e:
            print(f'is_user_exists Error - {e}')
            
    def is_user_existsbyid(self, user_id):
        try:
            data = self.get_users()
            is_exists = False
            record = ''
            for item in data:
                if item['id'] == user_id:
                    is_exists = True
                    record = item
            return is_exists, record
        except Exception as e:
            print(f'is_user_exists Error - {e}')
    
    
user = User(db_conf)