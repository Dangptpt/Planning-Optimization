import numpy as np
import random
import copy
import time

class LocalSearch:
    def __init__(self, pop_size, num_generations, time_limit):
        self.pop_size = pop_size
        self.num_generations = num_generations
        self.mutation_probability = 0.0
        self.keep_rate = 1.0
        self.local_search_prob = 1.0
        self.time_limit = time_limit

    def decode(self, individual, N):
        routes = []
        tmp = []
        for i in range(len(individual)):
            if individual[i] >= N:
                routes.append([0] + copy.deepcopy(tmp) + [0])
                tmp = []
            else:
                tmp.append(individual[i])
        routes.append([0] + copy.deepcopy(tmp) + [0])
        return routes
    
    def encode(self, routes):
        individual = []
        num_cities = 0
        for route in routes:
            num_cities += (len(route) - 2)
        for i, route in enumerate(routes):
            for pos in route[1:-1]:
                individual.append(pos)
            if i != len(routes) -1 :
                individual.append(i + 1 + num_cities)
        return individual

    def cost_route(self, distance_matrix, route):
        tmp = 0
        for i in range(0, len(route) - 1):
            try:
                tmp += distance_matrix[route[i]][route[i+1]]
            except IndexError as e:
                print(f"Error accessing distance_matrix[{route[i]}][{route[i+1]}]: {e}")
                print("Route:", route)
                print("Distance Matrix:", distance_matrix)
                raise e
        return tmp

    def fitness_function_individual(self, distance_matrix, individual):
        routes = self.decode(individual, len(distance_matrix))
        fitness = -float("inf")
        for route in routes:
            fitness = max(self.cost_route(distance_matrix, route), fitness)
        return fitness

    def mutate(self, individual):
        if random.uniform(0, 1) < self.mutation_probability:
            start = random.randint(0, len(individual) - 1)
            end = random.randint(0, len(individual) - 1)
            new_individual = np.copy(individual)
            new_individual[start], new_individual[end] = new_individual[end], new_individual[start]
            return new_individual
        else:
            return individual

    def ox_crossover(self, individual1, individual2):
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
        
        return offspring

    def generate_population(self, gen_len):
        population = []
        for i in range(self.pop_size):
            population.append(np.random.permutation([_ for _ in range(1, gen_len+1)]))
        return population

    def select_parents(self, population, fitness_scores):
        parent1 = random.choices(population, k=1)[0]
        parent2 = random.choices(population, k=1)[0]
        return parent1, parent2

    def generate_offspring(self, individual1, individual2):
        child = self.ox_crossover(individual1, individual2)
        child = self.mutate(child)
        return child

    def two_opt(self, distance_matrix, individual):
        routes = self.decode(individual, len(distance_matrix))
        for stt, route in enumerate(routes):
            for i in range(1, len(route) - 1):
                for j in range(i+1, len(route) - 1):
                    new_route = np.copy(route)
                    new_route[i:j+1] = route[j:i-1:-1]
                    new_cost = self.cost_route(distance_matrix, new_route)
                    current_cost = self.cost_route(distance_matrix, route)
                    if new_cost < current_cost:
                        routes[stt] = new_route
        return self.encode(routes)

    def local_search_2(self, distance_matrix, individual):
        routes = self.decode(individual, len(distance_matrix))
        improve = True
        max_stt, max_cost = None, -float("inf")
        min_stt, min_cost = None, float("inf")
        for stt, route in enumerate(routes):
            tmp = self.cost_route(distance_matrix, route)
            if tmp > max_cost:
                max_cost = tmp
                max_stt = stt
            if tmp < min_cost:
                min_cost = tmp
                min_stt = stt

        length = max_cost
        if min_stt != max_stt:
            new_routes = self.decode(individual, len(distance_matrix))
            new_routes[max_stt], new_routes[min_stt], new_length = self.optimize_routes(distance_matrix, new_routes[max_stt], new_routes[min_stt])
            if new_length < length:
                return self.encode(new_routes)     
               
        for i in range(len(routes)):
            if i == max_stt:
                continue
            new_routes = self.decode(individual, len(distance_matrix))
            new_routes[max_stt], new_routes[i], new_length = self.optimize_routes(distance_matrix, new_routes[max_stt], new_routes[i])
            if new_length < length:
                return self.encode(new_routes)
        return individual

    def optimize_routes(self, distance_matrix, route1, route2):
        max_length = max(self.cost_route(distance_matrix, route1), self.cost_route(distance_matrix, route2))
        res_route1 = copy.deepcopy(route1[:])
        res_route2 = copy.deepcopy(route2[:])
        for i in range(1, len(route1)-1):
            for j in range(1, len(route2)-1):
                new_route1 = route1[:]
                new_route2 = route2[:]
                new_route2.insert(j, new_route1.pop(i))
                new_length = max(self.cost_route(distance_matrix, new_route1), self.cost_route(distance_matrix, new_route2))
                if new_length < max_length:
                    res_route1 = new_route1
                    res_route2 = new_route2
                    max_length = new_length
        return res_route1, res_route2, max_length

    def solve(self, instance):
        distance_matrix = instance["distance_matrix"]  # Access distance matrix directly
        N = len(distance_matrix)
        K = N - 1  # Example calculation, adjust as per your instance data
        t_begin = time.time()
        population = self.generate_population(N + K - 2)
        best_individual = None
        best_fitness = float('inf')
        log1 = []
        log2 = [1e9 for i in range(10)]
        for generation in range(self.num_generations):
            fitness_scores = [self.fitness_function_individual(distance_matrix, individual) for individual in population]
            population_with_fitness = list(zip(population, fitness_scores))
            population_with_fitness.sort(key=lambda x: x[1], reverse=False)
            population = [route for route, fitness in population_with_fitness]
            tmp = self.fitness_function_individual(distance_matrix, population[0])
            if  tmp < best_fitness:
                best_individual = population[0]
                best_fitness = tmp
            if generation % 10 == 0:
                log1.append(best_fitness)
            for i in range(len(log2)):
                if log2[i] != 1e9:
                    continue
                else:
                    if ((time.time() - t_begin) > self.time_limit / 10.0 * i):
                        log2[i] = best_fitness
            if time.time() - t_begin >= self.time_limit:
                log2[-1] = best_fitness
                break
            if generation % 10 == 0:
                log1.append(best_fitness)
            if time.time() - t_begin >= self.time_limit:
                break
            next_population = [population[i] for i in range(int(self.pop_size * self.keep_rate))]
            while len(next_population) < self.pop_size:
                parent1, parent2 = self.select_parents(population, fitness_scores)
                child = self.generate_offspring(parent1, parent2)
                next_population.append(child)
            for i in range(len(next_population)):
                if random.uniform(0, 1) < self.local_search_prob:
                    next_population[i] = self.local_search_2(distance_matrix, next_population[i])
                    next_population[i] = self.two_opt(distance_matrix, next_population[i])
            population = next_population
        return self.decode(best_individual, len(distance_matrix)), log1, log2

# Example usage:
def read_input(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    N, m, M = map(int, lines[0].split())
    fields = []
    for line in lines[1:N+1]:
        fields.append(list(map(int, line.split())))
    
    distance_matrix = []
    for line in lines[N+1:2*N+1]:
        distance_matrix.append(list(map(int, line.split())))
    
    return {
        "N": N,
        "m": m,
        "M": M,
        "fields": fields,
        "distance_matrix": distance_matrix
    }

# Example of how to run the algorithm
instance = read_input('test.inp')
local_search = LocalSearch(pop_size=50, num_generations=1000, time_limit=60)
best_solution, log1, log2 = local_search.solve(instance)

print("Best solution:", best_solution)
print("Log1:", log1)
print("Log2:", log2)
