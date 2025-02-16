def func(a, b):
    i = 0
    while a % (b ** (i + 1)) == 0:
        i += 1
    return i

a, b = map(int, input().split())
print(func(a, b))