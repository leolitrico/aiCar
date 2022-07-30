import socket
import struct
import cv2
import pickle

host = ''
port = 5007

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(10)
print("listenening...")

connection, address = sock.accept()
print("connection established")

packetSize = struct.calcsize(">L")
data = b""

while True:
    #retrieve the entire packet
    while len(data) < packetSize:
        data += connection.recv(4096)

    packedMsgSize = data[:packetSize]
    data = data[packetSize:]
    msgSize = struct.unpack(">L", packedMsgSize)[0]

    while len(data) < msgSize:
        data += connection.recv(4096)
        
    frameData = data[:msgSize]
    data = data[msgSize:]

    frame = pickle.loads(frameData, fix_imports = True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    cv2.imshow('pi object detector',frame)
    cv2.waitKey(1)

