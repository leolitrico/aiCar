import socket
import struct
import cv2
import pickle

host = ''
port = 3456

sock = socket()
sock.bind((host, port))
sock.listen(10)

connection, address = sock.accept()

packet_size = struct.calcsize(">L")
data = b""

while True:
    while len(data) < packet_size:
        data += connection.recv(4096)
    packed_msg_size = data[:packet_size]
    data = data[packet_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: {}".format(msg_size))
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    cv2.imshow('ImageWindow',frame)
    cv2.waitKey(1)

