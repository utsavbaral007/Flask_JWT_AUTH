from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

mysql = MySQL()

app.config['MYSQL_USER'] = 'Utsav'
app.config['MYSQL_PASSWORD'] = '2828'
app.config['MYSQL_DB'] = 'file_upload'
app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/upload', methods = ['POST'])
def upload():
	file = request.files['inputFile']
	text = request.form.get['description']
	cur = mysql.connection.cursor()
	cur.execute("INSERT INTO upload(title, file) VALUES(%s, %s)", (text, file.read()))
	mysql.connection.commit()
	return "saved " +file.filename+ " to database"

if __name__ == '__main__':
	app.run(debug=True)