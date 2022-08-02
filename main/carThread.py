import sys
sys.path.insert(0, '/home/pi/aiCar/carControl')
import steering
import motor
import keyboard
import carSetup


deltaXTolerance = 20
noObjectDetectedCountLimit = 100000
noObjectDetectedCount = noObjectDetectedCountLimit


def consumer(threadQueue):
    while True:
        #if object detected, then get data sent and move car accordingly
        if threadQueue.qsize() > 0:
            deltaX, deltaY = threadQueue.get()
            steer = None
            if abs(deltaX) < 20:
                steer = steering.Steering.STRAIGHT
            elif deltaX < 0:
                steer = steering.Steering.LEFT
            else:
                steer = steering.Steering.RIGHT

            print("deltaX: " + str(deltaX) + "  deltaY: " + str(deltaY))
            steering.steer(steer)
            motor.run(deltaY)
        #
        else:
            global noObjectDetectedCount
            if(noObjectDetectedCount < 0):
                noObjectDetectedCount = noObjectDetectedCountLimit
                steering.steer(steering.Steering.STRAIGHT)
                motor.run(0)
            else:
                noObjectDetectedCount-=1



