import objectDetection
from queue import Queue
import sys
sys.path.insert(0, '/home/pi/aiCar/vision')

q = Queue()
objectDetection.producer(q)
