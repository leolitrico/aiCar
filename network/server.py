import socket
import cv2
import pickle
import encoding
import struct
from threading import Thread

clientIP = '192.168.1.63'
port = 5001

def setupSever():
    sock = socket()
    sock.connect((clientIP, port))
    sock.send('connected to pi')
    return sock

def sendImageBis(image, sock):
    result, frame = cv2.imencode('.jpg', image, encoding.encoding)
    data = pickle.dumps(frame, 0)
    size = len(data)

    sock.sendall(struct.pack(">L", size) + data)

def sendImage(image, sock):
    t1 = Thread(target=sendImageBis, args=(image, sock, ))
    t1.start()
