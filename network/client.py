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

packet_size = struct.calcsize(">L")
data = b""

while True:
    while len(data) < packet_size:
        data += connection.recv(4096)

    packed_msg_size = data[:packet_size]
    data = data[packet_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]

    while len(data) < msg_size:
        data += connection.recv(4096)
        
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    cv2.imshow('ImageWindow',frame)
    cv2.waitKey(1)

