from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
from kivy.config import Config

Config.set('graphics', 'resizable', True)

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

    def press(self, *args):
        self.get_inputs(args[0])

    def execute(self):
        print(self.Hardness)
        print(self.BOD)
        print(self.Acidity)

class BallModelApp(App):
    def build(self):
        self.title = "Ball Model"
        return BallModelUI()

if __name__ == '__main__':
    BallModelApp().run()
