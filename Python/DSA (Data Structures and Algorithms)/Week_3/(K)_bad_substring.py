def func(n, memo={}):
    if n in memo:
        return memo[n]
    if n == 0:
        return 1
    if n == 1:
        return 3
    memo[n] = 3 * func(n - 1, memo) - func(n-2, memo)
    return memo[n]

n = int(input().strip())
print(func(n))