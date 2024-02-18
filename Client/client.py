import pygame
import sys
import socket 
import time
import numpy as np

# IP Address and port on Raspberry Pi
HOST = "192.168.1.11"
PORT = 5000

DEADZONE = 0.01

# Column 1: Motor 1 - facing back on the right
# Column 2: Motor 2 - facing back on the left
# Column 3: Motor 3 - facing down in the center

# Row 1: X vector (forwards and back)
# Row 2: Y vector (left and right)
# Row 3: Z vector (up and down)

# Row 4: X rotation (roll)
# Row 5: Y rotation (pitch)
# Row 6: Z rotatioon (yaw)

PROPORTIONAL_MATRIX =  [[1, 1, 0],
                        [0, 0, 0],
                        [0, 0, 1],
                        [0, 0, 0],
                        [0, 0, 0],
                        [1, -1, 0]]

# Pre-process the joystick input to apply a deadzone, as well as determine the direction
def preProcessJoystick(axis):
    # Find the sign of the input value, if the value is negative the sign bit is set
    sign = 0
    if axis < 0:
        sign = 1

    # Cube the analog axis value, this should allow for better fine motor control
    axis = axis**3

    # Take the absolute value of the axis, this finishes the conversion into sign magnitude notation
    axis = abs(axis)

    # Apply deadzone
    if axis < DEADZONE:
        axis = 0

    return sign, axis

# Pre-process trigger to apply a deadzone, as well as map from range [-1,1] to range [0,1]
def preProcessTrigger(axis):
    axis = axis + 1
    axis = axis / 2

    # Apply deadzone
    if axis < DEADZONE:
        axis = 0
    
    return axis

# Take the input from the controller and output throttle and sign for each motor
# LeftY controls forward/backward movement
# LeftX controls yaw
# RightY controls up/down movement
def pufferfishControl(LeftYSign, LeftY, LeftXSign, LeftX, RightYSign, RightY):
    # Declaring the numpy array that will be used for the thrust vectors applied to the motors
    thrustMatrix = np.array([0, 0, 0])

    # Using list comprehension, multiply selected rows in the proportional matrix by the controller input and sum the vectors togethor
    thrustMatrix = thrustMatrix + [x * LeftY * LeftYSign for x in PROPORTIONAL_MATRIX[0]]       # Forward/backwards
    thrustMatrix = thrustMatrix + [x * LeftX * LeftXSign for x in PROPORTIONAL_MATRIX[5]]       # Yaw
    thrustMatrix = thrustMatrix + [x * RightY * RightYSign for x in PROPORTIONAL_MATRIX[2]]     # Up/down

    # Normalize the vector
    thrustMatrix = thrustMatrix / np.linalg.norm(thrustMatrix)

    # Declare the arrays for extracting the sign and value
    signArray = []
    valueArray = []

    # Pull the sign out from the matrix to make the sign array for the motor controller
    # The logic for this might need to be flipped
    for elem in thrustMatrix:
        if elem >= 0:
            signArray.append(0)
        else:
            signArray.append(1)

    # Take the absolute value of each element to make the value array for the motor controller
    for elem in thrustMatrix:
        valueArray.append(abs(elem))

    # Pad the arrays with 0 if there are fewer than 8 motors
    signArray = np.pad(signArray, (0, 8 - len(signArray)), constant_values = 0)
    valueArray = np.pad(valueArray, (0, 8 - len(valueArray)), constant_values = 0)

    # Concatenate the sign and value arrays into a string for transmission
    sendString = ','.join([str(elem) for elem in (signArray + valueArray)])
    return sendString


# Create a socket and connect to the Raspberry Pi
clientSocket = socket.socket()
clientSocket.connect((HOST, PORT))

# Initialize pygame and the joysticks array
pygame.init()
pygame.joystick.init()
joysticks = []

# Main loop
run = True
while run:
    # Initialize the string that will be sent to the Raspberry Pi
    sendString = None

    # Add joysticks
    for event in pygame.event.get():
        if event.type == pygame.JOYDEVICEADDED:
            print(event)
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks.append(joy)
        if event.type == pygame.QUIT:
            run = False    

    # For each available joystick (controller)
    for joystick in joysticks:
        # Read input from controller
        LeftXSign, LeftX = preProcessJoystick(joystick.get_axis(0))
        LeftYSign, LeftY = preProcessJoystick(joystick.get_axis(1))
        RightXSign, RightX = preProcessJoystick(joystick.get_axis(2))
        RightYSign, RightY = preProcessJoystick(joystick.get_axis(3))
        LeftTrigger = preProcessTrigger(joystick.get_axis(4))
        RightTrigger = preProcessTrigger(joystick.get_axis(5))

        # Create arrays for each of the inputs
        # signArray = [LeftXSign, LeftYSign, RightXSign, RightYSign, 1, 1]
        # valueArray = [LeftX, LeftY, RightX, RightY, LeftTrigger, RightTrigger]

        # Process the inputs for proportional control
        sendstring = pufferfishControl(LeftYSign, LeftY, LeftXSign, LeftX, RightYSign, RightY)

    # Make sure the string is not null, this can happen on startup
    if sendString:
        clientSocket.sendall(sendString.encode())

    # Sleep for a bit to not overwhelm Raspberry Pi
    time.sleep(.1)