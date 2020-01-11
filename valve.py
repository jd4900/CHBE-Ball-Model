import RPi.GPIO as GPIO
from time import sleep


def init_valve():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(17, GPIO.OUT)


def open_valve():
    GPIO.output(18, GPIO.LOW)
    GPIO.output(17, GPIO.HIGH)

    sleep(5)


def close_valve():
    GPIO.output(18, GPIO.HIGH)
    GPIO.output(17, GPIO.LOW)

    sleep(5)


if __name__ == "__main__":
    init_valve()
    open_valve()
    close_valve()
