from kivy.app import app
from kivy.uix.widget import Widget
from kivy.lang import Builder

Builder.load_file('animations.kv')

class MyLayout(Widget):
    pass

class AwesomeApp(App):
    def build(self):
        return MyLayout()

if _name_ == '_main_':
    AwesomeApp().run()