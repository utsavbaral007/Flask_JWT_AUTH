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