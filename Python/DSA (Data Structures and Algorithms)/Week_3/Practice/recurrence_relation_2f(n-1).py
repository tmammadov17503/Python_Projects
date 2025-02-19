# def func(n,memo = {}):
#     if n in memo:
#         return memo[n]
#     if n == 0:
#         return 0
#     if n == 1:
#         return 3
#
#     memo[n] = 3*(func(n-1, memo)) - 1
#     return memo[n]
#
# n = int(input())
# print(func(n))

import functools

@functools.lru_cache(maxsize=None)
def func(n):
    if n == 0:
        return 1
    if n == 1:
        return 3
    return 2 * func(n - 1) + sum(func(i) for i in range(n - 1)) + 1

n = int(input())

print(func(n))
