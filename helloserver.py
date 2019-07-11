from datetime import datetime
from flask import Flask,render_template, url_for, flash, redirect
from flask_socketio import SocketIO
from flask_socketio import send, emit
from flask_sqlalchemy import SQLAlchemy
import json
from peewee import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "hi"
app.config['SQALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
db = SQLAlchemy(app)
socketio = SocketIO(app)
app.debug = True

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    data = db.relationship('Data', backref='user', lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}','{self.image_file}')"
    
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Data('{self.date}')"

@app.route("/")
def anything():
    return render_template("trial.html")

def messageReceived(methods=['GET']):
    print('GET message was received!!!')
    
def messageReceived(methods=['POST']):
    print('POST message was received!!!')


if __name__ == "__main__":
    app.run(debug=True)
