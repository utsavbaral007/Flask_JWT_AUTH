# Flask API with JWT Authentication
JWT is a standard that defines a compact way to securely transmit information between a client and a server as a JSON object. The compact size of token makes the tokens easy to transfer through an URL, POST parameter, or inside an HTTP header. Also, since they are self-contained they include all the necessary information about a user so the database does not need to be queried more than once. The information in a JWT can be trusted because it is digitally signed using a secret or public/private key pair.

Let's now go through this simple Flask project and see how JWT is used to secure the API.

## Packages used 
All packages that are required for this project is kept inside `requirements.txt` file.

## Let's Start
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
