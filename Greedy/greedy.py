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

def check(i, sum, day, mark, d, s, e, M):
    if mark[i] != 0:
        return False
    if sum > M:
        return False
    if day < s[i] or day > e[i]:
        return False
    return True

def greedy(n, m, M, d, s, e):
    max_day = 0
    mark = [0] * (n + 1)
    res = 0

    for i in range(1, n + 1):
        max_day = max(max_day, e[i])

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
                mark[i] = 0

    total = 0
    for i in range(1, n + 1):
        if mark[i] != 0:
            res += 1
            total += d[i]

    print("Total harvested:", res)
    print("Num of fields:", total)

def main():
    file_path = 'test.inp'
    n, m, M, fields = read_input(file_path)
    d = [0] * (n + 1)
    s = [0] * (n + 1)
    e = [0] * (n + 1)
    
    for i in range(n):
        d[i + 1], s[i + 1], e[i + 1] = fields[i]
    
    greedy(n, m, M, d, s, e)

if __name__ == "__main__":
    main()