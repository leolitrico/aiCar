from locale import MON_1
import RPi.GPIO as GPIO

m1 = None
m2 = None


def setup():
    global m1
    global m2
    GPIO.setup(20, GPIO.OUT)  # M1
    GPIO.setup(21, GPIO.OUT)  # M2
    m1 = GPIO.PWM(20, 100)
    m2 = GPIO.PWM(21, 100)

    GPIO.setup(26, GPIO.OUT)  # PWMA
    GPIO.output(26, 1)  # output enable


def run(frequency):
    hi = 0
