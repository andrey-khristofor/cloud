import math
from random import *

f = open("input.txt", "w")
n = 600
f.write(str(n) + '\n')
v = [[0 for j in range(n)] for i in range(n)]

for i in range(0, n):
    for j in range(0, i + 1):
        if i == j:
            f.write('0 ')
        else:
            curr = random()
            if curr < 0.6:
                f.write('0 ')
            else:
                f.write(str(randint(1,10))+' ')
    f.write('\n')

f.close()