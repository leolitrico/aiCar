import sys
sys.path.insert(0, '/home/pi/aiCar/carControl')
import steering
import motor


deltaXTolerance = 20


def consumer(threadQueue):
    while True:
        if len(threadQueue) > 0:
            deltaX, deltaY = threadQueue.get()
            steer = None
            if abs(deltaX) < 20:
                steer = steering.Steering.STRAIGHT
            elif deltaX < 0:
                steer = steering.Steering.LEFT
            else:
                steer = steering.Steering.RIGHT

            steering.steer(steer)
            motor.run(deltaY)
