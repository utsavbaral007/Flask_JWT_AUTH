# Flask API with JWT Authentication
JWT is a standard that defines a compact way to securely transmit information between a client and a server as a JSON object. The compact size of token makes the tokens easy to transfer through an URL, POST parameter, or inside an HTTP header. Also, since they are self-contained they include all the necessary information about a user so the database does not need to be queried more than once. The information in a JWT can be trusted because it is digitally signed using a secret or public/private key pair.

Let's now go through this simple Flask project and see how JWT is used to secure the API.

## Packages used 
All packages that are required for this project is kept inside `requirements.txt` file.

## Let's Start by building API first
In your project directory create a `app.py` script file. This is where we write code for out database model, API and database configurations. 
#### This is how we import packages necessary for project:
```
from flask import Flask, render_template, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import mysql.connector
from authentication import check_for_token
```
- `render_template` :  Instead of returning hardcode HTML from the function, a HTML file can be rendered by the `render_template()`.
- `request` : In any web app, you'll have to process incoming request data from users. Flask, like any other web framework, allows you to access the request data easily.
- `jsonify` : The `jsonify` function in `flask` returns a `flask`. `Response()` object that already has the appropriate content-type header 'application/json' for use with json responses.
- `make_response` :  This function can be called instead of using a return and you will get a response object which you can use to attach headers.
- `SQLAlchemy` : `SQLAlchemy` is a library that facilitates the communication between Python programs and databases. Most of the times, this library is used as an Object Relational Mapper (ORM) tool that translates Python classes to tables on relational databases and automatically converts function calls to SQL statements.
- `Marshmallow` : `marshmallow` is an ORM/ODM/framework-agnostic library for converting complex datatypes, such as objects, to and from native Python datatypes.
- `mysql.connector` : helps python sever to communicate with MySQL servers, and how to use it to develop database applications.
### Moving on to the next part
```
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = ('mysql://<username>:<password>@<host>/database_name')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```
`__name__` is just a convenient way to get the import name of the place the app is defined. Flask uses the import name to know where to look up resources, templates, static files, instance folder, etc.

Applications need some kind of configuration. There are different settings you might want to change depending on the application environment like toggling the debug mode, setting the secret key, and other such environment-specific things. The config attribute of the Flask object. This is the place where Flask itself puts certain configuration values and also where extensions can put their configuration values.

### Now in this sections we'll see how to create model for API.
```
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
```
`db` and `ma` create instances for `MYSQLAlchemy` and `Marshmallow`.
We create class `upload_file` which contains the model that will be used as database's table.
`__init__` does act like a constructor. You'll need to pass `self` to any class functions as the first argument if you want them to behave as non-static methods. `self` are instance variables for your class.
`upload_schema` uses `marshmallow` to serialize the model `upload_file`.
`db.create_all()` creates database table in the given database.
### Now we provide route
```
@app.route('/')
@check_for_token
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
```
Inside the directory create a `templates` folder and inside that folder create `index.html` file. Inside `index.html`,
```
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1.0" />
		<title>File Upload</title>
	</head>
	<body>
		<form
			style="display: flex; flex-direction: column; width: 20%;"
			method="POST"
			action="/upload"
			enctype="multipart/form-data"
		>
			<input type="file" name="inputFile" />
			<textarea
				placeholder=""
				name="description"
				rows="4"
				col="1"
				placeholder="description..."
			></textarea>
			<button type="submit">Submit</button>
		</form>
	</body>
</html>
```
## JWT Authentication
Create a `authentication.py` script file in root directory and write the following code.
```
from flask import Flask, jsonify, request, make_response
from functools import wraps
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'

def check_for_token(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = request.args.get('token')
		if not token:
			return jsonify({'message' : 'Token missing'}), 403
		try:
			data = jwt.decode(token, app.config['SECRET_KEY'])
		except:
			return jsonify({'message' : 'Invalid token'}), 403
		return f(*args, **kwargs)
	return decorated

@app.route('/login')
def login():
	auth = request.authorization
	if auth and auth.password == 'password':
		token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=20)}, app.config['SECRET_KEY'])
		return jsonify({'token' : token.decode('UTF-8')})
	else:
		return make_response('Unable to verify'), 403

if __name__ == '__main__':
	app.run(debug=True)
```
- `wraps` : Also known as Decorator is a function that wraps and replaces another function. Since the original function is replaced, you need to remember to copy the original function's information to the new function.
- `jwt` :  The `jwt` library provides a way to manage the authentication process when we need to use JWT tokens in our flask applications.
- `datetime` : The `datetime` module supplies classes for manipulating dates and times in both simple and complex ways.

`SECRET_KEY` will be used for securely signing the session cookie and can be used for any other security related needs by extensions or your application.

#### Let's see with decorator first
We will call our function `check_for_token()`. Our aim with this decorator is to be able to decorate functions that are normally decorated with `@app.route()` and what it will do is decline access to webpages if the user doesn't have or provide an appropriate jwt. We wrap our inner function with `@wraps`. In our wrapped function we will define a variable `token` to which will be assigned a value of the key `('token')`. Then we attempt to decode the `token` using `decode` method of `jwt`. The first argument of the decode is encoded `token` and second is the `SECRET_KEY` and there's an optional third argument which is the algorithm. Now we wrap in an `except` handler so that if there's any problem with the token provided, the program doesn't stop. We finish our decorator returning `f(*args, **kwargs)` and `decorated` ready to be called downstream.

#### Let's work with generating jwt token
We have imported `check_for_token()` function inside `app.py` and have decorated the private authorized function with `@check_for_token` decorator. So `@app.route('/')` is only accessible if a current on expired token is passed in.

We need one more function. This is where we get the token after we pass username and password. We will be using Postman to send request. so if `auth.password == 'password'` then encode a token for the user. We pass dictionary as the first argument containing `username` which we are going to provide from postman and an `exp` condition which tells jwt when the token encoded is going to expire. Here we get the current time and add the amount of time from now the token will expire. i.e. current time = `datetime.datetime.utcnow()` and expire time = `datetime.timedelta(minutes=20)`. Finally we pass in out secret key, `app.config['SECRET_KEY']`. We use decode because since the token is generated in 'py' we need to decode it as a regular string. So we use `token.decode('UTF-8')`.

## Demo
Now what we do it open Postman and select GET request, add the url : `127.0.0.1:5000/login`. In 'Authorization' section add 'Type' to 'Basic auth'. Send the request without providing username and password. We get,
![Screenshot (41)](https://user-images.githubusercontent.com/50907127/85978745-1185c580-b9ff-11ea-8975-2312cca9f303.png)

Provide any username you want and set password as 'password'. We get the token.
![Screenshot (42)](https://user-images.githubusercontent.com/50907127/85979260-d9cb4d80-b9ff-11ea-99c8-ba437069ccad.png)

Copy the token, and open url: `127.0.0.1:5000/login`. We get the message that 'Token missing' because we haven't provided any token.
![Screenshot (43)](https://user-images.githubusercontent.com/50907127/85979569-77bf1800-ba00-11ea-90a3-6b98d51dc141.png)

Now we provide the token as: `127.0.0.1:5000?token=<:token>`. We can get access to `127.0.0.1:5000/`
![Screenshot (44)](https://user-images.githubusercontent.com/50907127/85979850-fc119b00-ba00-11ea-8579-4a8826b80224.png)

If we provide an invalid token, we get message as 'Invalid token'
![Screenshot (45)](https://user-images.githubusercontent.com/50907127/85980307-dcc73d80-ba01-11ea-92c9-7dd5b65f0222.png)






