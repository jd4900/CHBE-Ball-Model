from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
from kivy.config import Config
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button

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

    def get_inputs(self, button, state):
        if button.group == "Hardness" and state is "down":
            self.Hardness=button.text
        elif button.group == "Acidity" and state is "down":
            self.Acidity=button.text
        elif button.group == "BOD" and state is "down":
            self.BOD=button.text
        elif button.group == "Hardness" and state is not "down":
            self.Hardness = None
        elif button.group == "Acidity" and state is not "down":
            self.Acidity = None
        elif button.group == "BOD" and state is not "down":
            self.BOD = None


    def check_inputs(self):
        if any(item == None for item in [self.Hardness, self.Acidity, self.BOD]):
            logging.warning("Input should not be None")
            self.mkpopup()
        else:
            validate_inputs(self.Hardness, self.Acidity, self.BOD)

    def press(self, *args):
        self.get_inputs(args[0], args[1])

    def execute(self):
        self.check_inputs()

    def mkpopup(self):
        layout = GridLayout(cols = 1, padding = 10)
        
        popupLabel = Label(text="Missing Input!")
        closeButton = Button(text = "Click to Return")

        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)

        popup = Popup(
            title="Warning!", 
            content = layout
        )
        
        popup.open()

        closeButton.bind(on_press = popup.dismiss)


class BallModelApp(App):
    def build(self):
        self.title = "Ball Model"
        return BallModelUI()

if __name__ == '__main__':
    BallModelApp().run()
