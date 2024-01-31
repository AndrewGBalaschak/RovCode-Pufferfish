import socket
import time
import os 
from adafruit_servokit import ServoKit

#Constants
nbPCAServo=16 
#Parameters
MIN_IMP  =[500, 500, 500, 500, 500, 500, 500, 500, 00, 500, 500, 500, 500, 500, 500, 500]
MAX_IMP  =[2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500]
MIN_ANG  =[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
MAX_ANG  =[180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180]
#Objects
pca = ServoKit(channels=16)
# function init 
def init():
    i = 8
    print("survo inittialized!")
    pca.continuous_servo[i].set_pulse_width_range(MIN_IMP[i] , MAX_IMP[i])

HOST = "192.168.1.11"
PORT = 5000

BUFFER_SIZE = 1024

listenSocket = socket.socket()
listenSocket.bind((HOST, PORT))

listenSocket.listen()
print(f"server is listening on port {HOST}:{PORT}")

serverSocket, clientAdress = listenSocket.accept()

print(f"server accepted connection from {clientAdress}")



def pcaScenario():
    """Scenario to test servo"""
    for i in range(nbPCAServo):
        for j in range(MIN_ANG[i],MAX_ANG[i],1):
            print("Send angle {} to Servo {}".format(j,i))
            pca.continuous_servo[i].angle = j
            time.sleep(0.01)
        for j in range(MAX_ANG[i],MIN_ANG[i],-1):
            print("Send angle {} to Servo {}".format(j,i))
            pca.continuous_servo[i].angle = j
            time.sleep(0.01)
        pca.servo[i].angle=None #disable channel
        time.sleep(0.5)

#setup
init()


while True:
    data = serverSocket.recv(BUFFER_SIZE).decode()
    testArr = data.split(",")
    if (len(testArr) >= 6):
        data = f"LeftX: {testArr[0]}, LeftY: {testArr[1]}, RightX: {testArr[2]}, RightY: {testArr[3]}, leftTrigger: {testArr[4]}, RightTrigger: {testArr[5]}"
    os.system("clear")
    print(data)
    #pcaScenario()
    pca.continuous_servo[8].throttle = float(testArr[0])
    
    