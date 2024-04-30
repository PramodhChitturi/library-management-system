import mysql.connector
from abc import ABC
from db.globals import *
from time import time
class MySQLDBHandler:
    def __init__(self, db_config):
        # self.localhost = localhost
        # self.user = user
        # self.password = password
        # self.dbname = db_name
        self.db_config = db_config
        self.cnx = ''
        self.cursor = ''
            
    def get_connection(self, result_dict = ''):   
        try:
            self.cnx = mysql.connector.connect(**self.db_config)
                #host = localhost, user = user, password = password, database = self.dbname)
            if isinstance(self.cnx, mysql.connector.connection.MySQLConnection): 
                print('Created db connection')
                if result_dict:
                    self.cursor = self.cnx.cursor(dictionary=True)
                else:
                    self.cursor = self.cnx.cursor()
                if self.cursor:
                    print('Cursor created')
                else:
                    print('Failed to create cursor')
            else:
                print('Unable to create db connection')
        except Exception as e:
            print(f'ERROR: Failed to create either connection or cursor - {e}')
        # finally:
        #     self.cursor.execute('DROP table books_inventory_table')
        #     self.cursor.execute("create table books_inventory_table(id varchar(20) primary key, book_name varchar(30) NOT NULL, author varchar(20) NOT NULL,edition varchar(20), category varchar(30), description varchar(500), created_at varchar(30), count int(20),book_available int(20), availability ENUM('YES', 'NO'))")
            # self.cursor.execute('DROP TABLE borrowed_books')
            # self.cursor.execute("CREATE TABLE borrowed_books(borrow_id varchar(100) primary key,user_id int(10), person_name varchar(30), email varchar(300),book_id varchar(500), book_name varchar(30),author varchar(30), book_edition varchar(20), borrowed_at varchar(30), status ENUM('ACTIVE', 'INACTIVE'), returned_at varchar(50))")
            # self.cursor.execute('ALTER TABLE borrowed_books MODIFY returned_at varchar(50)')
            # self.cursor.execute('DROP TABLE users')
            # seconds =int(time())
            # self.cursor.execute(f'DROP TABLE {USER_TABLE}')
            # self.cursor.execute(f"CREATE TABLE users(id int NOT NULL AUTO_INCREMENT PRIMARY KEY, username varchar(25), email varchar(300), password varchar(50), role ENUM('ADMIN', 'USER'))")
            # self.cursor.execute(f'ALTER TABLE users AUTO_INCREMENT = {seconds}')
    def close_connection(self):
        self.cnx.commit()
        self.cursor.close()
        self.cnx.close()
    def execute_query(self,query, params = ''):
        try:
            if params:
                print('if params')
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
        except Exception as e:
            print(e)
        
            
    def fetch(self,query, result_dict = ''):
        if result_dict: 
            self.get_connection(result_dict=True)
        else:    
            self.get_connection()
        try:
            self.execute_query(query, params = '')
            result = self.cursor.fetchall()
            return result
    
        finally:   
            self.close_connection()
            
    def make_admin(self, user_id):
        try:
            changes = f'role = ADMIN '
            condition = f'id = "{user_id}"'
            query = update(USER_TABLE, changes, condition)
            self.execute_query(query)
        except Exception as e:
            print(e)
        finally:
            self.close_connection()
        
    def insert_into_books_inventory(self, values):
        try:
            self.get_connection()
            query = ADD_BOOK_TO_INVENTORY
            self.execute_query(query, params=values)
        except Exception as e:
            print(e)
        finally:
            self.close_connection()
    
    def insert_into_borrow(self, values):
        try:
            self.get_connection()
            query = ADD_BOOK_TO_BORROW
            self.execute_query(query, params = values)
        except Exception as e:
            print(e)
        finally:
            self.close_connection()

    def update_table(self,table_name, changes, condition):
        try:
            self.get_connection()
            # query = f'UPDATE {INVENTORY_TABLE} SET {changes} WHERE {condition}'
            query = update(table_name, changes, condition)
            print('Query =', query)
            self.execute_query(query)
        except Exception as e:
            print('e')
        finally:
            self.close_connection()
    
    def delete(self, table_name, condition):
        try:
            query = delete_record(table_name, condition)
            print('Query =', query)
            self.get_connection()
            self.execute_query(query)
        except Exception as e:
            print(e)
        finally:
            self.close_connection()
    
    def borrows_returns_report(self, book_id):
        try:
            borrows_query = borrow_report(book_id)
            borrows = self.fetch(borrows_query)
            returns_query = return_report(book_id)
            returns = self.fetch(returns_query)
            return borrows[0][0], returns[0][0]
        except Exception as e:
            print(e)
    
    def insert_into_user(self, name, email, password):
        try:
            self.get_connection()
            query = ADD_USER
            self.execute_query(query, params = (name, email, password, 'USER'))
        except Exception as e:
            print(e)
        finally:
            self.close_connection()
    # def createtable(self, table_name, *args):
    #     self.table = table_name
    #     self.col = []
    #     for i in args:
    #         self.col.append(i)e
    #     sql = f'CREATE TABLE {self.table}(self.col[0])' 
    #     self.execute(sql)
# class InventoryDBHandler(MySQLDBHandler) :
#     def fetch_inventory():
#         query = "select * from inventory"
#         data =  MySQLDBHandler.fetch_query(query)
#         return data
        
# db_config = { 'host':'localhost', 
#                  'user' : 'root', 
#                  'password'  : 'Vizag@123',
#                  'database': 'library'}   
# mysql_db = MySQLDBHandler(db_config)
# if __name__ == '__main__':
#     # print(mysql_db.fetch_inventory())
#     # print(mysql_db.fetch('SELECT * FROM inventory'))
#     mysql_db.get_connection()

