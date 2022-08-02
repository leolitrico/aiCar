import RPi.GPIO as GPIO
import motor
import steering


def setup():
    GPIO.setmode(GPIO.BCM)
    motor.setup()
    steering.setup()

def end():
    motor.end()
    steering.end()
    GPIO.cleanup()
