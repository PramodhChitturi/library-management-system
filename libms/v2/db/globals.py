#books__inentory_table
#self.cursor.execute('DROP table books_inventory_table')
#self.cursor.execute("create table books_inventory_table(id int NOT NULL AUTO_INCREMENT  PRIMARY KEY, book_name varchar(30) NOT NULL, author varchar(20) NOT NULL,edition varchar(20), category varchar(30), description varchar(500), created_at varchar(30), quantity int(20),book_available int(20), status ENUM('AVAILABLE', 'NOT AVAILABLE'))")
#self.cursor.execute(f'ALTER TABLE {INVENTORY_TABLE} AUTO_INCREMENT = 1234')

#borrowed_books
# self.cursor.execute('DROP TABLE borrowed_books')
# self.cursor.execute("CREATE TABLE borrowed_books(borrow_id int AUTO_INCREMENT PRIMARY KEY, user_id int(10), book_id varchar(10), borrowed_at varchar(30), status ENUM('ISSUED', 'RETURNED'), returned_at varchar(50))")
# self.cursor.execute('ALTER TABLE borrowed_books AUTO_INCREMENT = 15678')
# self.cursor.execute('CREATE VIEW borrowed_books_view AS SELECT borrowed_books.borrow_id, borrowed_books.user_id, users.username, users.email, borrowed_books.book_id, books_inventory_table.book_name, books_inventory_table.author, books_inventory_table.edition, borrowed_books.borrowed_at, borrowed_books.status, borrowed_books.returned_at FROM borrowed_books INNER JOIN users ON borrowed_books.user_id = users.id INNER JOIN books_inventory_table ON books_inventory_table.id = borrowed_books.book_id')

#users
# self.cursor.execute(f'DROP TABLE {USER_TABLE}')
# self.cursor.execute(f"CREATE TABLE users(id int NOT NULL AUTO_INCREMENT PRIMARY KEY, username varchar(25), email varchar(300), password varchar(50), role ENUM('ADMIN', 'USER'))")
# self.cursor.execute("ALTER TABLE library.users auto_increment = 1111 ")

#reserve
#self.cursor.execute(f'DROP TABLE {RESERVE_TABLE}')
# self.cursor.execute(f'CREATE TABLE {RESERVE_TABLE}(reserve_id INT AUTO_INCREMENT PRIMARY KEY, user_id int, username varchar(50), email varchar(255), book_id int, book_name varchar(30), author varchar(30), book_edition varchar(30), reserved_at varchar(50), status ENUM ("ACTIVE", "INACTIVE"))')
# self.cursor.execute(f'ALTER TABLE {RESERVE_TABLE} AUTO_INCREMENT = 100')
#database

from datetime import datetime, timedelta


MYSQL_DB = 'library'

#tables
INVENTORY_TABLE = 'books_inventory_table'
BORROW_TABLE = 'borrowed_books'
USER_TABLE = 'users'
RESERVE_TABLE = 'reserve'

#views
BORROWED_BOOKS = 'borrowed_books_view'

BORROW_LIMIT = 4

#queries
ALL_INVENTORY_BOOKS = f'SELECT * FROM {INVENTORY_TABLE}'
ALL_USERS = f'SELECT * FROM {USER_TABLE}'
ALL_BORROWED_BOOKS = f'SELECT * FROM {BORROWED_BOOKS}'

def GET_BOOK(book_name, edition):
    query = f'SELECT * FROM {INVENTORY_TABLE} WHERE book_name = "{book_name}" and edition = "{edition}"'
    return query

def GET_BOOK_BYID(book_id):
    query = f'SELECT * FROM {INVENTORY_TABLE} WHERE id = "{book_id}"'
    return query

def GET_BORROW_BOOKS_BY_ID(user_id):
    query = f'SELECT * FROM {BORROWED_BOOKS} WHERE user_id = "{user_id}"'
    return query

def GET_RESERVED_BOOK(user_id, book_id):
    query = f'SELECT * FROM {RESERVE_TABLE} where user_id = "{user_id}" and book_id = "{book_id}"'
    return query

def GET_RESERVE_BOOK_BY_BOOK_ID(book_id):
    query = f'SELECT * FROM {RESERVE_TABLE} WHERE book_id = "{book_id}"'
    return query

def INSERT(table_name, values):
    if table_name == USER_TABLE:
        query = f'INSERT INTO {USER_TABLE}(username, email, password, role) VALUES {values}'
    elif table_name == INVENTORY_TABLE:
        query = f"INSERT INTO {INVENTORY_TABLE}(book_name, author, edition, category, description, created_at, quantity, book_available, status) VALUES {values}"
    elif table_name == BORROW_TABLE:
        query = f"INSERT INTO {BORROW_TABLE}(user_id, book_id, borrowed_at, status, returned_at) VALUES {values}"
    elif table_name == RESERVE_TABLE: 
        query = f"INSERT INTO {RESERVE_TABLE}(user_id, username, email, book_id, book_name, author, book_edition, reserved_at, status) VALUES {values}"
    return query

def UPDATE(table_name, changes, condition):
    query = f"UPDATE {table_name} SET {changes} WHERE {condition}"
    return query

def DELETE(table_name, condition):
    query = f"DELETE FROM {table_name} WHERE {condition}"
    return query

def GET_USER(email):
    query = f"SELECT * FROM {USER_TABLE} WHERE email = '{email}'"
    return query
def REPORT(date_obj):
    datetime_obj = datetime.now()
    date = str(datetime_obj.date())
    query = f'SELECT * FROM {BORROWED_BOOKS} WHERE borrowed_at BETWEEN "{date_obj}" and "{date}" or returned_at BETWEEN "{date_obj}" and "{date}"' 
    return query

datetime_obj = datetime.now()
date =str( datetime_obj.date() - timedelta(5))

DEFAULTERS = f"SELECT * FROM {BORROW_TABLE} WHERE status = 'ISSUED' and borrowed_at <= '{date}'"