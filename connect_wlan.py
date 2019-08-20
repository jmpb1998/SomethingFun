from datetime import datetime
from flask import Flask,render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_socketio import SocketIO
from flask_socketio import send, emit
import json
from peewee import *
#from validate_email import validate_email


#initiate app
app = Flask(__name__)
#initiate database to the right path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////root/maindata/SomethingFun-master/example.db'

#create objects db(database) - socketio
db = SQLAlchemy(app)
socketio = SocketIO(app)

#class object of user
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    datalist = db.relationship('Data', backref='email', lazy=True)
    token = db.Column(db.String(60))
    last_data_logged = db.Column(db.DateTime)

    def __repr__(self):
        return f"User('{self.id}')"

#class object of data
class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    concentration = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.String(150))
    year = db.Column(db.Integer, nullable=False, default=datetime.utcnow().year)
    month = db.Column(db.String(20), nullable=False, default=datetime.utcnow().month)
    day = db.Column(db.Integer, nullable=False, default=datetime.utcnow().day)
    #date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sympton1 = db.Column(db.Integer)
    sympton2 = db.Column(db.Integer)
    sympton3 = db.Column(db.Integer)

    done = db.Column(db.Boolean, default = False)
    #refers to the User who owns the data
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



    def __repr__(self):
        return f"Data('{self.id}')"


def login(jsonget, returnBoolean):
    user = User(email = jsonget['email'], password = jsonget['password'] )
    try:
        user_id = User.query.filter_by(email = user.email).first()
        if user_id == None:
            # return False
            print (user_id)
            print("return False")
            returnBoolean['auth_boolean'] = False
            return 2
        else:
            if user.password == user_id.password:
                #return True
                print('return true')
                returnBoolean['auth_boolean'] = True
                return 0
            else:
                return 2
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return 4
        print('return false')
        returnBoolean['auth_boolean'] = False


def signup(jsonget):
    try:
        tmp_user = User(name = jsonget['name'], email = jsonget['email'], password = jsonget['password'])
        print(type(tmp_user))
        if validate_email(tmp_user.email):
            user_id = User.query.filter_by(email = tmp_user.email).first()
            if user_id == None:
                db.session.add(tmp_user)
                db.session.commit()
                print('successfully registered')
                return 0
            else:
                print('email already registered')
                return 1
        else:
            print('email not valid')
            return 5
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return 4


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


@socketio.on('disconnect')
def disconnect():
    print('disconnect')
    emit('user disconnected')

#handle login/register data
#if name empty do register
@socketio.on('json')
def handle_json(json):
    returnBoolean = { 'auth_boolean': 0, 'error': None}
    returnError = {'error_signup': 0}
    print('received json: ' + str(json))
    try:
        if(json['name'] == ''):
            print('doing Login')
            error = login(json, returnBoolean)
            returnBoolean['auth_boolean'] = error
            print( returnBoolean['auth_boolean'])
            emit('auth_login', returnBoolean)
            print('after emit')
        else:
            print('signup happening')
            error = signup(json)
            returnError['error_signup'] = error
            emit('auth_signup', returnError)
    except KeyError:
        pass;
    except TypeError:
        pass;
    #except AttributeError:
     #   print('skipped')
      #  pass

#handle received data
@socketio.on('data_measure_user')
def handle_data_user(json_data, methods=['GET', 'POST']):
    print ('received my event: ' + str(json_data))
    user = Data(user_id = json_data['user_id'])
    data_set = Data(concentration = json_data['concentration'], sympton1 = json_data['sympton1'], sympton2 = json_data['sympton2'], sympton3 = json_data['sympton3'], comments = json_data['comments'])
    try:
        print('Loading data')
        db.session.add(data_set, user)
        db.session.commit()
        return 0
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return 4

#handle request from data - app
#probably useless now
@socketio.on('data_request')
def handle_data_request(json_request, methods=['GET', 'POST']):
    print('Handling data request')

    #fetch last data logged by the user and user token
    last_data_logged = json_request['last_data_logged']
    user_token = json_request['token']

    #json struct
    returnData = {
        'concentration': {},
        'date': {}
    }

    #find user by token
    user = User.query.filter_by(token = user_token).first()

    data_itr = iter(user.data)
    #find data id in
    index = 0
    for date in user.datalist:
        if last_data_logged == date:
            data_log_id = index
            #add condition to warn if last data logged is last data in database
            #add smth to get out of loop
        index += 1

    for (concentration, date) in range (user.datalist[data_log_id],len(user.datalist)):
        #add to json
        returnData.update({'concentration': {date.id: concentration}, 'date': {date.id: date}})

    emit('data_upload', returnData)


@socketio.on('pi2database')
def store(json_data, methods=['GET', 'POST']):
    print('Storing data from PI')
    try:
        user_email = json_data['email']
        user_concentration = json_data['concentration']
        #user_id = User.query.filter_by(email = user_email).first()
        tmp_data = Data(concentration = user_concentration, email = user_email)
        db.session.add(tmp_data)
        db.session.commit()
        print('Successfully stored data')
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)

@socketio.on('database2app')
def upload(json_data, methods=['GET', 'POST']):

    print('Uploading data to App')
    try:
        user_email = json_data['email']
        print(user_email)
        tmp_user = User.query.filter_by(email = user_email).first()

        '''listUpload = []
        for item in tmp_user.datalist:
            if item.done == False:
                listUpload.append(item)'''


        #json_upload = {'alldata': tmp_user.datalist}
        conclist = []
        yearlist = []
        monthlist = []
        daylist = []
        for info in tmp_user.datalist:
            if not info.done:
                conclist.append(info.concentration)
                yearlist.append(info.year)
                monthlist.append(info.month)
                daylist.append(info.day)
        data = { 'concentration': conclist, 'year': yearlist, 'month': monthlist, 'day': daylist}
        emit('patientData', data, callback = ack())
        print(tmp_user.datalist)
        for item in tmp_user.datalist:
            item.done = True
        db.session.commit()

    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)

def ack():
    print ('Successfully uploaded')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')





'''@socketio.on('my event')
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
            signup(json)
    except KeyError:
        pass;
    except TypeError:
        pass;
    send(json,json=True)'''
