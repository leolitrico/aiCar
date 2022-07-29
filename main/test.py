import vision.objectDetection as t
from queue import Queue

q = Queue()
t.producer(q)
