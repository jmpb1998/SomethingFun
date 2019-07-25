# main.py

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.popup import Popup
import os
import socketio


sio = socketio.Client()
sio.connect('http://7e88826a.ngrok.io')
jsondata = { 'auth_boolean': 2, 'error': 'hi' }

@sio.on('auth_login')
def on_json(data):
    if data['auth_boolean'] == 0:
        sm.current = "home"
    else:
        jsondata = data


class WifiWindow(Screen):
    ssid = ObjectProperty(None)
    password = ObjectProperty(None)
    keys = ObjectProperty(None)

    caps = False
    caps_locked = False
    ssid_write = False
    passwd_write = False

    def build(self):
        self.root = get_main_window()
        with self.rootcanvas:
            Color(rgba=(.5, .5, .5))
            Rectangle(size=self.root, pos=self.root.pos)
        return self.root

    def right_button(self):
        sm.current = 'login'

    def ssid_focus(self):
        self.ssid_write = True
        self.passwd_write = False

    def passwd_focus(self):
        self.passwd_write = True
        self.ssid_write = False

    def caps_lock(self):
        if self.caps == False:
            self.caps = True
            self.caps_locked = True
        else:
            self.caps = False
            self.caps_locked = False

    def button_caps(self):
        if self.caps_locked == False:
            self.caps = False

    def shift_caps(self):
        self.caps = True

    def key_press(self, key):
        if self.ssid_write == True:
            if key == 'back':
                sObject = slice(len(self.ssid.text) - 1)
                self.ssid.text = self.ssid.text[sObject]
            else:
                if self.caps == True:
                    self.ssid.text = self.ssid.text + key.upper()
                else:
                    self.ssid.text = self.ssid.text + key
        if self.passwd_write == True:
            if key == 'back':
                sObject = slice(len(self.password.text) - 1)
                self.password.text = self.password.text[sObject]
            else:
                if self.caps == True:
                    self.password.text = self.password.text + key.upper()
                else:
                    self.password.text = self.password.text + key

    def wifi_connect(self):
        command = """sudo iwlist wlp2s0 scan | grep -ioE 'ssid:"(.*{}.*)'"""
        result = os.popen(command.format(self.ssid.text))
        result = list(result)

        if "Device or resource busy" in result:
                return None
        else:
            ssid_list = [item.lstrip('SSID:').strip('"\n') for item in result]
            print("Successfully get ssids {}".format(str(ssid_list)))


        for name in ssid_list:
            try:
                result = self.connection(name)
            except Exception as exp:
                print("Couldn't connect to name : {}. {}".format(name, exp))
            else:
                if result:
                    print("Successfully connected to {}".format(name))

    def connection(self, name):
        try:
            os.system("nmcli d wifi connect {} password {}".format(name,
       self.password.text))
        except:
            raise
        else:
            return True

class HomePage(Screen):
    def logoutBtn(self):
        sm.current = "login"

class HomeWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        sm.current = "main"

    def createBtn(self):
        sm.current = "wifi"

    def logoutBtn(self):
        sm.current = "login"

    def startSensor(self):
        #path to python file of biosensor
        os.chroot(path)
        os.system("python sensor.py")

        print(os.listdir(path))

class LoginWindow(Screen):

    email = ObjectProperty(None)

    password = ObjectProperty(None)

    keys = ObjectProperty(None)

    error = ObjectProperty(None)

    caps = False
    caps_locked = False
    email_write = False
    passwd_write = False
    '''
    @sio.on('auth_login')
    def on_json(data):
        print(data)
        print(data['auth_boolean'])
        if data['auth_boolean'] == 0:
            sm.current = "home"
        else:
            LoginWindow.errorcall()
       '''

    def errorcall(self):
        print(jsondata)
        if jsondata['auth_boolean'] == 1:
            self.error.text = 'Email already registered'
        if jsondata['auth_boolean'] == 2:
            self.error.text = 'Wrong email or password'
        if jsondata['auth_boolean'] == 3:
            self.error.text = 'Empty field'
        if jsondata['auth_boolean'] == 4:
            self.error.text = 'Server Error'
        if jsondata['auth_boolean'] == 5:
            self.error.text = 'Email not valid'

    def email_focus(self):
        self.email_write = True
        self.passwd_write = False

    def passwd_focus(self):
        self.passwd_write = True
        self.email_write = False

    def caps_lock(self):
        if self.caps == False:
            self.caps = True
            self.caps_locked = True
        else:
            self.caps = False
            self.caps_locked = False

    def button_caps(self):
        if self.caps_locked == False:
            self.caps = False

    def shift_caps(self):
        self.caps = True

    def key_press(self, key):
        if self.email_write == True:
            if key == 'back':
                sObject = slice(len(self.email.text) - 1)
                self.email.text = self.email.text[sObject]
            else:
                if self.caps == True:
                    self.email.text = self.email.text + key.upper()
                else:
                    self.email.text = self.email.text + key
        if self.passwd_write == True:
            if key == 'back':
                sObject = slice(len(self.password.text) - 1)
                self.password.text = self.password.text[sObject]
            else:
                if self.caps == True:
                    self.password.text = self.password.text + key.upper()
                else:
                    self.password.text = self.password.text + key




    def loginBtn(self):

        sio.emit('json', {'name': '', 'email': self.email.text, 'password': self.password.text})


    def wifiBtn(self):
        sm.current = "wifi"

    def nologin(self):
        sm.current = "home"


class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"

    def on_enter(self, *args):
        pass

class P(Screen):
    error = ObjectProperty(None)

    def returnlogin(self):
        popup.dismiss()


class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")
sm = WindowManager()


screens = [HomeWindow(name="home"), WifiWindow(name="wifi"),MainWindow(name="main"), LoginWindow(name="login"), HomePage(name="first_page")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "first_page"


class MyMainApp(App):
    def build(self):
        return sm


def alertPopup(data):
    popup = Popup(title = 'Error Occoured',
content=Label(text = 'hello'),
size_hint=(None, None), size=(dp(600), dp(200)))
    popup.open()


if __name__ == "__main__":
    MyMainApp().run()
