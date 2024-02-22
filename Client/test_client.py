from client import normalizeMatrix, pufferfishControl

# Test 1
# Forward movement
def test1():
    LeftX = 0.0
    LeftY = 0.5
    RightY = 0.0
    expected_output = "0,0,0,0,0,0,0,0,0.5,0.5,0.0,0.0,0.0,0.0,0.0,0.0"
    assert pufferfishControl(LeftX, LeftY, RightY) == expected_output
    
# Test 2
# Backwards movement
def test2():
    LeftX = 0.0
    LeftY = -0.8
    RightY = 0.0
    expected_output = "1,1,0,0,0,0,0,0,0.8,0.8,0.0,0.0,0.0,0.0,0.0,0.0"
    assert pufferfishControl(LeftX, LeftY, RightY) == expected_output

# Test 3
# Up movement
def test3():
    LeftX = 0.0
    LeftY = 0.0
    RightY = 1.0
    expected_output = "0,0,0,0,0,0,0,0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0"
    assert pufferfishControl(LeftX, LeftY, RightY) == expected_output

# Test 4
# Turn left while going forward
def test4():
    LeftX = -0.2
    LeftY = 0.7
    RightY = 0.0
    expected_output = "0,0,0,0,0,0,0,0,0.49999999999999994,0.8999999999999999,0.0,0.0,0.0,0.0,0.0,0.0"
    assert pufferfishControl(LeftX, LeftY, RightY) == expected_output