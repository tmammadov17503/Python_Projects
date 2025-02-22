import sys

def func(n, m, a):
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    dp[1][1] = a[0][0]

    for i in range(2, n + 1):
        dp[i][1] = dp[i - 1][1] + a[i - 1][0]

    for j in range(2, m + 1):
        dp[1][j] = dp[1][j - 1] + a[0][j - 1]

    for i in range(2, n + 1):
        for j in range(2, m + 1):
            dp[i][j] = min(dp[i - 1][j], dp[i][j - 1]) + a[i - 1][j - 1]

    return dp[n][m]

n, m = map(int, input().split())
a = [list(map(int, input().split())) for _ in range(n)]

print(func(n, m, a))