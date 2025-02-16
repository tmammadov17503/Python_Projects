def func(n):
    MOD = 35242346
    total = pow(1, n, MOD) + pow(2, n, MOD)

    for i in range(3, 101):
        total = (total + (i-1) * pow(i, n, MOD)) % MOD

    return total

n = int(input().strip())
print(func(n))
