#Alex Muralles
#Amuralle
#Problem Set 4

import sys
import math
import numpy as np
#for the following functions:
    #np.random.poisson
    #np.random.normal
    #np.random.exponential
from scipy import stats
#for the following functions:
    #stats.pearsonr
from scipy import misc
    #for choose function

#We will implement our coalesence tree as a generic tree with the following features:
#1. Each Node in our tree will have a set of mutations and a physical distance
#2. Each Node will also have a parent
#3. A coalesence will yeild two nodes with the same parent

#We will utilize object-oriented programming to accomplish this

#Our program will have the following steps:
#1. Generate a coalesence tree with k nodes to begin
#2. Add in mutations in accordance with time
#

#The tree class will contain all data for any given node
class node(object):
    def __init__(self,mutations=[],location=[0,0,0],t=-1,child=[]):
        self.mutations = mutations #Mutations of the node, calculated after generation
        self.location = location #Location of the node, calculated after generation
        self.child = child #Child of the current node
        self.time = t #Time passed from current node to the previous

def calculatePhysDistance(nodei,nodej):
    x1,y1,z1 = nodei.location
    x2,y2,z2 = nodej.location
    x = (x1-x2)**2
    y = (y1-y2)**2
    z = (z1-z2)**2
    return (x + y + z)

def aboutEqual(x,y):
    if (abs(x-y)) < (10**-6):
        return True
    else:
        return False

def calculateGeneticDistance(nodei,nodej):
    a = set(nodei.mutations)
    b = set(nodej.mutations)
    a = a.union(b)
    a = list(a)
    toRemove = []
    for i in range(len(a)):
        q = a[i]
        for j in a[i+1:]:
            if aboutEqual(q,j):
                toRemove.append(q)

    for r in toRemove:
        if r in a:
            a.remove(r)

    return len(a)

def generateTree(k):
    a = [] #a is our list of current-generation nodes, which we will update regularly
    for i in range(k):
        a.append(node())
    finalGen = list(a) #We only want to deal with the final generation, so we must
    #keep track of it by keeping the individual pointers to the objects
    #in a list we can output. Note that this is NOT a deep copy, so that once
    #we modify this object (input location data, etc) we can still access
    #that data
    step = 0
    while len(a) > 1:
        step = step + 1
        ti = np.random.exponential((1/misc.comb(len(a),2)))
        firstNode = -1
        secondNode = -1
        while (firstNode == secondNode):
            firstNode = np.random.randint(0,len(a))
            secondNode = np.random.randint(0,len(a))
        nodes = a
        node1 = nodes[firstNode]
        node2 = nodes[secondNode]
        nodes.remove(node1)
        nodes.remove(node2)
        #Thus, the length of nodes is len(a)-2
        b = []
        w = 0
        for j in range(len(nodes)):
            newNode = node()
            oldNode = nodes[j]
            newNode.child = [oldNode]
            newNode.time = ti
            b.append(newNode)
        ancestor = node()
        ancestor.time = ti
        ancestor.child = [node1,node2]
        b.append(ancestor)
        a = b
    assert(len(a) == 1)
    return a[0], finalGen

def generateData(root,u,varience):
    t = root.time
    rootLocationC = list(root.location)
    for child in root.child:
        child.location = list(root.location)
        #Calculate location
        deltaX = np.random.normal(0,((varience**2) * t))
        deltaY = np.random.normal(0,((varience**2) * t))
        deltaZ = np.random.normal(0,((varience**2) * t))
        child.location[0] = child.location[0] + deltaX
        child.location[1] = child.location[1] + deltaY
        child.location[2] = child.location[2] + deltaZ
        #Calculate genetic Distance
        child.mutations = list(root.mutations)
        numberOfMutations = np.random.poisson((t * u))
        numberOfMutations = int(numberOfMutations)
        for i in range(numberOfMutations):
            child.mutations.append(np.random.uniform())
        generateData(child,u,varience)

def calculateC(list1, list2,k):
    #To calculate C, we are going to use a package, but we have to handle
    #for cases in which the denominator is equal to 0 (which occured in test cases)
    #Using Lside and Rside to denote left and right sides of the provided formula
    n = (k*(k-1))/2.00
    sum1 = sum(list1)
    sum1 = sum1**2
    list1Squared = []
    for i in list1:
        list1Squared.append(i**2)
    squaredSum1 = sum(list1Squared)

    if(((n * squaredSum1) - sum1) == 0):
        return 0.00

    sum2 = sum(list2)
    sum2 = sum2**2
    list2Squared = []
    for i in list2:
        list2Squared.append(i**2)
    squaredSum2 = sum(list2Squared)

    if(((n * squaredSum2) - sum2) == 0):
        return 0.00

    return stats.pearsonr(list1,list2)[0]

def runTrials(k,u,v,r):
    Clist = []
    for trial in range(r):
        root,finalGen = generateTree(k)
        generateData(root,u,v)
        #We have all our data, now to calculate C for this trial
        #we must first gather a list of all our distances
        geneticDistance = []
        physicalDistance = []
        for i in range(len(finalGen)):
            currentNode = finalGen[i]
            for j in range(i+1,len(finalGen)):
                nextNode = finalGen[j]
                geneticDistance.append(calculateGeneticDistance(currentNode,nextNode))
                physicalDistance.append(calculatePhysDistance(currentNode,nextNode))
        c = calculateC(geneticDistance,physicalDistance,k)
        Clist.append(c)
    print("For " + str(r)+ " trials:")
    print("Mean: " + str(np.mean(Clist)))
    print("Standard Deviation: " + str(np.std(Clist)))

def init():
    filename = sys.argv[1]
    inputFile = open(filename,"r")
    lines = inputFile.readlines()
    k = int(lines[0])
    u = float(lines[1])
    v = float(lines[2])
    r = int(lines[3])
    runTrials(k,u,v,r)

init()
