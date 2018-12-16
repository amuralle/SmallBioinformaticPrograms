#Alex Muralles
#amuralle
#Max-Clique finder

import random
import math
import sys
random.seed()

#We will implement our adjacency matrix as a 2D-list with the following features
#for any vi, a single list will be dedicated to all the adjacencies of vi

#Thus, for example, for any arbitary vi, its section of the adjacency matrix would be represented by:
# A = [[vi1,vi2,vi3,vi4.....vin]] for a graph of length n

#To keep track of our frequencies, we will hash the STRING of the SORTED lists
#This will ensure that any two equal max cliques will be hashed the same

def pickWithProbability(probability):
    x = random.uniform(0,1)
    #we select a random chance
    if (x <= probability): #If that probability is within our threshhold:
        return True
    else:
        return False

def everythingConnects(v,V,matrix):
    for node in V:
        if matrix[node][v] == "0":
            return False
    return True

def energy(V):
    e = -len(V)
    return e

def runSampling(n,k,T,r,matrix):
    T = float(T)
    output = dict()
    degree = n #estabished by Q4 Pt. a
    V = list()
    for i in range(0,k):
        V2 = list(V) #create a copy of V, but not the same list
        T = T * (r ** i)
        v = random.randint(0,n-1) #select a random node
        if v in V:
            V2.remove(v)
        else:
            if everythingConnects(v,V,matrix):
                V2 = V2 + [v]
            else:
                V2 = V2

        if (energy(V2) <= energy(V)):
            V = V2

        elif ((T != 0) and (pickWithProbability(math.exp(-1/T)))):
            V = V2

        V.sort()
        Vstring = str(V)
        if(Vstring in output.keys()):
            output[Vstring] = output[Vstring] + 1
        else:
            output[Vstring] = 1

    for clique in output.keys():
        cliqueValues = clique.strip("[]")
        cliqueValues = cliqueValues.split()
        freq = str(output[clique])
        masterString = ""
        for number in cliqueValues:
            masterString = masterString + " " + "a" + str(number)
        masterString = masterString + ": " + freq
        print(masterString)



def init():
    filename = sys.argv[1]
    inputFile = open(filename,"r")
    lines = inputFile.readlines()
    n = int(lines[0])
    k = int(lines[1])
    T = float(lines[2])
    r = float(lines[3])
    M = []
    for line in lines[4:]:
        line = line.split()
        M.append(line)
    runSampling(n,k,T,r,M)


init()
