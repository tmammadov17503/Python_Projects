def func(x, y, memo={}):
    if x <= 0 or y <= 0:
        return 0
    if (x, y) in memo:
        return memo[(x, y)]

    if x <= y:
        memo[(x, y)] = func(x - 1, y - 2) + func(x - 2, y - 1) + 2
    else:
        memo[(x, y)] = func(x - 2, y - 2) + 1

    return memo[(x, y)]


x, y = map(int, input().split())
print(func(x, y))