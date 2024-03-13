import numpy as np

M = np.array(  [[0.866025, 0, 0.866025, 0.866025, 0, 0.866025],
                [0.5, 0, -0.5, 0.5, 0, -0.5],
                [0, -1, 0, 0, 1, 0],
                [0, -0.3048, 0, 0, -0.1778, 0],
                [-0.29368, 0., 0.293679, 0.293679, 0, -0.29368]])

# Returns a matrix normalized so the maximum value in the matrix is 1
def normalizeMatrix(ary):
    max = 1
    
    # Get maximum magnitude in matrix
    for elem in ary:
        if abs(elem) > max:
            max = abs(elem)
    
    # Divide each element by the max value
    return [x / max for x in ary]

def competitionControl(LeftX, LeftY, RightX, RightY, input5):
    print("\nM:\n", M)

    # Calculate the transpose of M, only needed when DoF != num motors
    MT = np.transpose(M)
    print("\nMT:\n", MT)

    # Calculate M5 = MT * M
    M5 = np.matmul(M, MT)
    print("\nM5:\n", M5)

    # Define pilot inputs (assuming)
    # pilot_inputs = np.array([LeftY, RightY, LeftX])
    pilot_inputs = np.array([   [LeftY, 0, 0, 0, 0],
                                [0, RightY, 0, 0, 0],
                                [0, 0, LeftX, 0, 0],
                                [0, 0, 0, RightX, 0],
                                [0, 0, 0, 0, input5]])

    # Calculate Pilot Equivalent (PE5)
    PE5 = np.matmul(np.sum(np.abs(M), axis=1), pilot_inputs)
    print("\nPE5:\n", PE5)

    # Solve for R5 using M5 * R5 = PE5
    R5 = np.linalg.solve(M5, PE5)
    print("\nR5:\n", R5)

    # Map R5 to thrusters (R6 = MT * R5)
    R6 = np.dot(MT, R5)

    # Normalize R6
    R6_normalized = normalizeMatrix(R6)

    print("Resulting thruster values (unnormalized):", R6)
    print("Resulting thruster values (normalized):", R6_normalized)

LeftX = 0
LeftY = 1
RightX = 0
RightY = 1
input5 = 0

competitionControl(LeftX, LeftY, RightX, RightY, input5)