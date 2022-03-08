import os

os.environ['DISPLAY'] = ":0.0"
os.environ['KIVY_WINDOW'] = 'egl_rpi'

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel
from kivy.properties import ObjectProperty
from kivy.animation import Animation

from datetime import datetime
from kivy.uix.widget import Widget
from pidev.Joystick import Joystick
joy = Joystick(0, False)
from threading import Thread
from time import sleep

time = datetime

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
ADMIN_SCREEN_NAME = 'admin'


class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)  # White



class MainScreen(Screen):
    among_us = ObjectProperty(None)
    """
    Class to handle the main screen and its associated touch events
    """
    count = 1
    baka = 0

    def joy_update(self):
        while True:
            self.button_cheese.text = str(joy.get_button_state(9))
            sleep(.1)
            text = self.button_cheese.text
            self.liz_is_h8r.text = str(joy.button_combo_check([0,1]))
            self.x_axis_button.text = str(joy.get_axis("x"))
            self.y_axis_button.text = str(joy.get_axis("y"))


    def start_joy_thread(self):
        Thread(target=self.joy_update, daemon=True).start()
    def pressed(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        print("Callback from MainScreen.pressed()")

    def btn(self):
        self.test_button.text = str(self.count)
        self.count += 1

    def sus(self):
        if self.among_us.text == "Sus":
          self.among_us.text = "Imposter"
        else:
            self.among_us.text = "Sus"

    def button_combo_check(self):
        if joy.button_combo_check([0,1]):
            self.liz_is_h8r.text= "1"
            self.refresh()

    def cheese(self):
        SCREEN_MANAGER.current = 'passCode'

    def animate_it(self, widget):
        self.baka += 1
        self.cheese_button = str(self.count)
        if self.baka < 2:
            anim = Animation(x=50) + Animation(size=(80, 80), duration=2.)
            anim.start(widget)
        else:
            SCREEN_MANAGER.current = 'passCode'
    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        SCREEN_MANAGER.current = 'passCode'


class AdminScreen(Screen):
    """
    Class to handle the AdminScreen and its functionality
    """

    def __init__(self, **kwargs):
        """
        Load the AdminScreen.kv file. Set the necessary names of the screens for the PassCodeScreen to transition to.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        PassCodeScreen.set_transition_back_screen(MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"

        super(AdminScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        quit()


"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))

"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()
