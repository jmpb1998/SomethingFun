# main.py

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window
import os

class WifiWindow(Screen):
    ssid = ObjectProperty(None)
    password = ObjectProperty(None)
    keys = ObjectProperty(None)
    
    caps = False
    caps_locked = False
    ssid_write = False
    passwd_write = False
    
    def right_button(self):
        sm.current = 'home'
    
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

screens = [HomeWindow(name="home"), WifiWindow(name="wifi"),MainWindow(name="main")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "home"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
