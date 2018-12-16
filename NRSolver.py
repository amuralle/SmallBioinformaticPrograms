#Alex Muralles
#amuralle
#Newton-Raphson Solver

import sys

#We will implement the Newton-Raphson solver with the following implementations of elements:
#Matricies (M) will in this case be 2 x 2 2D lists where M[0][0] = a, M[1][0] = b, etc.
#Vectors (v) will be lists of length 2 where the top is v[0]
#our list of c coefficents will be of length 10 with ci = c[i]

#Our input is a text file with the following format:
#Line 1: #Tab delimited file with 10 values c0 - c9
#Line 2: #n
#Line 3: #x0 y0 (either seperated by tabs or whitespace)

def inverseMatrix(M):
  #We will assume our implementation is a 2D list, where M[0][0] = a, M[1][0] = b, etc.
  assert(len(M) == 2)
  assert(len(M[0]) == 2)
  assert(len(M[1]) == 2)
  a = M[0][0]
  b = M[1][0]
  c = M[0][1]
  d = M[1][1]
  if(((a*d) - (b*c)) == 0):
      print("Warning, matrix inverse cannot be calculated, divide by 0")
      exit()
  q = (a*d) - (b*c)
  q = 1/q
  a2 = d * q
  b2 = (b * -1) * q
  c2 = (c * -1) * q
  d2 = a * q
  M[0][0] = a2
  M[1][0] = b2
  M[0][1] = c2
  M[1][1] = d2
  return M

def vectorSubtract(v1, v2):
    assert(len(v1) == 2)
    assert(len(v2) == 2)
    x = v1[0] - v2[0]
    y = v1[1] - v2[1]
    return [x,y]

def vectorMultiply(M,v):
    #We will assume our implementation is a 2D list, where M[0][0] = a, M[1][0] = b, etc.
    #We will also assume our vector is a list of length 2 [x,y]
    assert(len(M) == 2)
    assert(len(M[0]) == 2)
    assert(len(M[1]) == 2)
    assert(len(v) == 2)
    a = M[0][0]
    b = M[1][0]
    c = M[0][1]
    d = M[1][1]
    ab = v[0] * (a + b)
    cd = v[1] * (c + d)
    return [ab, cd]

def computeValue(x,y,c):
    #f(x,y) =c0+c1x+c2y+c3x2+c4y2  +
    #         c5xy+c6x3+c7y3+c8x2y+c9xy2
    #broken into halves for neatness
    a1 = (c[0]) + (c[1] * x) + (c[2] * y) + (c[3] * (x ** 2)) + (c[4] * (y ** 2))
    a2 = (c[5] * x * y) + (c[6] * (x ** 3)) + (c[7]* (y ** 3)) + (c[8] * (x ** 2) * (y)) + (c[9] * (x) * (y ** 2))
    return (a1 + a2)

def computeGradient(x,y,c):
    #F = [c1 + 2c3x + c5y + 3c6x2 + 2c8xy + c9y2,
    #     c2 + 2c4y + c5x + 3c7y2 + c8x2 + 2c9xy]
    x1 = c[1] + (2 * c[3] * x) + (c[5] * y) + (3 * c[6] * (x ** 2)) + (2 * c[8] * x * y) + (c[9] * (y ** 2))
    y1 = c[2] + (2 * c[4] * y) + (c[5] * x) + (3 * c[7] * (y ** 2)) + (2 * c[8] * (x ** 2)) + (c[9] * x * y)
    return [x1,y1]

def computeHessian(x,y,c):
    #M = [a b]
    #    [c d]
    #H = [2c3 + 6c6x + 2c8y,  c5 + 2c8x + 2c9y]
    #   [c5 + 2c8x + 2c9y,   2c4 + 6c7y + 2c9x]
    a = (2 * c[3]) + (6 * c[6] * x) + (2 * c[8] * y)
    b = c[5] + (2 * c[8] * x) + (2 * c[9] * y)
    c2 = b
    d = (2 * c[4]) + (6 * c[7] * y) + (2 * c[9] * x)
    M = [[0,0],[0,0]]
    M[0][0] = a
    M[1][0] = b
    M[0][1] = c2
    M[1][1] = d
    return M


def solver(x0,y0,c,n):
    for i in range(0,n):
        gradient = computeGradient(x0,y0,c)
        hessian = computeHessian(x0,y0,c)
        v0 = (x0,y0)
        inverseHessian = inverseMatrix(hessian)
        v1 = vectorSubtract(v0,vectorMultiply(inverseHessian,gradient))
        v0 = v1
        x0 = v0[0]
        y0 = v0[1]
    print(("x" + str(n) + ": "))
    print((str(x0)))
    print(("y" + str(n) + ":"))
    print((str(y0)))
    print("f(x,y) = ")
    print(str(computeValue(x0,y0,c)))
    print("(returning values for good style, please ignore repeats if they appear)")
    return (x0,y0,computeValue(x0,y0,c))

def init():
    filename = sys.argv[1]
    inputFile = open(filename,"r")
    lines = inputFile.readlines()
    cString = lines[0]
    nString = lines[1]
    n = int(nString)
    xyString = lines[2]
    cString = cString.split()
    c = [0] * 10
    for i in range(0,len(cString)):
        c[i] = int(cString[i])
    xyString = xyString.split()
    x = float(xyString[0])
    y = float(xyString[1])
    solver(x,y,c,n)


init()
