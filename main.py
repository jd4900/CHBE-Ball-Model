from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
from kivy.config import Config
import logging

Config.set('graphics', 'resizable', True)

def validate_inputs(Hardness, Acidity, BOD):
    if Hardness=='10 ppm' and Acidity=='7' and BOD=='Low':
        logging.info("Dispensing good stuff")
        return True
    else:
        logging.info("Dispensing bad stuff")
        return False

class BallModelUI(Widget):

    Hardness = None
    Acidity = None
    BOD = None

    def get_inputs(self, button):
        if button.group == "Hardness":
            self.Hardness=button.text
        elif button.group == "Acidity":
            self.Acidity=button.text
        elif button.group == "BOD":
            self.BOD=button.text

    def check_inputs(self):
        if any(item == None for item in [self.Hardness, self.Acidity, self.BOD]):
            logging.warning("Somethings Not Right!")
        else:
            validate_inputs(self.Hardness, self.Acidity, self.BOD)

    def press(self, *args):
        self.get_inputs(args[0])

    def execute(self):
        self.check_inputs()

class BallModelApp(App):
    def build(self):
        self.title = "Ball Model"
        return BallModelUI()

if __name__ == '__main__':
    BallModelApp().run()
