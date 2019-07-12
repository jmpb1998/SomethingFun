from datetime import datetime
from flask import Flask,render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_socketio import send, emit
import json
from peewee import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hi'
app.config['SQALCHEMY_DATABASE_URI'] = 'sqlite:///examples.db'
db = SQLAlchemy(app)
socketio = SocketIO(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    datalist = db.relationship('Data', backref='user', lazy=True)
    
    def __init__(self, id, data):
        self.id = id
        self.data = data
    
    def __repr__(self):
        return f"User('{self.username}')"
    
class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    
    def __repr__(self):
        return f"Data('{self.date}')"



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
    
    send(json,json=True)
    
@socketio.on('my event')
def handle_my_custom_event(jsonrecv, methods=['GET', 'POST']):
    print('received my event: ' + str(jsonrecv))
    try:
        socketio.emit('my response', jsonrecv)
        print("message received")
    except KeyError:
        pass;

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
