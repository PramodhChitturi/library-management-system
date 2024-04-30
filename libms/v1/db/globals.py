MYSQL_DB = 'library'
INVENTORY_TABLE = 'books_inventory_table'
BORROW_TABLE = 'borrowed_books'
USER_TABLE = 'users'
#queries
SELECT_ALL_BOOKS = f'SELECT id as ID, book_name as `Book name`, author as Author, edition as Edition, description as Description, category as Category, created_at as `Created at`, count as Count, book_available as `No.of books available`, availability as Availability FROM {INVENTORY_TABLE}'

SELECT_BORROWED_BOOKS = f'SELECT borrow_id as `Borrow ID`,user_id as `User ID`, person_name as Person, email as `Email`, book_id as `Book ID`, book_name as `Book name`,author as Author, book_edition as `Edition`,borrowed_at as `Borrowed at`, status as Status, returned_at as `Returned at` FROM {BORROW_TABLE}'

SELECT_ALL_USERS = f'SELECT * FROM {USER_TABLE}'

CHANGE_PASSWORD = f"UPDATE {USER_TABLE} SET password = %s WHERE email = '%s'"
 
def borrow_book_info(email):
    BORROW_BOOK_INFO = f"SELECT borrow_id as `Borrow ID`,user_id as `User ID`, person_name as Person, email as `Email`, book_id as `Book ID`, book_name as `Book name`,author as Author, book_edition as `Edition`,borrowed_at as `Borrowed at`, status as Status, returned_at as `Returned at` FROM {BORROW_TABLE} WHERE email = '{email}'"
    return BORROW_BOOK_INFO
# def borrow_book_by_person(person, email):
#     SELECT_BORROWED_BOOKS_BY_PERSON = f'SELECT borrow_id as `Borrow ID`,user_id as `User ID`, person_name as Person, email as `Email`, book_id as `Book ID`, book_name as `Book name`,author as Author, book_edition as `Edition`,borrowed_at as `Borrowed at`, status as Status, returned_at as `Returned at` FROM {BORROW_TABLE} WHERE person_name = "{person}" and email = "{email}"'
#     return SELECT_BORROWED_BOOKS_BY_PERSON

def report(dateandtime, report_dateandtime):
    REPORT = f'SELECT borrow_id as `Borrow ID`,user_id as `User ID`, person_name as Person, email as `Email`, book_id as `Book ID`, book_name as `Book name`,author as Author, book_edition as `Edition`,borrowed_at as `Borrowed at`, status as Status, returned_at as `Returned at` FROM {BORROW_TABLE} WHERE borrowed_at BETWEEN "{report_dateandtime}" and "{dateandtime}" or returned_at BETWEEN "{report_dateandtime}" and "{dateandtime}"'
    return REPORT
# SELECT_ALL_BOOKS = f'select Id as ID, `Book name` as Title, Author as Author from {INVENTORY_TABLE}'

ADD_BOOK_TO_INVENTORY = f'INSERT INTO {INVENTORY_TABLE} VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

ADD_BOOK_TO_BORROW = f'INSERT INTO {BORROW_TABLE} VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)'

ADD_USER = f'INSERT INTO {USER_TABLE}(username, email, password, role) VALUES(%s, %s, %s, %s)'

def update(table_name, changes, condition):
    # UPDATE_BOOK_DATA = f'UPDATE {INVENTORY_TABLE} SET %s WHERE %s'
    query = f'UPDATE {table_name} SET {changes} WHERE {condition}'
    return query

def getstr(num):
    str = ''
    for i in range(num):
        str += '%s'
        if i < num-1:
            str += ', '
    return str

def delete_record(table_name, condition):
    query = f"DELETE FROM {table_name} WHERE {condition}"
    return query

def search_by_book_name(book_name, table_name, user_id):
    if table_name == INVENTORY_TABLE:
        SEARCH = f"SELECT id as ID, book_name as `Book name`, author as Author, edition as Edition, description as Description, category as Category, created_at as `Created at`, count as Count, book_available as `No.of books available`, availability as Availability FROM {INVENTORY_TABLE} WHERE book_name = '{book_name}'"
    elif table_name == BORROW_TABLE:
        SEARCH = f"SELECT borrow_id as `Borrow ID`,user_id as `User ID`, person_name as Person, email as `Email`, book_id as `Book ID`, book_name as `Book name`,author as Author, book_edition as `Edition`,borrowed_at as `Borrowed at`, status as Status, returned_at as `Returned at` FROM {BORROW_TABLE} WHERE book_name = '{book_name}' and user_id = '{user_id}'"   
    return SEARCH

def search_by_book_id(book_id, table_name, user_id):
    if table_name == INVENTORY_TABLE:
        SEARCH = f"SELECT id as ID, book_name as `Book name`, author as Author, edition as Edition, description as Description, category as Category, created_at as `Created at`, count as Count, book_available as `No.of books available`, availability as Availability FROM {INVENTORY_TABLE} WHERE id = '{book_id}'"
    elif table_name == BORROW_TABLE:
        SEARCH = f"SELECT borrow_id as `Borrow ID`,user_id as `User ID`, person_name as Person, email as `Email`, book_id as `Book ID`, book_name as `Book name`,author as Author, book_edition as `Edition`,borrowed_at as `Borrowed at`, status as Status, returned_at as `Returned at` FROM {BORROW_TABLE} WHERE book_id = '{book_id}' and user_id = '{user_id}'"   

    return SEARCH

def search_by_borrow_id(borrow_id, user_id):
    SEARCH = f"SELECT borrow_id as `Borrow ID`,user_id as `User ID`, person_name as Person, email as `Email`, book_id as `Book ID`, book_name as `Book name`,author as Author, book_edition as `Edition`,borrowed_at as `Borrowed at`, status as Status, returned_at as `Returned at` FROM {BORROW_TABLE} WHERE borrow_id = '{borrow_id}' and user_id = '{user_id}'"   

    return SEARCH
    
    
# INSERT_BOOK = 'INSERT INTO %s VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'