def func(n):
    mod = 123456789
    if n == 1:
        return 1
    return pow(2, n - 2, mod)

n = int(input())
print(func(n))
