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

def check(i, total_sum, day, mark, d, s, e, M):
    if mark[i] != 0:
        return False
    if total_sum > M:
        return False
    if day < s[i] or day > e[i]:
        return False
    return True

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

# Example usage
def main():
    file_path = r'D:\school\TULKH\Planning-Optimization\Test\test100_100.inp'
    N, m, M, fields = read_input(file_path)
    d = [0] * (N + 1)
    s = [0] * (N + 1)
    e = [0] * (N + 1)

    for i in range(N):
        d[i + 1], s[i + 1], e[i + 1] = fields[i]

    initial_solution, initial_fitness = greedy(N, m, M, d, s, e)
    print("Initial Greedy Solution:", initial_solution)
    print("Initial Greedy Fitness:", initial_fitness)

if __name__ == "__main__":
    main()
