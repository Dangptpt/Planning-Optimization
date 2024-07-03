from ortools.sat.python import cp_model

def solve(N, m, M, fields):
    # Khởi tạo mô hình CP
    model = cp_model.CpModel()
    
    # Xác định ngày bắt đầu và kết thúc tối thiểu và tối đa
    min_day = min(s for d, s, e in fields)
    max_day = max(e for d, s, e in fields)
    
    # Khởi tạo các biến x[i, j] biểu thị liệu cánh đồng i có được thu hoạch vào ngày j hay không
    x, y = {}, {}
    for i in range(N):
        for j in range(fields[i][1], fields[i][2] + 1):
            x[(i, j)] = model.NewIntVar(0, 1, f'x[{i},{j}]')

    # Khởi tạo các biến y[j] biểu thị liệu có hoạt động thu hoạch vào ngày j hay không
    for i in range(min_day, max_day + 1):
        y[i] = model.NewIntVar(0, 1, f'y[{i}]')

    # Ràng buộc: mỗi cánh đồng chỉ được thu hoạch tối đa 1 lần
    for i in range(N):
        model.Add(sum([x[(i, j)] for j in range(fields[i][1], fields[i][2] + 1)]) <= 1)

    # Ràng buộc: tổng sản lượng thu hoạch trong một ngày phải nằm trong khoảng [m, M]
    for j in range(min_day, max_day + 1):
        model.Add(sum([x[(i, j)] * fields[i][0] for i in range(N) if j >= fields[i][1] and j <= fields[i][2]]) <= M * y[j]) 
        model.Add(sum([x[(i, j)] * fields[i][0] for i in range(N) if j >= fields[i][1] and j <= fields[i][2]]) >= m * y[j])

    # Hàm mục tiêu: tối đa hóa tổng sản lượng thu hoạch
    objective = sum([x[(i, j)] * fields[i][0] for i in range(N) for j in range(fields[i][1], fields[i][2] + 1)])
    model.Maximize(objective)

    # Khởi tạo solver và giải quyết mô hình
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Kiểm tra trạng thái giải pháp và in kết quả
    if status == cp_model.OPTIMAL:
        print('Total harvested =', round(solver.ObjectiveValue()))
        harvested_fields = [(i+1, j) for i in range(N) for j in range(fields[i][1], fields[i][2] + 1) if solver.Value(x[(i, j)]) > 0]
        print('Num of field(s):', len(harvested_fields))
        days_2 = set(x[1] for x in harvested_fields)
        print("Total day(s):", len(days_2))
    else:
        print('The problem does not have an optimal solution.')

    # In thông tin thống kê
    print("\nStatistics")
    print(f"  status   : {solver.status_name(status)}")
    print(f"  conflicts: {solver.num_conflicts}")
    print(f"  branches : {solver.num_branches}")
    print(f"  wall time: {solver.wall_time} s")

# Đọc dữ liệu từ tệp đầu vào
with open('Test/test5000_200.inp', 'r') as file:
    data = file.read()

lines = data.split('\n')
N, m, M = map(int, lines[0].split())
fields = []
for line in lines[1:]:
    if line.strip():
        d, s, e = map(int, line.split())
        fields.append((d, s, e))

# Gọi hàm solve để giải quyết bài toán
solve(N, m, M, fields)
