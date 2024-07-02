


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
        population = set()
        attempts = 0
        max_days = max(e for _, s, e in fields) + 1

        while len(population) < population_size and attempts < 10 * population_size:
            individual = [-1] * N
            daily_harvest = [0] * max_days

            for i in range(N):
                possible_days = [day for day in range(fields[i][1], fields[i][2] + 1) if daily_harvest[day] + fields[i][0] <= M]
                if possible_days:
                    chosen_day = random.choice(possible_days)
                    individual[i] = chosen_day
                    daily_harvest[chosen_day] += fields[i][0]

            # Ensure all fields are assigned a day and daily harvest constraints are satisfied
            if all(day != -1 for day in individual) and all(m <= daily_harvest[day] <= M for day in range(len(daily_harvest)) if daily_harvest[day] > 0):
                print(individual_tuple)
                individual_tuple = tuple(individual)
                if individual_tuple not in population:
                    population.add(individual_tuple)


        return [list(ind) for ind in population]

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
        print(len(population))
        best_individual = None
        best_fitness = float('inf')
        log1 = []
        log2 = [1e9 for _ in range(10)]

        for generation in range(self.num_generations):
            fitness_scores = [self.fitness_function_individual(individual, N, m, M, fields) for individual in population]
            population_with_fitness = list(zip(population, fitness_scores))
            population_with_fitness.sort(key=lambda x: x[1], reverse=True)
            population = [ind for ind, fitness in population_with_fitness]
            print(population)
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
ga = GA(pop_size=10, num_generations=10, mutation_probability=0.1, local_search_prob=0.0, keep_rate=0.5, time_limit=60)
best_individual, log1, log2 = ga.solve(N, m, M, fields)
print("Best individual:", best_individual)
print("Log1:", log1)
print("Log2:", log2)
