from ortools.sat.python import cp_model

def solve(N, m, M, fields):
    model = cp_model.CpModel()
    min_day = min(s for d, s, e in fields)
    max_day = max(e for d, s, e in fields)
    x, y = {}, {}
    for i in range(N):
        for j in range(fields[i][1], fields[i][2] + 1):
            x[(i, j)] = model.NewIntVar(0, 1, f'x[{i},{j}]')

    for i in range(min_day, max_day + 1):
        y[i] = model.NewIntVar(0, 1, f'y[{i}]')

    for i in range(N):
        model.Add(sum([x[(i, j)] for j in range(fields[i][1], fields[i][2] + 1)]) <= 1)

    for j in range(min_day, max_day + 1):
        model.Add(sum([x[(i, j)] * fields[i][0] for i in range(N) if j >= fields[i][1] and j <= fields[i][2]]) <= M*y[j]) 
        model.Add(sum([x[(i, j)] * fields[i][0] for i in range(N) if j >= fields[i][1] and j <= fields[i][2]]) >= m*y[j])

    objective = sum([x[(i, j)] * fields[i][0] for i in range(N) for j in range(fields[i][1], fields[i][2] + 1)])
    model.Maximize(objective)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)


    if status == cp_model.OPTIMAL:
        print('Total harvested =', round(solver.ObjectiveValue()))
        harvested_fields = [(i+1, j) for i in range(N) for j in range(fields[i][1], fields[i][2] + 1) if solver.Value(x[(i, j)]) > 0]
        print('Num of field(s):',len(harvested_fields))
        print (len(harvested_fields))
        days_2 = set(x[1] for x in harvested_fields)
        print("Total day(s):",len(days_2))
        # for field, day in harvested_fields:
        #     print(field, day)
    else:
        print('The problem does not have an optimal solution.')


    print("\nStatistics")
    print(f"  status   : {solver.status_name(status)}")
    print(f"  conflicts: {solver.num_conflicts}")
    print(f"  branches : {solver.num_branches}")
    print(f"  wall time: {solver.wall_time} s")

with open('Test/test5000_200.inp', 'r') as file:
    data = file.read()

lines = data.split('\n')
N, m, M = map(int, lines[0].split())
fields = []
for line in lines[1:]:
    d, s, e = map(int, line.split())
    fields.append((d, s, e))

# fields = []
# N, m, M = map(int, input().split())
# for i in range(N):
#     d, s, e = map(int, input().split())
#     fields.append((d, s, e))

solve(N, m, M, fields)
