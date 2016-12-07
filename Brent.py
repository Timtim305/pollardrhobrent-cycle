from fractions import gcd
from random import randint
import time
start_time = time.time()
def brent(N):
    if N % 2 == 0:
        return 2
    step = 0
    y, c, m = randint(1, N - 1), randint(1, N - 1), randint(1, N - 1)
    g, r, q = 1, 1, 1
    while g == 1:
        x = y
        for i in range(r):
            y = ((y**2) % N + c) % N
        k = 0
        while (k < r and g == 1):
            ys = y
            for i in range(min(m, r - k)):
                y = ((y**2) % N + c) % N
                q = q * (abs(x - y)) % N
            g = gcd(q, N)
            step+=1
            k = k + m
        r = r * 2
    if g == N:
        while True:
            ys = ((ys * ys) % N + c) % N
            g = gcd(abs(x - ys), N)
            step += 1
            if g > 1:
                break
    print(g)
    print(step)
    return g

brent(454793809843660109)
print("--- %s seconds ---" % (time.time() - start_time))