import carControl.motor as motor
import carControl.steering as steering
deltaXTolerance = 20
areaFactor = 1


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
