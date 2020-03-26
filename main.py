import cvxpy as cp

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
n = 7
x = []
for i in range(0, n):
    x.append([])
    for j in range(0, n):
        x[i].append(cp.Variable(1, boolean=True))

b = []
for i in range(0, n):
    b.append([])
    for j in range(0, n):
        b[i].append(cp.Variable(1, boolean=True))

for i in range(0, n):
    for j in range(0, n):
        b[i][j] = 1 - x[(j - i) % n][j]

objective = cp.Minimize(0)
constraints = []

# x can only be one of 0..n
for i in range(0, n):
    constraints.append(1 == cp.sum(x[i]))

# each x is different
for i in range(0, n):
    expr = 0 + x[0][i]
    for j in range(1, n):
        expr += x[j][i]
    constraints.append(1 == expr)

for i in range(0, n):
    constraints.append(cp.sum(b[i]) >= n - 1)

# symmetry breaking constraint
constraints.append(x[0][0] == 1)

cntSolutions = 0
while True:
    prob = cp.Problem(objective, constraints)
    result = prob.solve()

    if result is None:
        # no more solutions are found
        break

    cntSolutions += 1
    print('Seating:')
    y = []
    for i in range(0, n):
        for j in range(0, n):
            if x[i][j].value >= 0.9:
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

    # exclude current solution
    expr = 0 + x[0][y[0]]
    for i in range(1, n):
        expr += x[i][y[i]]
    constraints.append(expr <= n - 1)

print(f'Total solutions: {cntSolutions}')
