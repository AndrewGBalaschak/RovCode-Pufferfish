import numpy as np

M =  np.array(  [[1, 1, 0],
                [0, 0, 1],
                [-1, 1, 0]])

# Returns a matrix normalized so the maximum value in the matrix is 1
def normalizeMatrix(ary):
    max = 1
    
    # Get maximum magnitude in matrix
    for elem in ary:
        if abs(elem) > max:
            max = abs(elem)
    
    # Divide each element by the max value
    return [x / max for x in ary]


def pufferfishControl(LeftX, LeftY, RightY):
    # Calculate the transpose of M, only needed when DoF != num motors
    # MT = np.transpose(M)
    # print("MT: ", MT)

    # Calculate M5 = MT * M
    # M5 = np.matmul(MT, M)
    # print("\nM5: ", M5)

    # Define pilot inputs (assuming)
    # pilot_inputs = np.array([LeftY, RightY, LeftX])
    pilot_inputs = np.array([   [LeftY, 0, 0],
                                [0, RightY, 0],
                                [0, 0, LeftX]])

    # Calculate Pilot Equivalent (PE5)
    PE5 = np.matmul(np.matmul(np.abs(M), np.array([1,1,1])), pilot_inputs)
    print("\nPE5: ", PE5)

    # Solve for R5 using M5 * R5 = PE5
    R5 = np.linalg.solve(M, PE5)
    print("\nR5: ", R5)

    # Map R5 to thrusters (R6 = MT * R5)
    # R6 = np.dot(MT, R5)

    # Normalize R6
    R5_normalized = normalizeMatrix(R5)

    print("Resulting thruster values (unnormalized):", R5)
    print("Resulting thruster values (normalized):", R5_normalized)

LeftX = -1
LeftY = 0.5
RightY = 0

pufferfishControl(LeftX, LeftY, RightY)