import sys
sys.path.insert(0, '/home/pi/aiCar/carControl')
import motor
import steering
import carSetup
import socket

carSetup.setup()
print("car ready")

host = ''
port = 5007

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(10)
print("listenening...")

connection, address = sock.accept()
print("connection established")

while True:
    #retrieve the entire packet
    data = connection.recv(1024).decode().split(" ")
    direction = data[0]
    forward = data[1]
    throttle = data[2]

    
    #if direction == "right":
        #steering.steer(steering.Steering.RIGHT)
    #elif direction == "left":
        #steering.steer(steering.Steering.LEFT)
    #else:
        #steering.steer(steering.Steering.STRAIGHT)

    #if forward == "forward":
        #motor.run(-1 * int(throttle))
    #elif forward == "none":
        #motor.run(0)
    #else:
        #motor.run(int(throttle))
    
    print(direction + " " + forward + ":" + throttle) 