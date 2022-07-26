from queue import Queue
from threading import Thread
import carThread
import vision.vision as vision

threadQueue = Queue()
t1 = Thread(target = carThread.consumer, args = (threadQueue, ))
t2 = Thread(target = vision.producer, args = (threadQueue, ))
t1.start()
t2.start()

