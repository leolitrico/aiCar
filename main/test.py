from queue import Queue
import sys

sys.path.insert(0, '/home/pi/aiCar/vision')
sys.path.insert(0, '/home/pi/aiCar/network')
import objectDetection
import imageClassification
import server

server.setupServer()
q = Queue()
objectDetection.producer(q, imageClassification.getInterpreter())
