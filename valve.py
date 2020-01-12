import RPi.GPIO as GPIO
from time import sleep

GPIO_PIN_17 = 17
GPIO_PIN_18 = 18


def init_valve():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_PIN_17, GPIO.OUT)
    GPIO.setup(GPIO_PIN_18, GPIO.OUT)

    close_valve()


def open_valve():
    GPIO.output(GPIO_PIN_17, GPIO.HIGH)
    GPIO.output(GPIO_PIN_18, GPIO.LOW)


def close_valve():
    GPIO.output(GPIO_PIN_17, GPIO.LOW)
    GPIO.output(GPIO_PIN_18, GPIO.HIGH)


if __name__ == "__main__":
    init_valve()

    open_valve()

    sleep(10)

    close_valve()
