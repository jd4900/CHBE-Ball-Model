import RPi.GPIO as GPIO
from time import sleep


def init_valve(valve):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(valve[0], GPIO.OUT)
    GPIO.setup(valve[1], GPIO.OUT)

    close_valve()


def open_valve(valve):
    GPIO.output(valve[0], GPIO.HIGH)
    GPIO.output(valve[1], GPIO.LOW)


def close_valve(valve):
    GPIO.output(valve[0], GPIO.LOW)
    GPIO.output(valve[1], GPIO.HIGH)


if __name__ == "__main__":
    init_valve([22, 23])
    init_valve([22, 23])

    open_valve([22, 23])

    sleep(10)

    close_valve([22, 23])
