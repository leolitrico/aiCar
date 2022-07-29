from queue import Queue
import sys
sys.path.insert(0, '/home/pi/aiCar/vision')
import objectDetection

q = Queue()
objectDetection.producer(q)
