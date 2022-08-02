import sys
sys.path.insert(0, '/home/pi/aiCar/carControl')
import steering
import motor
import keyboard
import carSetup


deltaXTolerance = 20


def consumer(threadQueue):
    while True:
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

        #if q is pressed then end the locomotion and cleanup GPIOs     
        if keyboard.is_pressed("q"):
            carSetup.end()

