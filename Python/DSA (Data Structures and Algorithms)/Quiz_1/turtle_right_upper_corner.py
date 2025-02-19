import sys


def func(n, m, a):
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    dp[1][m] = a[0][m - 1]

    for i in range(2, n + 1):
        dp[i][m] = dp[i - 1][m] + a[i - 1][m - 1]

    for j in range(m - 1, 0, -1):
        dp[1][j] = dp[1][j + 1] + a[0][j - 1]

    for i in range(2, n + 1):
        for j in range(m - 1, 0, -1):
            dp[i][j] = min(dp[i - 1][j], dp[i][j + 1]) + a[i - 1][j - 1]

    return dp[n][1]


n, m = map(int, input().split())
a = [list(map(int, input().split())) for _ in range(n)]

print(func(n, m, a))



# # #FOR THE FILE INPUT
#import sys
# def func(n, m, a):
#     dp = [[0] * (m + 1) for _ in range(n + 1)]
#
#     dp[1][m] = a[0][m - 1]
#
#     for i in range(2, n + 1):
#         dp[i][m] = dp[i - 1][m] + a[i - 1][m - 1]
#
#     for j in range(m - 1, 0, -1):
#         dp[1][j] = dp[1][j + 1] + a[0][j - 1]
#
#     for i in range(2, n + 1):
#         for j in range(m - 1, 0, -1):
#             dp[i][j] = min(dp[i - 1][j], dp[i][j + 1]) + a[i - 1][j - 1]
#
#     return dp[n][1]
#
# with open("input(5).txt", "r") as file:
#     lines = file.readlines()
#     n, m = map(int, lines[0].split())
#     a = [list(map(int, line.split())) for line in lines[1:]]
#
# print(func(n, m, a))


# #OTHER FILE INPUT
# import sys
#
# def func(n, m, a):
#     dp = [[0] * (m + 1) for _ in range(n + 1)]
#
#     dp[1][m] = a[0][m - 1]
#
#     for i in range(2, n + 1):
#         dp[i][m] = dp[i - 1][m] + a[i - 1][m - 1]
#
#     for j in range(m - 1, 0, -1):
#         dp[1][j] = dp[1][j + 1] + a[0][j - 1]
#
#     for i in range(2, n + 1):
#         for j in range(m - 1, 0, -1):
#             dp[i][j] = max(dp[i - 1][j], dp[i][j + 1]) + a[i - 1][j - 1]
#
#     return dp[n][1]
#
#
# with open("input(4).txt", "r") as file:
#     lines = file.readlines()
#     n, m = map(int, lines[0].split())
#     a = [list(map(int, line.split())) for line in lines[1:]]
#
# print(func(n, m, a))


#NO FILE FOR OTHER
# def func(n, m, a):
#     dp = [[0] * (m + 1) for _ in range(n + 1)]
#
#     dp[1][m] = a[0][m - 1]
#
#     for i in range(2, n + 1):
#         dp[i][m] = dp[i - 1][m] + a[i - 1][m - 1]
#
#     for j in range(m - 1, 0, -1):
#         dp[1][j] = dp[1][j + 1] + a[0][j - 1]
#
#     for i in range(2, n + 1):
#         for j in range(m - 1, 0, -1):
#             dp[i][j] = max(dp[i - 1][j], dp[i][j + 1]) + a[i - 1][j - 1]
#
#     return dp[n][1]
#
#
# n, m = map(int, input().split())
# a = [list(map(int, input().split())) for _ in range(n)]
#
# print(func(n, m, a))



