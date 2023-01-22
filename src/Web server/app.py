import jwt
import os
from flask.helpers import make_response
from flask.json import jsonify
from functools import wraps
from hashlib import sha256
from flask import request, Flask, current_app
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy

from database.user import user

app = Flask('app', __name__)

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

@app.route('/register', methods = ['POST'])
def register():
    json = request.get_json()
    
    login = json['login']

    username = json['username']

    password = json['password']

    token_required = json['token_required']
    
    user = User.query.filter_by(login = login).first()

    if user:
        return { 
            'error': 'Could not found a user with login: <login>'
        }, 409

    user = User(
        login = login,
        username = username,
        password = sha256(password.encode()).hexdigest(),
        token_required = token_required
    )

    db.session.add(user)
    db.session.commit()

    return user.serialize()

@app.route('/login', methods = ['POST'])
def login():
    json = request.get_json()

    login    = json['login']

    password = json['password']


    user = User.query.filter_by(login = login).first()

    if not user:
        return {
            'error': 'Could not found a user with login: <login>'
        }, 404
    
    pass_hash = sha256(password.encode()).hexdigest()

    if user.password == pass_hash:
        payload = {
            'id': user.id,
            'exp': datetime.utcnow() + timedelta(minutes = 30)
        }

        token = jwt.encode(payload, current_app.config.get('SECRET_KEY'), algorithm="HS256")

        return { 'access': token }, 200

    return { 
        'error': 'Wrong password'
    }, 401


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        
        if not token:
            return '<h1>There is no token<h1>'
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return '<h1>Incorrect token<h1>'
        return f(*args, **kwargs)

    return decorated


@app.route('/protected')
def protected():
    token = request.args.get('token')

    if not token:
        return "<h1>Hello, no token was provided</h1>"
    
    try:
        jwt.decode(token, app.config.get('SECRET_KEY'), algorithms=['HS256'])
    except:
        return "<h1>Hello, Could not verify the token</h1>"
    
    return "<h1>Hello, token which is provided is correct </h1>"


if __name__ == "__main__":
    app.run(debug = True)