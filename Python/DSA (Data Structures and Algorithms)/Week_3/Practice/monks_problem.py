def func(n, memo={}):
    if n in memo:
        return memo[n]
    if n == 0:
        return 0
    if n == 1:
        return 1
    memo[n] = 2 * func(n - 1, memo) + 1
    return memo[n]

n = int(input().strip())
print(func(n))