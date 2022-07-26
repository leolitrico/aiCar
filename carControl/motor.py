import RPi.GPIO as GPIO

def consumer(threadQueue):
    if len(threadQueue) > 0:
        data = threadQueue.get()