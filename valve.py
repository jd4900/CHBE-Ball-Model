from time import sleep
import logging

try:
    import RPi.GPIO as GPIO

    def init_valve(valve):
        logging.info("Valve: Initing %s valve!", valve)

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(valve[0], GPIO.OUT)
        GPIO.setup(valve[1], GPIO.OUT)

        close_valve(valve)

    def open_valve(valve):
        logging.info("Valve: Opening %s valve!", valve)

        GPIO.output(valve[0], GPIO.HIGH)
        GPIO.output(valve[1], GPIO.LOW)

        sleep(5)
        GPIO.output(valve[0], GPIO.LOW)

    def close_valve(valve):
        logging.info("Valve: Closing %s valve!", valve)

        GPIO.output(valve[0], GPIO.LOW)
        GPIO.output(valve[1], GPIO.HIGH)

        sleep(5)
        GPIO.output(valve[1], GPIO.LOW)

except ModuleNotFoundError:
    logging.warning("Valve: Could not import GPIO")

    def init_valve(valve=None):
        logging.info("Valve: Initing %s valve!", valve)

    def open_valve(valve=None):
        logging.info("Valve: Opening %s valve!", valve)

    def close_valve(valve=None):
        logging.info("Valve: Closing %s valve!", valve)


if __name__ == "__main__":

    BLUE = [17, 18]
    BLACK = [22, 23]

    init_valve(BLUE)
    init_valve(BLACK)

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
