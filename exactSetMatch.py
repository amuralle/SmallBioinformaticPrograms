#exactSetMatch.py
#Alex Muralles
#03-512
#September 20th, 2018

import sys


def hashSeq(Kmer):
    hash = 0
    for char in Kmer:
        hash = hash << 2
        if char == 'C':
            hash = hash + 0
        if char == 'G':
            hash = hash + 1
        if char == 'A':
            hash = hash + 2
        if char == 'T':
            hash = hash + 3
    return hash

def CreateKmerTable(S, k):
    T = [None] * ((4**k)-1)
    for i in range(0,len(S)):
        Kmer = S[i:i+k]
        n = hashSeq(Kmer) % len(T)
        if T[n] == None:
            T[n] = [i]
        else:
            T[n] = T[n] + [i]
    return T

def LookupKmer(T, i):
    n = hashSeq(i) % len(T)
    return T[n]

def TestSequenceMatch(S,j,t):
    for char in t:
        if S[j] != char:
            return False
        j = j + 1
    return True

def ExactSetMatch(k,G,R,n):
    T = CreateKmerTable(G,k)
    output = [[]] * n
    i = 0
    for i in range(0,n):
        restrictionSeq = R[i]
        #Using the assumption that len(rx) > k from the homework
        Kmer = restrictionSeq[0:k]
        r = restrictionSeq[k:]
        if LookupKmer(T,Kmer) != None:
            matches = LookupKmer(T,Kmer)
            for start in matches:
                if TestSequenceMatch(G,start+k,r):
                    output[i] = output[i] + [start]
    #print the specified outfit
    for seqi in range(0,n):
        theList = output[seqi]
        for location in theList:
            print(R[seqi] + ": " + str(location))

def init():
    filename = sys.argv[1]
    inputFile = open(filename,"r")
    lines = inputFile.readlines()
    kmerLength = int(lines[0])
    n = int(lines[1])
    G = lines[2]
    R = []
    for singleLine in range(3,3+n):
        R = R + [lines[singleLine].strip()]
    ExactSetMatch(kmerLength,G,R,n)


init()
