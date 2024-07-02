import numpy as np
import random
import time

class LocalSearch:
    def __init__(self, max_iterations, N, m, M, fields):
        self.max_iterations = max_iterations
        self.N = N
        self.m = m
        self.M = M
        self.fields = fields

    def decode(self, individual):
        return individual

    def encode(self, solution):
        return solution

    def fitness_function(self, solution):
        daily_harvest = {}
        total_harvest = 0

        for i in range(self.N):
            day = solution[i]
            if day not in daily_harvest:
                daily_harvest[day] = 0
            daily_harvest[day] += self.fields[i][0]
            total_harvest += self.fields[i][0]

        for harvest in daily_harvest.values():
            if harvest < self.m or harvest > self.M:
                return 0,

        return total_harvest,

    def get_valid_neighbors(self, solution):
        neighbors = []
        for i in range(self.N):
            for day in range(self.fields[i][1], self.fields[i][2] + 1):
                if day != solution[i]:
                    neighbor = solution.copy()
                    neighbor[i] = day

                    # Check if the neighbor is valid
                    if self.is_valid_neighbor(neighbor):
                        neighbors.append(neighbor)
        return neighbors

    def is_valid_neighbor(self, neighbor):
        daily_harvest = {}
        for i in range(self.N):
            day = neighbor[i]
            if day not in daily_harvest:
                daily_harvest[day] = 0
            daily_harvest[day] += self.fields[i][0]

        for harvest in daily_harvest.values():
            if harvest < self.m or harvest > self.M:
                return False
        return True

    def local_search(self, initial_solution):
        current_solution = initial_solution
        best_solution = initial_solution
        current_fitness = self.fitness_function(current_solution)[0]
        best_fitness = current_fitness

        for _ in range(self.max_iterations):
            neighbors = self.get_valid_neighbors(current_solution)
            next_solution = None
            next_fitness = -1

            for neighbor in neighbors:
                neighbor_fitness = self.fitness_function(neighbor)[0]
                if neighbor_fitness > next_fitness:
                    next_solution = neighbor
                    next_fitness = neighbor_fitness

            if next_fitness <= current_fitness:
                break

            current_solution = next_solution
            current_fitness = next_fitness

            if current_fitness > best_fitness:
                best_solution = current_solution
                best_fitness = current_fitness

        return best_solution

# Reading input from a file
def read_input(file_path):
    with open(file_path, 'r') as file:
        data = file.read()

    lines = data.split('\n')
    N, m, M = map(int, lines[0].split())
    fields = []
    for line in lines[1:]:
        if line.strip():
            d, s, e = map(int, line.split())
            fields.append((d, s, e))
    return N, m, M, fields

def generate(N, fields, m, M):
    individual = [0] * N
    daily_harvest = [0] * (max(e for _, s, e in fields) + 1)

    for i in range(N):
        for day in range(fields[i][1], fields[i][2] + 1):
            if daily_harvest[day] + fields[i][0] <= M:
                individual[i] = day
                daily_harvest[day] += fields[i][0]
                break
    return individual

# Example usage
N, m, M, fields = read_input('test.inp')

initial_solution = generate(N, fields, m, M)
local_search = LocalSearch(max_iterations=1000, N=N, m=m, M=M, fields=fields)
best_solution = local_search.local_search(initial_solution)
best_fitness = local_search.fitness_function(best_solution)[0]
print("Best solution:", best_solution)
print("Best fitness:", best_fitness)
