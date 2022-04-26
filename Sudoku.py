from random import randint
import random
from copy import deepcopy

# Global Variables & helper functions
Population_Count = 500
dim = 9
str_size = dim * dim


def compare_index(arr, x, y):
    for pair in arr:
        if x == ((pair[0] * 9) + pair[1]) or y == ((pair[0] * 9) + pair[1]):
            return True
    return False


# ----------------------------------------------------------------------------------------------------------------------

class Sudoku:
    global dim

    def __init__(self):
        self.Board = [[5, 0, 0, 4, 6, 7, 3, 0, 9],
                      [9, 0, 3, 8, 1, 0, 4, 2, 7],
                      [1, 7, 4, 2, 0, 3, 0, 0, 0],
                      [2, 3, 1, 9, 7, 6, 8, 5, 4],
                      [8, 5, 7, 1, 2, 4, 0, 9, 0],
                      [4, 9, 6, 3, 0, 8, 1, 7, 2],
                      [0, 0, 0, 0, 8, 9, 2, 6, 0],
                      [7, 8, 2, 6, 4, 1, 0, 0, 5],
                      [0, 1, 0, 0, 0, 0, 7, 0, 8]]
        self.fitness = self.Fitness()
        self.digit_count = [0] * 9

    def get_index(self):
        x = list()
        for i in range(9):
            for j in range(9):
                if self.Board[i][j] != 0:
                    self.digit_count[self.Board[i][j] - 1] += 1
                    x.append([i, j])
        return x

    def fill(self):
        for i in range(9):
            for j in range(9):
                if self.Board[i][j] == 0:
                    self.Board[i][j] = randint(1, 9)
                    while self.digit_count[self.Board[i][j] - 1] == 9:  # make sure each digit is 9 times
                        self.Board[i][j] = randint(1, 9)
                    self.digit_count[self.Board[i][j] - 1] += 1

        self.fitness = self.Fitness()
        return self

    def copy(self, matrix):
        self.Board = deepcopy(matrix)
        self.fitness = self.Fitness()

    def get(self):
        return self

    def Print(self):
        print("|---------Sudoku----------|")
        for i in range(dim):
            print(self.Board[i])

    def Fitness(self):
        fitness = 0
        for i in range(dim):
            for j in range(dim):
                # checking rows
                for k in range(i + 1, dim):
                    if self.Board[i][j] == self.Board[k][j]:
                        fitness += 1
                # check columns
                for k in range(j + 1, dim):
                    if self.Board[i][j] == self.Board[i][k]:
                        fitness += 1
                # check 3 x 3 board
                start_col = j - (j % 3)
                start_row = i - (i % 3)
                end_col = start_col + 3
                end_row = start_row + 3
                for m in range(start_row, end_row):
                    for n in range(start_col, end_col):
                        if m == i and n == j:
                            continue
                        if self.Board[i][j] == self.Board[m][n]:
                            fitness += 1
        return fitness


# ----------------------------------------------------------------------------------------------------------------------


def String(matrix):
    global dim
    s = ""
    for i in range(dim):
        for j in range(dim):
            s += str(matrix[i][j])
    return s


def Matrix(s):
    global dim
    matrix = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    index = 0
    for i in range(dim):
        for j in range(dim):
            matrix[i][j] = int(s[index])
            index += 1
    return matrix


def RandomPair():
    global Population_Count
    x = randint(0, Population_Count - 1)
    y = randint(0, Population_Count - 1)
    while x == y:
        y = randint(0, Population_Count - 1)  # make sure two different
    return x, y


# ----------------------------------------------------------------------------------------------------------------------


def CrossOver(a, b):  # takes two strings and perform two-point crossover
    global str_size
    pivot1 = randint(0, str_size - 2)  # first pivot
    pivot2 = randint(pivot1 + 1, str_size - 1)  # second

    s = ""
    s = a[0: pivot1]
    s += b[pivot1: pivot2]
    s += a[pivot2: str_size]
    return s


def Mutate(x, arr):  # swap two genes in a chromosome while keeping fixed positions
    index1 = randint(0, str_size - 2)  # first pivot
    index2 = randint(index1 + 1, str_size - 1)  # second
    while compare_index(arr, index1, index2):
        index1 = randint(0, str_size - 2)
        index2 = randint(index1 + 1, str_size - 1)
    s = ""
    for i in range(str_size):
        if i == index1:
            s += x[index2]
        elif i == index2:
            s += x[index1]
        else:
            s += x[i]
    return s


# ----------------------------------------------------------------------------------------------------------------------


class Population:
    population = list()
    Fixed_Index = list()

    def __init__(self):
        self.generation = 0
        for i in range(Population_Count):
            s = Sudoku()
            s.fill()
            self.population.append(deepcopy(s))
            del s
        self.Fixed_Index = Sudoku().get_index()

    def GeneticAlgorithm(self):
        global Population_Count
        g_limit = 1000

        while self.generation < g_limit:
            self.generation += 1
            new_gen = list()

            # Sorting bby fitness in descending order
            self.population.sort(key=lambda obj: obj.fitness)

            # check if found otherwise print best fit
            fit = self.population[0].fitness
            if fit == 0:
                return self.population[0]

            print("Generation = ", self.generation, "  Best Fit = ", fit)

            # 0.2 elitism
            for i in range(int(0.2 * Population_Count)):
                new_gen.append(deepcopy(self.population[i]))

            # 0.4 crossover
            for i in range(int(0.2 * Population_Count), int(0.6 * Population_Count)):
                x, y = RandomPair()
                s = Sudoku()
                s.copy(Matrix(CrossOver(String(self.population[x].Board), String(self.population[y].Board))))
                new_gen.append(deepcopy(s))
                del s

            # rest 0.4 mutation
            for i in range(int(0.6 * Population_Count), int(Population_Count)):
                s = Sudoku()
                index = randint(0, Population_Count - 1)
                s.copy(Matrix(Mutate(String(self.population[index].Board), self.Fixed_Index)))
                new_gen.append(deepcopy(s))
                del s

            # new gen replaces old
            self.population = deepcopy(new_gen)
            del new_gen

        return self.population[0]
