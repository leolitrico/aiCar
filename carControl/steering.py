from enum import Enum
import RPi.GPIO as GPIO


class Steering(Enum):
    STRAIGHT = 0
    LEFT = 1
    RIGHT = 2


def setup():
    GPIO.setup(6, GPIO.OUT)  # M3
    GPIO.setup(13, GPIO.OUT)  # M4
    GPIO.setup(12, GPIO.OUT)  # PWMB
    GPIO.output(6, 0)
    GPIO.output(13, 0)
    GPIO.output(12, 1)  # output enable


def steer(steer):
    if steer == Steering.STRAIGHT:
        GPIO.output(6, 0)
        GPIO.output(13, 0)
    elif steer == Steering.RIGHT:
        GPIO.output(6, 1)
        GPIO.output(13, 0)
    else:
        GPIO.output(6, 0)
        GPIO.output(13, 1)
