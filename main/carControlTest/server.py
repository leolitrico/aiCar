import socket
import cv2
import pickle
import struct
import keyboard

clientIP = '192.168.1.66'
port = 5007

print("server setting up...")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((clientIP, port))
print("server up and connected to client")

direction = "straight"
forward = "none"
throttle = "40"
string = direction + " " + forward + " " + throttle

while True:
    
    if keyboard.is_pressed("up arrow"):
        forward = "forward"
    elif keyboard.is_pressed("down arrow"):
        forward = "backward"
    else:
        forward = "none"
    
    if keyboard.is_pressed("left arrow"):
        direction = "left"
    elif keyboard.is_pressed("right arrow"):
        direction = "right"
    else:
        direction = "straight"

    if keyboard.is_pressed("q"):
        throttle = input("enter throttle (above 20): ")
    
    tempString = direction + " " + forward + " " + throttle 
    if(tempString != string):
        sock.send(tempString.encode())
        string = tempString
        print(string)



