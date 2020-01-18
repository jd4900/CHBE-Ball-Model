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

from valve import init_valve, open_valve, close_valve

# Configure App
Config.set('graphics', 'resizable', True)
Config.set('kivy', 'window_icon', 'assets/icon.png')

# Color Constants for Pop-ups
WARNING_RED = [255/255, 51/255, 51/255, 1]
GOOD_GREEN = [30/255, 130/255, 76/255, 1]

# Constants for ProgressBar
MAX_VALUE = 100
LOADING_TIME = 4  # seconds
TIMEOUT = LOADING_TIME / MAX_VALUE

# Valve Constants
GPIO_PIN_17 = 17
GPIO_PIN_18 = 18
BLACK_VALVE = [GPIO_PIN_17, GPIO_PIN_18]

GPIO_PIN_22 = 22
GPIO_PIN_23 = 23
BLUE_VALVE = [GPIO_PIN_22, GPIO_PIN_23]

init_valve(BLUE_VALVE)
init_valve(BLACK_VALVE)


def validate_inputs(Hardness, Acidity, BOD):
    # Helper Function for deciding which valve will open
    if Hardness == '10 ppm' and Acidity == '7' and BOD == 'Low':
        return True
    else:
        return False


class BallModelUI(Widget):

    Hardness = None
    Acidity = None
    BOD = None

    def get_inputs(self, button, state):
        # Ensures that App variables are clear if state is not down
        # and sets App variable to selected button when pressed
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
        # Clear all states when `Execute` is pressed
        self.ids.button1.state = "normal"
        self.ids.button2.state = "normal"
        self.ids.button3.state = "normal"
        self.ids.button4.state = "normal"
        self.ids.button5.state = "normal"
        self.ids.button6.state = "normal"
        self.ids.button7.state = "normal"
        self.ids.button8.state = "normal"
        self.ids.button9.state = "normal"

        Logger.info("APP: Button state cleared")

    def check_inputs(self):
        # Ensures App has value for Hardness, Acidity, and BOD when Execute is pressed
        if any(item is None for item in [self.Hardness, self.Acidity, self.BOD]):
            Logger.warning('APP: Input should not be None')
            self.mk_warning_popup()
        else:
            is_correct = validate_inputs(self.Hardness, self.Acidity, self.BOD)
            self.mk_dispense_bar(is_correct)
            # TODO: Add code for opening and closing valve here

            open_valve(BLACK_VALVE)

            if is_correct:
                open_valve(BLUE_VALVE)

            Logger.info('APP: Valve is opening')

    def press(self, *args):
        # Wrapper Function for get_inputs. FIXME: Really not doing much and should be removed
        self.get_inputs(args[0], args[1])

    def execute(self):
        # Wrapper function for check_inputs. FIXME: Really not doing much and should be removed
        self.check_inputs()

    def mk_dispense_bar(self, is_correct):
        # Makes dispense bar popup depending on if the inputs are correct or not.
        self.pb = ProgressBar(max=MAX_VALUE)
        self.popup = Popup(
            title="WARNING! TOXIC!",
            title_size='56sp',
            size_hint=(None, None), size=(400, 200),
            title_color=WARNING_RED,
            separator_color=WARNING_RED,
            content=self.pb,
            auto_dismiss=False
        )

        if is_correct is True:
            Logger.info('APP: Dispensing good stuff')
            self.popup.title = "Successfully Neutralized!"
            self.popup.title_color = GOOD_GREEN
            self.popup.separator_color = GOOD_GREEN
        else:
            Logger.info('APP: Dispensing bad stuff')

        self.popup.bind(on_open=self.puopen)
        self.popup.open()

    def next(self, dt):
        # Increase the value of the progress bar until it reaches MAX_VALUE.
        # Then clears state, cancels event, and dismisses the popup.
        if self.pb.value >= MAX_VALUE:
            self.clear_button_state()
            self.event.cancel()

            self.popup.dismiss()
            close_valve(BLACK_VALVE)
            close_valve(BLUE_VALVE)

            Logger.warning('APP: Valve is closed')

        else:
            self.pb.value += 1

    def puopen(self, instance):
        self.event = Clock.schedule_interval(self.next, TIMEOUT)

    def mk_warning_popup(self):
        # Makes Warning Popup if input is missing.
        layout = GridLayout(cols=1, padding=10)

        popupLabel = Label(
            text="[color=ff3333][b][size=24]Missing Input![/size][/b][/color]",
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

    def dismiss_popup(self, dt):
        self.dismiss()

    def mk_caution_popup(self):
        # Makes Caution Popup if input is missing.
        layout = GridLayout(cols=1, padding=10)

        popupLabel = Label(
            text="[color=ff3333][b][size=32]WARNING! TOXIC! [/size][/b][/color]",
            markup=True,
        )

        layout.add_widget(popupLabel)

        popup = Popup(
            title="WARNING!",
            title_size='32sp',
            content=layout,
            size_hint=(None, None), size=(400, 400),
            separator_color=WARNING_RED,
            title_color=WARNING_RED
        )

        popup.open()

        Clock.schedule_once(self.dismiss_popup, 5)


class BallModelApp(App):
    def build(self):
        self.title = "Ball Model"
        return BallModelUI()


if __name__ == '__main__':
    BallModelApp().run()
