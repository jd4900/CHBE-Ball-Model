import RPi.GPIO as GPIO
from time import sleep


def init_valve(valve):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(valve[0], GPIO.OUT)
    GPIO.setup(valve[1], GPIO.OUT)

    close_valve(valve)


def open_valve(valve):
    GPIO.output(valve[0], GPIO.HIGH)
    GPIO.output(valve[1], GPIO.LOW)

    sleep(5)
    GPIO.output(valve[0], GPIO.LOW)


def close_valve(valve):
    GPIO.output(valve[0], GPIO.LOW)
    GPIO.output(valve[1], GPIO.HIGH)

    sleep(5)
    GPIO.output(valve[1], GPIO.LOW)


if __name__ == "__main__":

    BLUE = [17, 18]
    BLACK = [22, 23]

    while True:
        command = input("Enter a command: ")

        if command == "or":
            open_valve(BLUE)
        elif command == "ol":
            open_valve(BLACK)
        elif command == "cr":
            close_valve(BLUE)
        elif command == "cl":
            close_valve(BLACK)

        continue
