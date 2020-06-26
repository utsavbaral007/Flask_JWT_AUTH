from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from database import connect_db

app = Flask(__name__)

connect_db()

app.config['SQLALCHEMY_DATABASE_URI'] = ('mysql://utsav:2828@localhost/'+connect_db.db_name)
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
	description = request.form.get('description')
	file = request.files['inputFile']
	new_file = upload_file(description = description, file= file.read())
	db.session.add(new_file)
	db.session.commit()
	return 'file ' +file.filename+ ' uploaded successfully'

if __name__ == '__main__':
	app.run(debug=True)