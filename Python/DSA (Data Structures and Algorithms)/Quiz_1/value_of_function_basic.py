def func(n, memo={}):
    if n in memo:
        return memo[n]
    if n == 0:
        return 1
    else:
        memo[n] = func(n // 2, memo) + func(n // 3, memo)
        return memo[n]

n = int(input())
print(func(n))