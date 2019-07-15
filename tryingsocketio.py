from datetime import datetime
from flask import Flask,render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_socketio import send, emit
import json
from peewee import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////root/maindata/python/sensus/server/try_database.db'
db = SQLAlchemy(app)
socketio = SocketIO(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    datalist = db.relationship('Data', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}')"
    
class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    
    def __repr__(self):
        return f"Data('{self.date}')"
    
def login(jsonget, returnBoolean):
    user = User(email = jsonget['email'], password = jsonget['password'] )
    try: 
        user_id = User.query.filter_by(email = user.email).first()
        if user_id == None:
            # return False
            print("return False")
            returnBoolean['auth_boolean'] = False
            return None
        else:
            if user.password == user_id.password: 
                #return True
                print('return true')
                returnBoolean['auth_boolean'] = True
                return None
    except: 
        pass;
    print('return false')
    returnBoolean['auth_boolean'] = False
    return None
                
def signup(jsonget): 
    try: 
        tmp_user = User(name = jsonget['name'], email = jsonget['email'], password = jsonget['password'])
        print(type(tmp_user))
        db.session.add(tmp_user)
        db.session.commit()
    except: 
        pass;


@app.route('/')
def index():
    return render_template('trial.html')

@socketio.on('connect')
def test_connect():
    print('connection success:')
    emit('after connect', {'data':'Lets dance'})
    
@socketio.on('just_connected')
def handle_my_custom_event(welcome):
    print('received welcome: ' + welcome['data'])

@socketio.on('json')
def handle_json(json):
    returnBoolean = { 'auth_boolean': True }
    print('received json: ' + str(json))
    try:
        if(json['name'] == ''):
            print('doing Login')
            login(json, returnBoolean)
            print( returnBoolean['auth_boolean'])
            emit('auth_login', returnBoolean)
            print('after emit')
        else:
            print('signup happening')
            signup(json)
    except KeyError:
        pass;
    except TypeError:
        pass;
    send(json,json=True)
    #except AttributeError:
     #   print('skipped')
      #  pass
@socketio.on('my event')
def handle_my_custom_event(jsonrecv, methods=['GET', 'POST']):
    returnBoolean = { 'auth_boolean': True }
    print('received my event: ' + str(jsonrecv))
    try:
        if(json['name'] == ''):
            print('doing Login')
            login(json, returnBoolean)
            socketio.emit('auth_login', returnBoolean)
            print('after emit')
        else:
            signup()
    except KeyError:
        pass;
    except TypeError:
        pass;
    send(json,json=True)
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
