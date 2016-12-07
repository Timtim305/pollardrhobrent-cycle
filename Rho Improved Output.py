import random
import datetime
import sys
import math


import random
import datetime
import sys
import math

def f(x, c, n):
    return (x ** 2 + c) % n

def gcd(a, b):
    while b != 0:
        t = b;
        b = a % b
        a = t
    return a


def pollards(n):  ##returns factor, count
    x = 2
    c = 1
    y = f(x, c, n)
    d = 1
    counter = 0

    found = False
    while not found:
        x = f(x, c, n)
        y = f(f(y, c, n), c, n)
        d = gcd(abs(x - y), n)
        counter += 1

        if (d != 1 and d != n):
            found = True

        if (counter > 100000):
            return (-1, -1)
    print(counter)


def imppollards(n, c):  ##returns factor, count
    x = random.randint(0, n - 1)
    y = random.randint(0, n - 1)
    count = 0
    j = 1
    d = 1
    i = 2
    found = False
    while not found:
        x_next = ((x * x) % n + c) % n
        for j in range(i - 1):
            for i in range(2, j):
                y = (y * y + c) % n
                d = gcd(abs(x_next - y), n)
                count += 1
                if (d != 1) and (d != n):
                    found = True
    print(n, count)

pollards(4087)