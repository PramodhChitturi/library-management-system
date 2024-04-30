import mysql.connector
from db.globals import *
from time import time
class MySQLDBHandler:
    def __init__(self, db_config):
        self.db_config = db_config
        self.cursor = ''
        self.cnx = ''
    
    def get_connection(self, result_dict = ''):
        try:
            self.cnx = mysql.connector.connect(**self.db_config)
            if result_dict:
                self.cursor = self.cnx.cursor(dictionary= True)
            else:
                self.cursor = self.cnx.cursor()
        except Exception as e:
            print(f'get_connection Error - {e}')
        # finally:
        #   self.cursor.execute('CREATE VIEW report AS SELECT ')  
    def close_connection(self):
        try:
            self.cnx.commit()
            self.cursor.close()
            self.cnx.close()
        except Exception as e:
            print(f'close_connection Error - {e}')
        
    def execute_query(self,query, params = ''):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
        except Exception as e:
            print('query =', query)
            print(f'execute_connection Error - {e}')
        
    
    def fetch(self, query, result_dict = ''):
        try:
            self.get_connection(result_dict)
            self.execute_query(query)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print(f'fetch Error - {e}')
        finally:
            self.close_connection()
    
    def insert_into_talbe(self, table_name, values):
        try:
            self.get_connection()
            query = INSERT(table_name, values)
            self.execute_query(query)
        except Exception as e:
            print(f'insert Error - {e}')
        finally:
            self.close_connection()
        
    def update_table(self, table_name, changes, condition):
        try:
            self.get_connection()
            query = UPDATE(table_name, changes, condition)
            self.execute_query(query)
        except Exception as e:
            print(f'update Error - {e}')
        finally:
            self.close_connection()
    
    def delete_from_table(self, table_name, condition):
        try:
            self.get_connection()
            query = DELETE(table_name, condition)
            self.execute_query(query)
        except Exception as e:
            print(f'delete Error - {e}')
        finally:
            self.close_connection()
            
    

# db_config = {'host' : 'localhost',
#              'user' : 'root',
#              'password' : 'Vizag@123',
#              'database' : 'library'
#     }
# mysql_db = MySQLDBHandler(db_config)
# if __name__ == '__main__':
    
#     mysql_db.get_connection()
