from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder

Config.set('graphics', 'width', '350')
Config.set('graphics', 'height', '650')


class SignUp(App):
    def build(self):
        return Builder.load_file("signup.kv")
