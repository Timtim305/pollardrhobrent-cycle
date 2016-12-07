import random
import datetime
import sys
import math
import time

###Initialize list of prime numbers
primesListFile = open("primeslistUpTo100k.txt", 'r')
primesList = []
for item in primesListFile.read().strip().replace("[", "").replace("]", "").split(","):
    primesList.append(int(item))


###################################

###List functions
def max(aList):
    ans = -2
    for i in aList:
        if i > ans:
            ans = i
    return ans


def min(aList):
    ans = sys.maxsize
    for i in aList:
        if i < ans:
            ans = i
    return ans


def average(aList):
    sum = 0
    for i in aList:
        sum += i
    return float(sum) / len(aList)


#####################################

###Stuff for the actual algorithm
def f(x, c, n):
    return (x ** 2 + c) % n


def gcd(a, b):
    while b != 0:
        t = b;
        b = a % b
        a = t
    return a


def pollards(n, c):  ##returns factor, count
    if n < 10**12:
        count = 0
        y = random.randint(0, n - 1)
        g, r, q = 1, 1, 1
        nextRadius = 0
        while g == 1:
            x = y
            k = nextRadius
            for i in range(r):
                y = f(y, c, n)
            while (k < r and g == 1):
                ys = y
                for i in range(min([math.floor(math.log(n)), r - k])):
                    y = f(y, c, n)
                    q = q * (abs(x - y)) % n
                    k += 1
                g = gcd(q, n)
                count += 1
            nextRadius = r
            r = r * 2
        if g == n:
            while True:
                ys = f(ys, c, n)

                g = gcd(abs(x - ys), n)
                count += 1
                if g > 1:
                    break
    else:
        count = 0
        y = random.randint(0, n - 1)
        g, r, q = 1, 1, 1
        nextRadius = 0
        while g == 1:
            x = y
            k = nextRadius
            for i in range(r):
                y = f(y, c, n)
            while (k < r and g == 1):
                ys = y
                for i in range(min([math.floor(n ** .25), r - k])):
                    y = f(y, c, n)
                    q = q * (abs(x - y)) % n
                    k += 1
                g = gcd(q, n)
                count += 1
            nextRadius = r
            r = r * 2
        if g == n:
            while True:
                ys = f(ys, c, n)

                g = gcd(abs(x - ys), n)
                count += 1
                if g > 1:
                    break
    return (g, count)


def pollardsBrents(N, c):
    count = 0
    m = random.randint(1, N - 1)
    y = 2
    g, r, q = 1, 1, 1
    while g == 1:
        x = y
        for i in range(r):
            y = f(y, c, N)
        k = 0
        while (k < r and g == 1):
            ys = y
            for i in range(min([m, r - k])):
                y = f(y, c, N)
                q = q * (abs(x - y)) % N
            g = gcd(q, N)
            count += 1
            k = k + m
        r = r * 2
    if g == N:
        while True:
            ys = f(ys, c, N)

            g = gcd(abs(x - ys), N)
            count += 1
            if g > 1:
                break

    return (g, count)


#################################

###Output methods
def outputToConsole(n, c):
    t = pollards(n, c)
    print("Number to Factor: " + str(n) + "\t C:" + str(c) + "\t Factor: " + str(t[0]) + "\t Iterations:" + str(t[1]))


def outputToFile(n, c, f):
    t = pollards(n, c)
    s = (str(n) + "\t" + str(c) + "\t" + str(t[0]) + "\t" + str(t[1]))
    f.write("\n" + s)


def output(n, c, f):
    t = pollards(n, c)
    s = (str(n) + "\t" + str(c) + "\t" + str(t[0]) + "\t" + str(t[1]))
    f.write("\n" + s)
    print("Number to Factor: " + str(n) + "\t C:" + str(c) + "\t Factor: " + str(t[0]) + "\t Iterations:" + str(t[1]))


def getStats(n, outFile,
             outFileRaw):  ##Outputs the avg of 10 trials using c=1 and c=-2 as controls, the min time, and the max time
    ##Order of output is n, c=+1, c=-1, best case, worse case, avg
    ##Raw file is just a list with all 10 numbers tested and all 10 number of iterations
    cList = [1, -1]
    iterationsList = []

    statForOneC = pollards(n, 1)
    iterationsList.append(statForOneC[1])

    statForOneC = pollards(n, -1)
    iterationsList.append(statForOneC[1])

    numbersTested = 0
    while numbersTested < 8:
        c = random.randint(2, n - 2)
        statForOneC = pollards(n, c)
        if (statForOneC[0] != -1):  ##ensures we don't count c values that don't return an answer
            iterationsList.append(statForOneC[1])
            cList.append(c)
            numbersTested += 1

    ##print(iterationsList)
    outputString = str(n) + '\t' + str(iterationsList[0]) + '\t' + str(iterationsList[1]) + '\t' + str(
        min(iterationsList)) + '\t' + str(max(iterationsList)) + '\t' + str(average(iterationsList))
    outFile.write("\n" + outputString)
    outFileRaw.write("\n" + str(n) + '\t' + str(cList) + '\t' + str(iterationsList))
    ##print(outputString)


def getStats2(n, outFile,
              outFileRaw):  ##Outputs the avg of 10 trials using c=1 and c=-2 as controls, the min time, and the max time
    ##Order of output is n, c=+1, c=-1, best case, worse case, avg
    ##Raw file is just a list with all 10 numbers tested and all 10 number of iterations
    cList = [1, -1]
    iterationsList = []

    statForOneC = pollardsBrents(n, 1)
    iterationsList.append(statForOneC[1])

    statForOneC = pollardsBrents(n, -1)
    iterationsList.append(statForOneC[1])

    numbersTested = 0
    while numbersTested < 8:
        c = random.randint(2, n - 2)
        statForOneC = pollardsBrents(n, c)
        if (statForOneC[0] != -1):  ##ensures we don't count c values that don't return an answer
            iterationsList.append(statForOneC[1])
            cList.append(c)
            numbersTested += 1

    ##print(iterationsList)
    outputString = str(n) + '\t' + str(iterationsList[0]) + '\t' + str(iterationsList[1]) + '\t' + str(
        min(iterationsList)) + '\t' + str(max(iterationsList)) + '\t' + str(average(iterationsList))
    outFile.write("\n" + outputString)
    outFileRaw.write("\n" + str(n) + '\t' + str(cList) + '\t' + str(iterationsList))
    ##print(outputString)


######################################

###Main
todaysTime = datetime.datetime.now().strftime("%d %m %y, %H %M")
out = open("FLOYDSAverageCIterationsData" + todaysTime + ".txt", 'a')
outraw = open("FLOYDSRAWAverageCIterationsData" + todaysTime + ".txt", 'a')
out2 = open("BRENTSAverageCIterationsData" + todaysTime + ".txt", 'a')
outraw2 = open("BRENTSRAWAverageCIterationsData" + todaysTime + ".txt", 'a')
for i in range(1, 10000):
    t = random.choice(primesList) * random.choice(primesList)
    getStats(t, out, outraw)
    getStats2(t, out2, outraw2)
    print(i)

    #############################################