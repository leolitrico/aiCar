from locale import MON_1
import RPi.GPIO as GPIO

m1 = None
m2 = None
deltaYTolerance = 30
maxDeltaY = 300


def setup():
    global m1
    global m2
    GPIO.setup(20, GPIO.OUT)  # M1
    GPIO.setup(21, GPIO.OUT)  # M2
    m1 = GPIO.PWM(20, 100)
    m2 = GPIO.PWM(21, 100)
    m1.start(0)
    m2.start(0)

    GPIO.setup(26, GPIO.OUT)  # PWMA
    GPIO.output(26, 1)  # output enable

def end():
    m1.ChangeDutyCycle(0)
    m2.ChangeDutyCycle(0)
    GPIO.output(26, 0)


def run(deltaY):
    absoluteY = abs(deltaY)
    if absoluteY < deltaYTolerance:
        m1.ChangeDutyCycle(0)
        m2.ChangeDutyCycle(0)
    else:
        dutyCycle = min(100, absoluteY / maxDeltaY * 100)
        if deltaY < 0:
            # go forward
            m1.ChangeDutyCycle(dutyCycle)
            m2.ChangeDutyCycle(0)
        else:
            # go backwards
            m1.ChangeDutyCycle(0)
            m2.ChangeDutyCycle(dutyCycle)
