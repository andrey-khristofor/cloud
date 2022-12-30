from os import stat
from Pyro4 import expose
from array import *


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers


    def solve(self):
        V = self.read_input()
        n = len(V)
        step = n / len(self.workers)
        mapped = []

        for i in range(0, len(self.workers)):
            mapped.append(self.workers[i].mymap(V, i * step, (i + 1) * step))

        reduced = self.myreduce(mapped)
        self.write_output(reduced)


    @staticmethod
    @expose
    def mymap(V, a, b):
        n = len(V)
        for k in range(a, b):
            for i in range(n):
                for j in range(n):
                    d = V[i][k] + V[k][j]
                    if V[i][j] > d:
                        V[i][j] = d
        return V


    @staticmethod
    @expose
    def myreduce(mapped):
        res = mapped[0].value
        for chunk in mapped:
            res = Solver.mergeMin(res, chunk.value)
        return res



    @staticmethod
    @expose
    def mergeMin(first, second):
        n = len(first)
        for i in range(n):
            for j in range(n):
                if second[i][j] < first[i][j]:
                    first[i][j] = second[i][j]
        return first


    def read_input(self):
        f = open(self.input_file_name, 'r')
        n = int(f.readline())
        V = [[0 for j in range(n)] for i in range(n)]
        for i in range(0, n):
            x = f.readline().split(' ')
            for j in range(0, i + 1):
                curr = int(x[j])
                if curr == 0:
                    curr = 1000000
                V[i][j] = curr
                V[j][i] = curr
        f.close()
        return V

    def write_output(self, output):
        f = open(self.output_file_name, 'w')

        n = len(output)

        for i in range(n):
            for j in range(n):
                f.write(str(output[i][j]) + ' ')
            f.write('\n')

        f.close()