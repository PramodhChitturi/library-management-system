from db.globals import *
from db.mysql_ops import *
import os
from dotenv import find_dotenv, load_dotenv
from json_data import *
from datetime import datetime, timedelta
# db_config = { 'host':'localhost', 
#                  'user' : 'root', 
#                  'password'  : 'Vizag@123',
#                  'database': 'library'}  
load_dotenv(find_dotenv())
db_config = { 'host':os.environ['DB_SERVER'], 
                 'user' : os.environ['DB_USER_NAME'], 
                 'password'  : os.environ['DB_PASSWORD'],
                 'database': os.environ['DB_DATABASE']} 

class InventoryDBHandler(MySQLDBHandler)  :
    
    def get_allbooks(self,table_name, result_dict = ''):
        if table_name == INVENTORY_TABLE:
            data =  self.fetch(SELECT_ALL_BOOKS, result_dict)
        elif table_name == BORROW_TABLE:
            data = self.fetch(SELECT_BORROWED_BOOKS, result_dict)
        return data
    
    def get_borrowed_books(self, email, result_dict = ''):
        query = borrow_book_info(email)
        data = self.fetch(query, result_dict)
        return data
    
    def is_book_exists(self, book_name, author, edition):
        data = get_inventory_data()
        is_exists = False
        count = 0
        book_available = 0
        for item in data:
            if item['Book name'] == book_name and item['Author'] == author and item['Edition'] == edition:
                is_exists = True
                count = item['Count']
                book_available = item['No.of books available']
                
        return is_exists, count, book_available
    
    def is_book_exists_byid(self, _id):
        data = get_inventory_data()
        record = {'ID':'-','Book name':'-', 'Author':'-', 'Edition':'-', 'Description':'-', 'Category':'-', 'Created at':'-', 'Count':0, 'No.of books available':0, 'Availability':'NO'}
        is_exists = False
        for item in data:
            if item['ID'] == _id:
                is_exists = True
                # count = item['Count']
                # book_available = item['No.of books available']
                record = item
        return is_exists, record
    def search(self, search_line, _filter, table_name, user_id):
        try:
            data = []
            if _filter == 'book_name':
                query = search_by_book_name(search_line, table_name, user_id)
                data = self.fetch(query, result_dict = True)
            elif _filter == 'book_id':
                query = search_by_book_id(search_line, table_name, user_id)
                data = self.fetch(query, result_dict = True)
            elif _filter == 'borrow_id':
                query = search_by_borrow_id(search_line, user_id)
                data = self.fetch(query, result_dict = True)
            return data
        except Exception as e:
            print(e)
    def add_book_to_inventory(self, book_name, author, edition, category, description):
        book_exists, count, book_available = self.is_book_exists(book_name, author, edition)
        if not book_exists:
            dateandtime = datetime.now()
            date = str(dateandtime.date())
            time = dateandtime.strftime('%X')
            created_at = date + ' ' + time
            strlen = len(book_name) - 3
            book_id = book_name[:2]+book_name[:strlen:-1] + edition
            book_id = book_id.replace(' ', '')
            count = 1
            book_available = 1
            record = (book_id, book_name, author, edition, category, description, created_at, count, book_available, 'YES')
            self.insert_into_books_inventory(record)
        else: 
            data = get_inventory_data()
            count = count + 1
            book_available = book_available + 1
            changes = f"count = '{count}', book_available = '{book_available}', availability = 'YES'"
            condition = f"book_name = '{book_name}' and author = '{author}' and edition = '{edition}'"
            self.update_table(INVENTORY_TABLE, changes = changes, condition = condition)
            return 'book is already available'
        
    def delete_record_book_inventory_table(self, table_name, book_id):
        book_exists, record = self.is_book_exists_byid(book_id)
        book_deleted= True
        count = record['Count']
        book_available = record['No.of books available']
        if book_exists:
            if count > 1:
                count -= 1 
                book_available -= 1
                changes = f'count = {count}, book_available = {book_available}'
                condition = f"id = '{book_id}'"
                self.update_table(INVENTORY_TABLE, changes, condition)
            else:
                condition = f"id = '{book_id}'"
                self.delete(table_name, condition)
        else:
            book_deleted = False
        return book_deleted
    
    def add_book_to_borrow(self, user_id, person, email, book_id):
        book_exists, record= self.is_book_exists_byid(book_id)
        print(record)
        count = record['Count']
        books_available = record['No.of books available']
        availability = record['Availability']
        borrowed = False
        if book_exists:
            if availability == 'YES' and books_available > 0:
                borrowed = True
                book_name = record['Book name']
                author = record['Author']
                book_edition  = record['Edition']
                dateandtime = datetime.now()
                date = dateandtime.strftime('%Y-%m-%d')
                time = dateandtime.strftime('%X')
                borrowed_at = date + ' ' + time
                borrow_id = person[:3] + person[len(person)-3:] + book_id + str(books_available) + str(count)
                if books_available > 1:
                    books_available -= 1
                    changes = f"book_available = {books_available}"
                    condition = f"id = '{book_id}'"   
                elif books_available == 1:
                    books_available -= 1
                    changes = f"book_available = {books_available}, availability = 'NO'"
                    condition = f"id = '{book_id}'"
                self.update_table(INVENTORY_TABLE, changes, condition)
                borrow_record = (borrow_id, user_id, person, email, book_id, book_name, author, book_edition, borrowed_at, 'ACTIVE', '-')
                self.insert_into_borrow(borrow_record)
        return borrowed
    
    def is_borrowed(self, person, email, book_id):
        is_borrowed = False
        record = {'Borrow ID':'-', 'Person':'-', 'Email':'-', 'Book ID':'-', 'Book name':'-','Author':'-', 'Edition':'-', 'Borrowed at':'-', 'Status':'-', 'Returned at': '-'}
        data = get_borrowed_data()
        for item in data:
            if item['Person'] == person and item['Email'] == email and item['Book ID'] == book_id:
                is_borrowed = True
                record = item
        return is_borrowed, record
    
    def is_borrowed_byid(self, borrow_id):
        is_borrowed = False
        record = {'Borrow ID':'-', 'Person':'-', 'Contact number':'-', 'Book ID':'-', 'Book name':'-','Author':'-', 'Edition':'-', 'Borrowed at':'-', 'Status':'-', 'Returned at': '-'}
        data = get_borrowed_data()
        for item in data:
            if item['Borrow ID'] == borrow_id:
                is_borrowed = True
                record = item
        return is_borrowed, record
    
    def returnbook(self, borrow_id, book_id):
        try:
            dateandtime = datetime.now()
            date = str(dateandtime.date())
            time = dateandtime.strftime('%X')
            returned_at = date + ' ' + time
            is_returned = False
            isborrowed, record = self.is_borrowed_byid(borrow_id)
            is_exists, book_record =self.is_book_exists_byid(book_id)
            if record['Status'] == 'ACTIVE' and book_record['No.of books available'] < book_record['Count']:
                borrow_condition = f"borrow_id = '{borrow_id}'"
                borrow_changes = f"status = 'INACTIVE', returned_at = '{returned_at}'"
                book_available = book_record['No.of books available'] + 1
                inventory_condition =f"id = '{book_id}'"
                inventory_changes = f"book_available = {book_available}, availability = 'YES'"
                if is_exists and isborrowed:
                    is_returned = True
                    self.update_table(BORROW_TABLE, borrow_changes, borrow_condition)
                    self.update_table(INVENTORY_TABLE, inventory_changes, inventory_condition)
            
        except Exception as e:
            print(e)
        return is_returned
    
    def report(self):
        weekly_data = ''
        monthly_data = ''
        
        dateandtimenow = datetime.now()
        dateandtime = str(dateandtimenow.date()) + ' ' + dateandtimenow.strftime('%X')
        
        monthly = datetime.now() - timedelta(days = 30)
        monthly_date = str(monthly.date()) + ' ' + monthly.strftime('%X')

        
        weekly = datetime.now()- timedelta(days = 7)
        weekly_date = str(weekly.date()) + ' ' + weekly.strftime('%X')
        
        weekly_report = report(dateandtime, weekly_date)
        print(weekly_report)
        weekly_data = self.fetch(weekly_report, result_dict=True)

        monthly_report = report (dateandtime, monthly_date)
        print(monthly_report)
        monthly_data = self.fetch(monthly_report, result_dict = True)
        
        print('Weekly report =', weekly_data)
        print('Monthly_report =', monthly_data)
        return weekly_data, monthly_data
        # return weekly_data, monthly_data
inventory_handler =  InventoryDBHandler(db_config)

# if __name__ == "__main__":
    
#     data = inventory_handler.get_allbooks()
#     print(data)