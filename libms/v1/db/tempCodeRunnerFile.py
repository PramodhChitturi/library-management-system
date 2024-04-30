nfig = { 'host':'localhost', 
                 'user' : 'root', 
                 'password'  : 'Vizag@123',
                 'database': 'library'}   
mysql_db = MySQLDBHandler(db_config)
if __name__ == '__main__':
    # print(mysql_db.fetch_inventory())
    # print(mysql_db.fetch('SELECT * FROM inventory'))
    mysql_db.get_connection()

