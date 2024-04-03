import pygame
import sys
import os
import socket 
import time
import numpy as np

# IP Address and port on Raspberry Pi
HOST = "192.168.1.11"
PORT = 5000


def testAllMotors():
    # Loop over the first 64 integers
    for i in range(64):
        thrustMatrix = []
        signArray = []
        valueArray = []

        # Convert integer to binary and remove the '0b' prefix
        binary_string = bin(i)[2:]

        # Pad the binary string with leading zeros to make it 6 digits long
        binary_string_padded = binary_string.zfill(6)

        # Split binary string into individual digits and convert each to an integer
        # thrustMatrix = [int(bit) for bit in binary_string_padded]
        thrustMatrix = [1 if bit == '1' else -1 for bit in binary_string_padded]

        # Pull the sign out from the matrix to make the sign array for the motor controller
        for elem in thrustMatrix:
            if elem < 0:
                signArray.append(1)
            else:
                signArray.append(0)

        # Take the absolute value of each element to make the value array for the motor controller
        for elem in thrustMatrix:
            valueArray.append(abs(elem))

        # Pad the arrays with 0 if there are fewer than 8 motors
        signArray = np.pad(signArray, (0, 8 - len(signArray)), constant_values = 0)
        valueArray = np.pad(valueArray, (0, 8 - len(valueArray)), constant_values = 0)

        # Concatenate the sign and value arrays into a string for transmission
        sendString = ','.join([str(elem) for elem in (signArray.tolist() + valueArray.tolist())])
        clientSocket.sendall(sendString.encode())

        # Print the values to the screen
        os.system("clear")
        print(valueArray)
        time.sleep(1)


# Create a socket and connect to the Raspberry Pi
clientSocket = socket.socket()
clientSocket.connect((HOST, PORT))

testAllMotors()