import objectDetection
import setup
from queue import Queue
from threading import Thread
import carThread
import sys
sys.path.insert(0, '/home/pi/aiCar/carControl')
sys.path.insert(0, '/home/pi/aiCar/vision')

threadQueue = Queue()
setup.setup()
t1 = Thread(target=carThread.consumer, args=(threadQueue, ))
t2 = Thread(target=objectDetection.producer, args=(threadQueue, ))
t1.start()
t2.start()
