import numpy as np
import random
import time

# Định nghĩa lớp TabuSearch (Tìm kiếm Tabu)
class TabuSearch:
    def __init__(self, tabu_size, max_iterations, N, m, M, fields):
        # Khởi tạo các tham số cho thuật toán tìm kiếm Tabu
        self.tabu_size = tabu_size
        self.max_iterations = max_iterations
        self.N = N
        self.m = m
        self.M = M
        self.fields = fields

    def decode(self, individual):
        # Giải mã cá thể (ở đây chỉ trả về chính cá thể đó)
        return individual

    def encode(self, solution):
        # Mã hóa lại giải pháp (ở đây cũng chỉ trả về chính giải pháp đó)
        return solution

    def fitness_function(self, solution):
        # Hàm tính toán độ thích nghi cho một giải pháp
        daily_harvest = {}
        total_harvest = 0

        for i in range(self.N):
            day = solution[i]
            if day != 0:
                if day not in daily_harvest:
                    daily_harvest[day] = 0
                daily_harvest[day] += self.fields[i][0]

        for harvest in daily_harvest.values():
            if harvest < self.m or harvest > self.M:
                # Nếu thu hoạch không hợp lệ, đặt sản lượng của ngày đó thành 0
                continue
            total_harvest += harvest

        return total_harvest,

    def get_valid_neighbors(self, solution):
        # Hàm lấy các hàng xóm hợp lệ của một giải pháp
        neighbors = []
        for i in range(self.N):
            for day in range(self.fields[i][1], self.fields[i][2] + 1):
                if day != solution[i]:
                    neighbor = solution.copy()
                    neighbor[i] = day

                    # Kiểm tra nếu hàng xóm là hợp lệ
                    if self.is_valid_neighbor(neighbor):
                        neighbors.append(neighbor)
        return neighbors

    def is_valid_neighbor(self, neighbor):
        # Hàm kiểm tra nếu hàng xóm là hợp lệ
        daily_harvest = {}
        for i in range(self.N):
            day = neighbor[i]
            if day not in daily_harvest:
                daily_harvest[day] = 0
            daily_harvest[day] += self.fields[i][0]
        return True

    def tabu_search(self, initial_solution):
        # Hàm thực hiện tìm kiếm Tabu
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

# Đọc dữ liệu từ tệp
def read_input(file_path):
    with open(file_path, 'r') as file:
        data = file.read()

    lines = data.split('\n')
    n, m, M = map(int, lines[0].split())
    fields = []
    for line in lines[1:]:
        if line.strip():
            d, s, e = map(int, line.split())
            fields.append((d, s, e))
    return n, m, M, fields

# Hàm kiểm tra điều kiện hợp lệ của một ô
def check(i, total_sum, day, mark, d, s, e, M):
    if mark[i] != 0:
        return False
    if total_sum > M:
        return False
    if day < s[i] or day > e[i]:
        return False
    return True

# Thuật toán tham lam để tạo giải pháp ban đầu
def greedy(n, m, M, d, s, e):
    max_day = 0
    mark = [0] * (n + 1)

    for i in range(1, n + 1):
        max_day = max(max_day, e[i])

    for day in range(1, max_day + 1):
        total_sum = 0
        tmp = []
        for i in range(1, n + 1):
            if check(i, total_sum + d[i], day, mark, d, s, e, M):
                mark[i] = day
                total_sum += d[i]
                tmp.append(i)
        if total_sum < m:
            for i in tmp:
                mark[i] = 0

    solution = [mark[i] for i in range(1, n + 1)]
    total_harvested = sum(1 for i in range(1, n + 1) if mark[i] != 0)
    num_fields = sum(d[i] for i in range(1, n + 1) if mark[i] != 0)

    # In tổng fitness
    fitness = sum(d[i] for i in range(1, n + 1) if mark[i] != 0)
    print("Total harvested:", total_harvested)
    print("Num of fields:", num_fields)
    print("Fitness:", fitness)
    
    return solution, fitness

# Ví dụ sử dụng
def main():
    file_path = 'Test/test5000_200.inp'
    N, m, M, fields = read_input(file_path)
    d = [0] * (N + 1)
    s = [0] * (N + 1)
    e = [0] * (N + 1)

    for i in range(N):
        d[i + 1], s[i + 1], e[i + 1] = fields[i]

    initial_solution, initial_fitness = greedy(N, m, M, d, s, e)
    print("Initial Greedy Solution:", initial_solution)
    print("Initial Greedy Fitness:", initial_fitness)

    tabu_search = TabuSearch(tabu_size=10, max_iterations=1000, N=N, m=m, M=M, fields=fields)
    best_solution = tabu_search.tabu_search(initial_solution)
    best_fitness = tabu_search.fitness_function(best_solution)[0]

    print("Best solution:", best_solution)
    print("Best fitness:", best_fitness)

if __name__ == "__main__":
    main()
