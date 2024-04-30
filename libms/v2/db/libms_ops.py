from db.mysql_ops import MySQLDBHandler
import os
from dotenv import load_dotenv, find_dotenv
from db.globals import *
from datetime import datetime, timedelta
from smtplib import *
load_dotenv(find_dotenv())

db_conf = {
            'host': os.environ['DB_SERVER'],
            'user': os.environ['DB_USER_NAME'],
            'password': os.environ['DB_PASSWORD'],
            'database': os.environ['DB_DATABASE']    
          }

class LibraryOperations(MySQLDBHandler):
    def get_all_books(self):
        try:
            query = ALL_INVENTORY_BOOKS
            self.get_connection()
            data = self.fetch(query, result_dict= True)
            return data
        except Exception as e:
            print(f'get_all_books Error = {e}')\
    
    def get_book_byid(self, book_id):
        try:
            query = GET_BOOK_BYID(book_id)
            record = ''
            self.get_connection()
            record = self.fetch(query, result_dict=True)
            return record
        except Exception as e:
            print(f'get_book Error - {e}')
    
    def get_book(self, book_name, edition):
        try:
            query = GET_BOOK(book_name, edition)
            record = ''
            self.get_connection()
            record = self.fetch(query, result_dict=True)
            return record
        except Exception as e:
            print(f'get_book Error - {e}')

    def isbook_existsbyid(self, book_id):
        try:
            record = self.get_book_byid(book_id)
            if record :
                is_exists = True
            else:
                is_exists = False
            return is_exists
        except Exception as e:
            print(f'isbook_existsbyid Error - {e}')
            
    def isbook_exists(self, book_name, edition):
        try:
            record = ''
            record = self.get_book(book_name, edition)
            if record:
                is_exists = True
            else:
                is_exists = False
            return is_exists, record
        except Exception as e:
            print(f'isbook_exists Error - {e}')
            
    def addbook(self, book_name, author, edition, category, description):
        try:
            is_exists, record = self.isbook_exists(book_name, edition)
            is_added = False
            print('record =', record)
            if is_exists:
                quantity = record[0]['quantity'] + 1
                books_available = record[0]['book_available'] + 1
                status = 'AVAILABLE'
                changes = f'quantity = {quantity}, book_available = {books_available}, status = "{status}"'
                condition = f'book_name = "{book_name}" and edition = "{edition}"'
                query = UPDATE(INVENTORY_TABLE, changes, condition)
            else:
                datetime_obj = datetime.now()
                created_at = str(datetime_obj.date())
                quantity = 1
                books_available = 1
                record = (book_name, author, edition, category, description, created_at, quantity, books_available, 'AVAILABLE')
                print('record =', record)
                query = INSERT(INVENTORY_TABLE, record)
            self.get_connection()
            self.execute_query(query)
            is_added = True
            return is_added
        except Exception as e:
            print(f'addbook Error - {e}')
        finally:
            self.close_connection()
    
    def delbook(self, book_id):
        try:
            is_deleted = True
            record = self.get_book_byid(book_id)
            print('record =', record)
            quantity = record[0]['quantity']
            print('quantity =', quantity)
            if quantity == 1:
                condition = f'id = "{book_id}"'
                query = DELETE(INVENTORY_TABLE, condition)
            elif quantity > 1:
                books_available = record[0]['book_available'] - 1
                quantity -= 1
                changes = f'quantity = {quantity}, book_available = {books_available}'
                condition = f'id = "{book_id}"'
                query = UPDATE(INVENTORY_TABLE, changes, condition)
            self.get_connection()
            self.execute_query(query)
            return is_deleted
        except Exception as e:
            print(f'delbook Error - {e}')
        else:
            is_deleted = False
            return is_deleted
        finally:
            self.close_connection()
    
    def borrowbook(self,user_id, book_id):
        #drop borrow table (Completed)
        #create drop id (completed)
        #generate borrow id using auto increment (completed)
        #implement borrowbook
        #generate receipt with borrow_id, user (id, name, email), book_name
        #download and print reciept
        try:
            borrowed = True
            book_record = self.get_book_byid(book_id)
            book_record = book_record[0]
            book_status = book_record['status']
            if book_status == 'AVAILABLE':
                user_id = user_id
                # person_name = user_record['username']
                # email = user_record['email']
                # # book_id
                # book_name = book_record['book_name']
                # author = book_record['author']
                # book_edition = book_record['edition']
                datetimeobj = datetime.now()
                borrowed_at = str(datetimeobj.date())
                status = 'ISSUED'
                returned_at = '-'
                record = (user_id, book_id, borrowed_at, status, returned_at)
                books_available = book_record['book_available']
                quantity = book_record['quantity']
                if books_available >1:
                    changes = f'book_available = {books_available - 1}'
                elif books_available == 1:
                    changes = f'book_available = {books_available - 1}, status = "NOT AVAILABLE"'
                else:
                    borrowed = False
                if borrowed == True:
                    condition = f'id = "{book_id}"'
                    query1 = INSERT(BORROW_TABLE, record)
                    query2 = UPDATE(INVENTORY_TABLE, changes, condition)
                    self.get_connection()
                    self.execute_query(query1)
                    self.execute_query(query2)
            else:
                borrowed = False
            return borrowed
        except Exception as e:
            print(f'borrowbook Error - {e}')
        finally:
            self.close_connection()
            
    def get_all_borrowedbooks(self):
        try:
            query = ALL_BORROWED_BOOKS
            self.get_connection()
            data = self.fetch(query, result_dict=True)
            return data
        except Exception as e:
            print(f'get_all_borrowedbooks Error - {e}')
    
    def get_all_borrowedbooks_byuserid(self, user_id):
        try:
            data = 'NO RECORDS FOUND'
            query = GET_BORROW_BOOKS_BY_ID(user_id)
            self.get_connection()
            data = self.fetch(query, result_dict= True)
            return data
        except Exception as e:
            print(f'get_all_borrowedbooks_byuserid Error - {e}')
        
    def return_book(self, book_id, borrow_id):
        try:
            returned = False
            datetime_obj = datetime.now()
            returned_at = str(datetime_obj.date())
            changes = f'status = "RETURNED", returned_at = "{returned_at}"'
            condition = f'borrow_id = "{borrow_id}"'
            query = UPDATE(BORROW_TABLE, changes, condition)
            record = self.get_book_byid(book_id)
            record = record[0]
            book_available = record['book_available'] + 1
            if book_available <= record['quantity']:
                self.get_connection()
                self.execute_query(query)
                changes = f'book_available = {book_available}, status = "AVAILABLE"'
                condition = f'id = "{book_id}"'
                query = UPDATE(INVENTORY_TABLE, changes, condition)
                self.execute_query(query)
                returned = True
            return returned
        except Exception as e:
            print(f'return_book Error - {e}')
        finally:
            self.close_connection()
     
    def report(self):
        datetime_obj = datetime.now()
        date = datetime_obj.date()
        weekly = str(date - timedelta(7))
        monthly = str(date - timedelta(30))
        weekly_report_query = REPORT(weekly)
        monthly_report_query = REPORT(monthly)
        self.get_connection()
        weekly_report = self.fetch(weekly_report_query, result_dict = True)
        self.get_connection()
        monthly_report = self.fetch(monthly_report_query, result_dict=True) 
        return weekly_report, monthly_report
    
    def  is_book_reserved(self,user_id, book_id):
        try:
            is_reserved = False
            record = ''
            query = GET_RESERVED_BOOK(user_id, book_id)
            self.get_connection()
            record = self.fetch(query, result_dict=True)
            if record:
                is_reserved = True
            return is_reserved, record
        except Exception as e:
            print(f'is_book_reserved Error - {e}')
        
    def reserve_book(self, user_record, book_record):
        try:
            user_id = user_record['id']
            username = user_record['username']
            email = user_record['email']
            book_id = book_record['id']
            book_name = book_record['book_name']
            author = book_record['author']
            book_edition = book_record['edition']
            datetime_obj = datetime.now()
            reserved_at = str(datetime_obj.date())
            status = 'ACTIVE'
            values = (user_id, username, email, book_id, book_name, author, book_edition, reserved_at, status)
            self.get_connection()
            query = INSERT(RESERVE_TABLE, values)
            self.execute_query(query)
        except Exception as e:
            print(f'reserve_book Error - {e}')
        finally:
            self.close_connection()
    
    # def send_mail_to_reserved(self, book_id):
    #     try:
    #         query = GET_RESERVE_BOOK_BY_BOOK_ID(book_id)
    #         self.get_connection()
    #         record = self.fetch(query, result_dict = True)
    #         if record:
    #             smtp_obj = SMTP('smtp.gmail.com', 587)
    #             smtp_obj.ehlo()
    #             smtp_obj.starttls()
    #             smtp_obj.login(os.environ['EMAIL'], os.environ['APP_PASS'])
    #             subject = 'Reserved book available'
    #             for item in record:
    #                 if item['status'] == 'ACTIVE':
    #                     message = f'You reserved for book\nBook ID: {record[0]['book_id']}\nBook name: {record[0]['book_name']}\nBook author: {record[0]['author']}\nBook edition: {record[0]['book_edition']}\nIS AVAILABLE NOW IN LIBRARY\nVisit the library to get the book'                     
    #                     print('message =', message)
    #                     msg = 'Subject: '+ subject + '\n' + message
    #                     from_address = os.environ['EMAIL']
    #                     to_address = item['email']
    #                     smtp_obj.sendmail(from_address, to_address, msg)
    #                     reserve_id = item['reserve_id']
    #                     changes = 'status = "INACTIVE"'
    #                     condition = f'reserve_id = {reserve_id}'
    #                     query = UPDATE(RESERVE_TABLE, changes, condition)
    #                     self.get_connection()
    #                     self.execute_query(query)
    #                     smtp_obj.quit()
    #     except Exception as e:
    #         print(f'send_mail_to_reserved Error - {e}')

inventory_handler = LibraryOperations(db_conf)