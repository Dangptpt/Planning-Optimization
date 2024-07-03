def read_input(file_path):
    # Đọc dữ liệu từ tệp đầu vào
    with open(file_path, 'r') as file:
        data = file.read()

    # Tách dòng và chuyển đổi thành danh sách các giá trị
    lines = data.split('\n')
    n, m, M = map(int, lines[0].split())
    fields = []
    for line in lines[1:]:
        if line.strip():
            d, s, e = map(int, line.split())
            fields.append((d, s, e))
    return n, m, M, fields

def check(i, total_sum, day, mark, d, s, e, M):
    # Kiểm tra xem có thể chọn ngày thu hoạch cho cánh đồng i không
    if mark[i] != 0:
        return False
    if total_sum > M:
        return False
    if day < s[i] or day > e[i]:
        return False
    return True

def greedy(n, m, M, d, s, e):
    # Thuật toán tham lam để chọn ngày thu hoạch
    max_day = 0
    mark = [0] * (n + 1)

    # Tìm ngày cuối cùng có thể thu hoạch
    for i in range(1, n + 1):
        max_day = max(max_day, e[i])

    # Duyệt qua từng ngày để chọn cánh đồng thu hoạch
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
    # Đọc tệp đầu vào
    file_path = 'Test/test5000_200.inp'
    N, m, M, fields = read_input(file_path)
    d = [0] * (N + 1)
    s = [0] * (N + 1)
    e = [0] * (N + 1)

    # Gán giá trị cho các cánh đồng
    for i in range(N):
        d[i + 1], s[i + 1], e[i + 1] = fields[i]

    # Gọi thuật toán tham lam để tìm giải pháp ban đầu
    initial_solution, initial_fitness = greedy(N, m, M, d, s, e)
    print("Initial Greedy Solution:", initial_solution)
    print("Initial Greedy Fitness:", initial_fitness)

if __name__ == "__main__":
    main()
