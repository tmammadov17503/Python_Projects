# def func(n, memo={}):
#     if n in memo:
#         return memo[n]
#     if n == 1 or n == 2:
#         return 1
#
#     memo[n] = func(n-1, memo) + func(n-2, memo)
#     return memo[n]
#
# n = int(input().strip())
# print(func(n))

def func(n, memo={}):
    if n in memo:
        return memo[n]

    if n == 0:
        return 1
    if n == 1:
        return 2

    memo[n] = func(n-1, memo) + func(n-2, memo)
    return memo[n]

n = int(input().strip())
print(func(n))
