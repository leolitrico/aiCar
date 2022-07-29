import socket
import cv2
import pickle
import encoding
import struct
from threading import Thread

clientIP = '192.168.1.63'
port = 5007

def setupServer():
    print("server setting up...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((clientIP, port))
    print("server up")
    return sock

def sendImage(image, sock):
    result, frame = cv2.imencode('.jpg', image, encoding.encoding)
    data = pickle.dumps(frame, 0)
    size = len(data)

    sock.sendall(struct.pack(">L", size) + data)
