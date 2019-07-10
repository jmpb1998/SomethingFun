from flask import Flask,render_template, url_for, flash, redirect
from flask_sqalchemy import SQLAlchemy
import json
from peewee import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "hi"
app.config['SQALCHEMY_DATABASE_URI'] = 'sqlite:///patientdata.db'
app.debug = True

class User(db.Model):
    id = db.Column(db.integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')


@app.route("/")
def anything():
    return render_template("session.html")

def messageReceived(methods=['GET']):
    print('GET message was received!!!')
    
def messageReceived(methods=['POST']):
    print('POST message was received!!!')


if __name__ == "__main__":
    initialize()
    socketio.run(app, port=8000)
