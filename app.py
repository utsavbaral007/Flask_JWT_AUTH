from flask import Flask, render_template, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import mysql.connector
import sys

conn = mysql.connector.connect(host = 'localhost', user = 'utsav', password = '2828')
db = conn.cursor()
db.execute('CREATE DATABASE IF NOT EXISTS learngaroo_flask_api')
db.execute('SHOW DATABASES')
db_list = db.fetchall()
print(db_list)
db_name = 'learngaroo_flask_api'
if (db_name,) in db_list:
	keep_db = input("Do you want to keep using the database? (y/n): ")
	if keep_db == 'y':
		db.execute('USE '+db_name)
	elif keep_db == 'n':
		db.execute('DROP DATABASE learngaroo_flask_api')
		db.execute('CREATE DATABASE '+db_name)
	else:
		print("Please enter y or n")
		sys.exit()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = ('mysql://utsav:2828@localhost/learngaroo_flask_api')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class upload_file(db.Model):
	id = db.Column(db.Integer, primary_key = True, nullable = False)
	description = db.Column(db.String(200), unique = True, nullable = False)
	file = db.Column(db.LargeBinary(length = 4294967295), nullable = False)
	def __init__(self, description, file):
		self.description = description
		self.file = file

class upload_schema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = upload_file

db.create_all()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/upload', methods = ['POST'])
def upload():
	response = request.post('127.0.0.1/upload', )
	description = request.form.get('description')
	file = request.files['inputFile']
	new_file = upload_file(description = description, file= file.read())
	db.session.add(new_file)
	db.session.commit()
	return 'file ' +file.filename+ ' uploaded successfully'


if __name__ == '__main__':
	app.run(debug=True)