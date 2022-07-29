from queue import Queue
import sys

sys.path.insert(0, '/home/pi/aiCar/vision')
import objectDetection
import imageClassification

q = Queue()
objectDetection.producer(q, imageClassification.getInterpreter())
