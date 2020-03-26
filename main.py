from mip import Model, BINARY, xsum, OptimizationStatus

# terminal colors
black = lambda text: '\033[0;30m' + text + '\033[0m'
red = lambda text: '\033[0;31m' + text + '\033[0m'
green = lambda text: '\033[0;32m' + text + '\033[0m'
yellow = lambda text: '\033[0;33m' + text + '\033[0m'
blue = lambda text: '\033[0;34m' + text + '\033[0m'
magenta = lambda text: '\033[0;35m' + text + '\033[0m'
cyan = lambda text: '\033[0;36m' + text + '\033[0m'
white = lambda text: '\033[0;37m' + text + '\033[0m'

# actual problem
model = Model('thinkmathone')
model.verbose = 0
n = 7
x = []
for i in range(0, n):
    x.append([])
    for j in range(0, n):
        x[i].append(model.add_var(var_type=BINARY, name=f'x_${i}_${j}'))

b = []
for i in range(0, n):
    b.append([])
    for j in range(0, n):
        b[i].append(model.add_var(var_type=BINARY, name=f'b_${i}_${j}'))

for i in range(0, n):
    for j in range(0, n):
        b[i][j] = 1 - x[(j - i) % n][j]


# x can only be one of 0..n
for i in range(0, n):
    model += 1 == xsum(x[i][j] for j in range(n))

# each x is different
for i in range(0, n):
    expr = 0 + x[0][i]
    for j in range(1, n):
        expr += x[j][i]
    model += 1 == expr

# only one can be satisfied
for i in range(0, n):
    model += xsum(b[i][j] for j in range(n)) == n - 1

# symmetry breaking constraint
model += x[0][0] == 1
cntSolutions = 0
while True:
    result = model.optimize()
    if result != OptimizationStatus.OPTIMAL:
        # no more solutions are found
        break

    cntSolutions += 1
    print('Seating:')
    y = []
    for i in range(0, n):
        for j in range(0, n):
            if x[i][j].xi(0) >= 0.9:
                print(f'x[{i}][{j}]')
                y.append(j)

    # print out all permutations
    print('Permutations:')
    for i in range(0, n):
        print(f'permutation {i}:')
        for j in range(0, n):
            print(j, end='')
        print()
        for j in range(0, n):
            val = y[(j + i) % n]
            if j == val:
                print(red(str(val)), end='')
            else:
                print(val, end='')
        print()

    print()
    print()
    # exclude current solution
    tmp = 0 + x[0][y[0]]
    for i in range(1, n):
        tmp += x[i][y[i]]
    model += tmp <= n - 1

print(f'Total solutions: {cntSolutions}')
