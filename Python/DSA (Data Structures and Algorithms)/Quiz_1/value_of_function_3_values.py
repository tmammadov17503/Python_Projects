def fibonacci(n, fibo_memo={}):
    if n in fibo_memo:
        return fibo_memo[n]
    if n == 0:
        return 2
    if n == 1:
        return 3
    fibo_memo[n] = fibonacci(n - 1, fibo_memo) + fibonacci(n - 2, fibo_memo)
    return fibo_memo[n]

def func(x, y, m, memo={}):
    if x <= 0 or y <= 0:
        return 0
    if (x, y) in memo:
        return memo[(x, y)]
    if x <= y:
        memo[(x, y)] = (func(x - 1, y - 2, m, memo) + func(x - 2, y - 1, m, memo) + fibonacci(x)) % m
    else:
        memo[(x, y)] = (func(x - 2, y - 2, m, memo) + fibonacci(y)) % m
    return memo[(x, y)]

x, y, m = map(int, input().split())
print(func(x, y, m))