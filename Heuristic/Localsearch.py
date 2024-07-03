import numpy as np
import random
import time

def read_input(file_path):
    # Hàm đọc dữ liệu từ tệp và trả về các tham số và danh sách các ô
    with open(file_path, 'r') as file:
        data = file.read()
    
    lines = data.split('\n')
    n, m, M = map(int, lines[0].split())  # Đọc n, m, M từ dòng đầu tiên
    fields = []
    for line in lines[1:]:
        if line.strip():
            d, s, e = map(int, line.split())
            fields.append((d, s, e))  # Đọc dữ liệu các ô và thêm vào danh sách
    return n, m, M, fields

def check(i, sum, day, mark, d, s, e, M):
    # Hàm kiểm tra điều kiện hợp lệ của một ô
    if mark[i] != 0:  # Nếu ô đã được đánh dấu, trả về False
        return False
    if sum > M:  # Nếu tổng sản lượng vượt quá M, trả về False
        return False
    if day < s[i] or day > e[i]:  # Nếu ngày không nằm trong khoảng [s[i], e[i]], trả về False
        return False
    return True  # Nếu tất cả điều kiện đều thỏa mãn, trả về True

def greedy(n, m, M, d, s, e):
    # Thuật toán tham lam để tạo giải pháp ban đầu
    max_day = 0
    mark = [0] * (n + 1)

    for i in range(1, n + 1):
        max_day = max(max_day, e[i])  # Tìm ngày lớn nhất có thể thu hoạch

    for day in range(1, max_day + 1):
        sum = 0
        tmp = []
        for i in range(1, n + 1):
            if check(i, sum + d[i], day, mark, d, s, e, M):
                mark[i] = day
                sum += d[i]
                tmp.append(i)
        if sum < m:
            for i in tmp:
                mark[i] = 0  # Hủy bỏ các ô không đạt điều kiện

    solution = [mark[i] for i in range(1, n + 1)]
    return solution

class LocalSearch:
    # Định nghĩa lớp LocalSearch (Tìm kiếm cục bộ)
    def __init__(self, max_iterations, N, m, M, fields):
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
            if day !=0:
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

    def local_search(self, initial_solution):
        # Hàm thực hiện tìm kiếm cục bộ
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

# Ví dụ sử dụng
N, m, M, fields = read_input('Test/test5000_200.inp')
d = [0] * (N + 1)
s = [0] * (N + 1)
e = [0] * (N + 1)

for i in range(N):
    d[i + 1], s[i + 1], e[i + 1] = fields[i]

# Tạo giải pháp ban đầu bằng thuật toán tham lam
initial_solution = greedy(N, m, M, d, s, e)

# Sử dụng thuật toán tìm kiếm cục bộ để tìm giải pháp tốt nhất
local_search = LocalSearch(max_iterations=1000, N=N, m=m, M=M, fields=fields)
best_solution = local_search.local_search(initial_solution)
best_fitness = local_search.fitness_function(best_solution)[0]

# In ra giải pháp và độ thích nghi tốt nhất
print("Best solution:", best_solution)
print("Best fitness:", best_fitness)
