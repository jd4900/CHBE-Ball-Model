from kivy.app import App
from kivy.uix.widget import Widget

class BallModelUI(Widget):
    pass

class BallModelApp(App):
    def build(self):
        return BallModelUI()

if __name__ == '__main__':
    BallModelApp().run()