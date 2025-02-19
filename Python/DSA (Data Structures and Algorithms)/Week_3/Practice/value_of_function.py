# def func(n, memo={}):
#     if n in memo:
#         return memo[n]
#     if n == 1:
#         return 1
#     if n == 2:
#         return 2
#     memo[n] = func(n - 1, memo) + func(n-2, memo) + 1
#     return memo[n]
#
# n = int(input())
# print(func(n))

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