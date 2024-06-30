import random

def generate_test_case(filename, N):
    # Generate N, m, M within their constraints
    # m = random.randint(1, 10000)
    # M = random.randint(m, 10000)
    
    # Initialize a list to store the fields
    fields = []
    total = 0;
    for i in range(N):
        d = random.randint(1, 100)
        s = random.randint(1, 950)
        # e must be >= s
        e = s + random.randint(1, 50)  
        fields.append((d, s, e))
        total += d
    m = random.randint(50, 200)
    M = random.randint(m, 500)
    min_day = min([field[1] for field in fields])
    max_day = max([field[2] for field in fields])
    print(total, min_day, max_day)
    # Write the test case to the file
    with open(filename, 'w') as f:
        f.write(f"{N} {m} {M}\n")
        for field in fields:
            f.write(f"{field[0]} {field[1]} {field[2]}\n")

# Generate a test case and save it to a file
generate_test_case('Test/test100_1.inp', 100)

