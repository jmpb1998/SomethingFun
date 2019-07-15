import socketio
sio = socketio.Client()
sio.connect('http://cd5de449.ngrok.io')
sio.emit('json', {'name': '', 'email': 'hello', 'password': 'hi'})
