from flask import Flask,render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import json
from peewee import *
from datetime import datetime


app = Flask(__name__)
app.config["SECRET_KEY"] = "hi"
app.config['SQALCHEMY_DATABASE_URI'] = 'sqlite:///patientdata.db'
app.debug = True
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    data = db.relationship('Data', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}')"

class Post(db.Model):
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
def anything():
    return render_template("basic_temp.html")

def messageReceived(methods=['GET']):
    print('GET message was received!!!')

def messageReceived(methods=['POST']):
    print('POST message was received!!!')


if __name__ == "__main__":
    initialize()
    socketio.run(app, port=8000)
