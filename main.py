from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.logger import Logger

Config.set('graphics', 'resizable', True)

WARNING_RED = [255/255, 51/255, 51/255, 1]
GOOD_GREEN = [30/255, 130/255, 76/255, 1]


def validate_inputs(Hardness, Acidity, BOD):
    if Hardness == '10 ppm' and Acidity == '7' and BOD == 'Low':
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
        if button.group == "Hardness" and state == "down":
            self.Hardness = button.text
        elif button.group == "Acidity" and state == "down":
            self.Acidity = button.text
        elif button.group == "BOD" and state == "down":
            self.BOD = button.text
        elif button.group == "Hardness" and state != "down":
            self.Hardness = None
        elif button.group == "Acidity" and state != "down":
            self.Acidity = None
        elif button.group == "BOD" and state != "down":
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
        if any(item is None for item in [self.Hardness, self.Acidity, self.BOD]):
            Logger.warning('APP: Input should not be None')
            self.mk_warning_popup()
        else:
            is_correct = validate_inputs(self.Hardness, self.Acidity, self.BOD)
            self.mk_dispense_bar(is_correct)

    def press(self, *args):
        self.get_inputs(args[0], args[1])

    def execute(self):
        self.check_inputs()

    def mk_dispense_bar(self, is_correct):
        self.pb = ProgressBar(max=100)
        self.popup = Popup(
            title="Evacuating Holding Tank!",
            title_size='24sp',
            size_hint=(None, None), size=(400, 200),
            title_color=WARNING_RED,
            separator_color=WARNING_RED,
            content=self.pb,
            auto_dismiss=False
        )

        if is_correct is True:
            self.popup.title = "Dispensing Liquid Product!"
            self.popup.title_color = GOOD_GREEN
            self.popup.separator_color = GOOD_GREEN

        self.popup.bind(on_open=self.puopen)
        self.popup.open()

    def next(self, dt):
        if self.pb.value >= 100:
            self.clear_button_state()
            self.event.cancel()

            self.popup.dismiss()
        else:
            self.pb.value += 1

    def puopen(self, instance):
        self.event = Clock.schedule_interval(self.next, 1 / 25)

    def mk_warning_popup(self):
        layout = GridLayout(cols=1, padding=10)

        popupLabel = Label(
            text="[color=ff0000][b][size=24]Missing Input![/size][/b][/color]",
            markup=True,
        )

        closeButton = Button(text="Click to Return")

        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)

        popup = Popup(
            title="Warning!",
            title_size='24sp',
            content=layout,
            size_hint=(None, None), size=(400, 400),
            separator_color=WARNING_RED,
            title_color=WARNING_RED
        )

        popup.open()

        closeButton.bind(on_press=popup.dismiss)


class BallModelApp(App):
    def build(self):
        self.title = "Ball Model"
        return BallModelUI()


if __name__ == '__main__':
    BallModelApp().run()
