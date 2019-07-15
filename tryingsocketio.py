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
    username = db.Column(db.String(30), unique=True, nullable=False)
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
    
def login(jsonget):
    user = User(email = jsonget['email'], password = jsonget['password'] )
    try: 
        user_id = User.query.filter_by(email = user.email).first()
        if user_id == None:
            # return False
            print("return False")
            return false
        else:
            if user.password == user_id.password: 
                #return True
                print('return true')
                return true 
    except: 
        pass;
    print('return false')
    return false
                
def signup(jsonget): 
    user = User(name = jsonget['name'], email = jsonget['email'], password = jsonget['password'])
    
    try: 
        db.session.add(user)
        
    except: 
        pass; 
    
    


@app.route('/')
def index():
    return render_template('trial.html')

@socketio.on('connect')
def test_connect():
    print('connection success:')
    emit('after connect', {'data':'Lets dance'})
    
@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)

@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))
    print(json)
    #try:
    if(json['name'] == ''):
        print('doing Login')
        auth_login = login(json)
        print(tyupe(auth_login))
        print(auth_login)
        socketio.emit('auth_login', auth_login)
    else:
        signup()
    send(json,json=True)
    #except AttributeError:
     #   print('skipped')
      #  pass
@socketio.on('my event')
def handle_my_custom_event(jsonrecv, methods=['GET', 'POST']):
    print('received my event: ' + str(jsonrecv))
    print('doing Login')
    auth_login = login(json)
    print(tyupe(auth_login))
    print(auth_login)
    socketio.emit('auth_login', auth_login)
    print("message received")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
