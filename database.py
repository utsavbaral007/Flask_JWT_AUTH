import mysql.connector
import sys

class connect_db():
	conn = mysql.connector.connect(host = 'localhost', user = 'utsav', password = '2828')
	db = conn.cursor()
	db.execute('show databases')
	db_list = db.fetchall()
	db_name = input('Enter a database name: ')
	if (db_name,) in db_list:
		print('database already exists')
		delete = input("Do you want to delete the existing database? (y/n): ")
		if delete == 'y':
			db.execute('drop database ' +db_name)
			print('database deleted successfully')
			ask_new_db = input('Create a new database? (y/n): ')
			if ask_new_db == 'y':
				db_name = input('Enter a new database name: ')
				db.execute('create database ' +db_name)
				print('New database created')
			else:
				sys.exit()
		elif delete == 'n':
			print('continue using the existing database')
	else:
		print('database does not exist')
		db_name = input("Enter a new database name: ")
		db.execute('create database ' +db_name)
		print('New database created')




		

