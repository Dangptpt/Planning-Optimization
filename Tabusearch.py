import numpy as np
import random
import time

class GA:
    def __init__(self, pop_size, num_generations, mutation_probability, local_search_prob, keep_rate, time_limit):
        self.pop_size = pop_size
        self.num_generations = num_generations
        self.mutation_probability = mutation_probability
        self.keep_rate = keep_rate
        self.local_search_prob = local_search_prob
        self.time_limit = time_limit

    def decode(self, individual, N):
        return individual

    def encode(self, routes):
        return routes

    def fitness_function_individual(self, individual, N, m, M, fields):
        daily_harvest = {}
        total_harvest = 0

        for i in range(N):
            day = individual[i]
            if day not in daily_harvest:
                daily_harvest[day] = 0
            daily_harvest[day] += fields[i][0]
            total_harvest += fields[i][0]

        for harvest in daily_harvest.values():
            if harvest < m or harvest > M:
                return 0,

        return total_harvest,

    def mutate(self, individual, N, m, M, fields):
        if random.uniform(0, 1) < self.mutation_probability:
            start = random.randint(0, len(individual) - 1)
            end = random.randint(0, len(individual) - 1)
            new_individual = np.copy(individual)
            new_individual[start], new_individual[end] = new_individual[end], new_individual[start]

            if self.fitness_function_individual(new_individual, N, m, M, fields)[0] == 0:
                return individual  # Return the original if mutation is invalid
            return new_individual
        else:
            return individual

    def ox_crossover(self, individual1, individual2, N, m, M, fields):
        cut1 = random.randint(0, len(individual1) - 1)
        cut2 = random.randint(0, len(individual1) - 1)
        if cut1 > cut2:
            cut1, cut2 = cut2, cut1
        offspring = [-1] * len(individual1)
        offspring[cut1:cut2+1] = individual1[cut1:cut2+1]
        pos = (cut2 + 1) % len(individual1)
        for i in range(len(individual1)):
            if individual2[i] not in offspring:
                while offspring[pos] != -1:
                    pos = (pos + 1) % len(individual1)
                offspring[pos] = individual2[i]

        if self.fitness_function_individual(offspring, N, m, M, fields)[0] == 0:
            return individual1
        return offspring

    def generate_population(self, N, fields, population_size, m, M):
        population = []
        for _ in range(population_size):
            individual = [0] * N
            daily_harvest = [0] * (max(e for _, s, e in fields) + 1)

            for i in range(N):
                for day in range(fields[i][1], fields[i][2] + 1):
                    if daily_harvest[day] + fields[i][0] <= M:
                        individual[i] = day
                        daily_harvest[day] += fields[i][0]
                        break

            population.append(individual)
        return population

    def select_parents(self, population):
        parent1 = random.choices(population, k=1)[0]
        parent2 = random.choices(population, k=1)[0]
        return parent1, parent2

    def generate_offspring(self, individual1, individual2, N, m, M, fields):
        child = self.ox_crossover(individual1, individual2, N, m, M, fields)
        child = self.mutate(child, N, m, M, fields)
        return child

    def solve(self, N, m, M, fields):
        t_begin = time.time()
        population = self.generate_population(N, fields, self.pop_size, m, M)
        best_individual = None
        best_fitness = float('inf')
        log1 = []
        log2 = [1e9 for _ in range(10)]

        for generation in range(self.num_generations):
            fitness_scores = [self.fitness_function_individual(individual, N, m, M, fields) for individual in population]
            population_with_fitness = list(zip(population, fitness_scores))
            population_with_fitness.sort(key=lambda x: x[1], reverse=True)
            population = [ind for ind, fitness in population_with_fitness]
            tmp = self.fitness_function_individual(population[0], N, m, M, fields)
            if tmp[0] < best_fitness:
                best_individual = population[0]
                best_fitness = tmp[0]
            if generation % 10 == 0:
                log1.append(best_fitness)
            for i in range(len(log2)):
                if log2[i] != 1e9:
                    continue
                else:
                    if (time.time() - t_begin) > self.time_limit / 10.0 * i:
                        log2[i] = best_fitness
            if time.time() - t_begin >= self.time_limit:
                log2[-1] = best_fitness
                break
            next_population = [population[i] for i in range(int(self.pop_size * self.keep_rate))]
            while len(next_population) < self.pop_size:
                parent1, parent2 = self.select_parents(population)
                child = self.generate_offspring(parent1, parent2, N, m, M, fields)
                next_population.append(child)
            population = next_population
        return best_individual, log1, log2


class TabuSearch:
    def __init__(self, tabu_size, max_iterations, N, m, M, fields):
        self.tabu_size = tabu_size
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

    def tabu_search(self, initial_solution):
        current_solution = initial_solution
        best_solution = initial_solution
        tabu_list = []
        tabu_list.append(current_solution.copy())
        current_fitness = self.fitness_function(current_solution)[0]
        best_fitness = current_fitness

        for _ in range(self.max_iterations):
            neighbors = self.get_valid_neighbors(current_solution)
            next_solution = None
            next_fitness = -1

            for neighbor in neighbors:
                if neighbor not in tabu_list:
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

            tabu_list.append(next_solution.copy())
            if len(tabu_list) > self.tabu_size:
                tabu_list.pop(0)

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

# Example usage
N, m, M, fields = read_input('test.inp')
ga = GA(pop_size=500, num_generations=1000, mutation_probability=0.1, local_search_prob=0.0, keep_rate=0.5, time_limit=60)
initial_solution , log1, log2 = ga.solve(N, m, M, fields)
tabu_search = TabuSearch(tabu_size=10, max_iterations=1000, N=N, m=m, M=M, fields=fields)
best_solution = tabu_search.tabu_search(initial_solution)
best_fitness = tabu_search.fitness_function(best_solution)[0]
print("Best solution:", best_solution)
print("Best fitness:", best_fitness)
