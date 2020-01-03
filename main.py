from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
from kivy.config import Config
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.logger import Logger

import time

Config.set('graphics', 'resizable', True)

def validate_inputs(Hardness, Acidity, BOD):
    if Hardness=='10 ppm' and Acidity=='7' and BOD=='Low':
        Logger.info('APP: Dispensing good stuff')
        return True
    else:
        Logger.info('APP: Dispensing bad stuff')
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

    def clear_button_state(self):
            self.ids.button1.state = "normal"
            self.ids.button2.state = "normal"
            self.ids.button3.state = "normal"
            self.ids.button4.state = "normal"
            self.ids.button5.state = "normal"
            self.ids.button6.state = "normal"
            self.ids.button7.state = "normal"
            self.ids.button8.state = "normal"
            self.ids.button9.state = "normal"

    def check_inputs(self):
        if any(item == None for item in [self.Hardness, self.Acidity, self.BOD]):
            Logger.warning('APP: Input should not be None')
            self.mk_warning_popup()
        else:
            validate_inputs(self.Hardness, self.Acidity, self.BOD)
            self.mk_dispense_bar()

    def press(self, *args):
        self.get_inputs(args[0], args[1])

    def execute(self):
        self.check_inputs()

    def mk_dispense_bar(self):        
        self.pb = ProgressBar(max=100)
        self.popup = Popup(
            title="Evacuating Holding Tank!",
            content=self.pb
        )

        self.popup.bind(on_open = self.puopen)
        self.popup.open()

    def next(self, dt):
        if self.pb.value >= 100:
            self.clear_button_state()
            self.pb.value = 0

            self.popup.dismiss()
        else:
            self.pb.value += 1

    def puopen(self, instance):
        Clock.schedule_interval(self.next, 1 / 25)

    def mk_warning_popup(self):
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
