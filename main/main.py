from queue import Queue
from threading import Thread
import carThread
import carControl.carSetup as setup
import vision.objectDetection as objectDetection

threadQueue = Queue()
setup.setup()
t1 = Thread(target=carThread.consumer, args=(threadQueue, ))
t2 = Thread(target=objectDetection.producer, args=(threadQueue, ))
t1.start()
t2.start()
