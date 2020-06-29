import mysql.connector
import sys

class connect_db():
	conn = mysql.connector.connect(host = 'localhost', user = 'utsav', password = '2828')
	db = conn.cursor()
	db.execute('show databases')
	db_list = db.fetchall()
	db_name = 'learngaroo_flask_api'
	if (db_name,) in db_list:
		overwrite = input('Do you want to overwrite the database? (y/n): ')
		if overwrite == 'y':
			db.execute('DROP DATABASE '+db_name)
			db.execute('CREATE DATABASE '+db_name)
			print('Database has been successfully overwritten!')
			sys.exit()
		elif overwrite == 'n':
			db.execute('USE '+db_name)
			print('Continue working on existing database '+db_name)
			sys.exit()
		else:
			print('Please enter y or n')
			sys.exit()





		

