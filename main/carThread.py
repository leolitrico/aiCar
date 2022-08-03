import sys
sys.path.insert(0, '/home/pi/aiCar/carControl')
import steering
import motor
import keyboard
import carSetup


deltaXTolerance = 130


def consumer(threadQueue):
    noObjectDetectedCountLimit = 1000000 # 1'000'000
    noObjectDetectedCount = noObjectDetectedCountLimit
    #counter = 0 #counter to see delay between objectDetection, and carControl
    
    while True:
        #if object detected, then get data sent and move car accordingly
        if threadQueue.qsize() > 0:
            deltaX, deltaY = threadQueue.get()
            steer = None
            if abs(deltaX) < deltaXTolerance:
                steer = steering.Steering.STRAIGHT
            elif deltaX < 0:
                steer = steering.Steering.LEFT
            else:
                steer = steering.Steering.RIGHT

            #print("CarCounter: " + str(counter))
            counter += 1
            steering.steer(steer)
            motor.run(deltaY)
            
        #if no data is received, then make car neutral (with a delay)
        else:
            if(noObjectDetectedCount < 0):
                noObjectDetectedCount = noObjectDetectedCountLimit
                steering.steer(steering.Steering.STRAIGHT)
                motor.run(0)
            else:
                noObjectDetectedCount-=1



