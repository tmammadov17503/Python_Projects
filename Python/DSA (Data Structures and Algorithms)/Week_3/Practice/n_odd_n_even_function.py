def count_ones_in_binary(n):
    return bin(n).count('1')

def func(n, memo={}):
    if n in memo:
        return memo[n]
    if n == 0:
        return 0
    if n % 2 == 1:
        memo[n] = 2 * func(n // 2, memo) + (n // 2 + 1)
    else:
        memo[n] = func(n - 1, memo) + count_ones_in_binary(n)
    return memo[n]

x, y = map(int, input().split())

print(func(x) + func(y))
