# main.py

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window
import os
import socketio 


sio = socketio.Client()
sio.connect('http://7c665d26.ngrok.io')


class WifiWindow(Screen):
    ssid = ObjectProperty(None)
    password = ObjectProperty(None)
    keys = ObjectProperty(None)
    
    caps = False
    caps_locked = False
    ssid_write = False
    passwd_write = False
    
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


class HomeWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        sm.current = "main"

    def createBtn(self):
        sm.current = "wifi"
        
    def logoutBtn(self):
        sm.current = "login"

class LoginWindow(Screen):

    email = ObjectProperty(None)

    password = ObjectProperty(None)

    keys = ObjectProperty(None)
    
    caps = False
    caps_locked = False
    email_write = False
    passwd_write = False
    
    @sio.on('auth_login')
    def on_json(data):

        print(data)
        print(data['auth_boolean'])
        if data['auth_boolean'] == 0:
            sm.current = "home"

    
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


class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"

    def on_enter(self, *args):
        pass


class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("my.kv")
sm = WindowManager()

screens = [HomeWindow(name="home"), WifiWindow(name="wifi"),MainWindow(name="main"), LoginWindow(name="login")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
