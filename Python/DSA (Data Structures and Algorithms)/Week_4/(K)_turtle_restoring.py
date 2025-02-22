import sys

def func(n, m, a):
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    path = []

    for i in range(1, n + 1):
        dp[i][1] = dp[i - 1][1] + a[i - 1][0]

    for j in range(1, m + 1):
        dp[1][j] = dp[1][j - 1] + a[0][j - 1]

    for i in range(2, n + 1):
        for j in range(2, m + 1):
            dp[i][j] = min(dp[i - 1][j], dp[i][j - 1]) + a[i - 1][j - 1]

    i, j = n, m
    while i > 1 and j > 1:
        path.append((i, j))
        if dp[i - 1][j] + a[i - 1][j - 1] == dp[i][j]:
            i -= 1
        else:
            j -= 1

    while i > 1:
        path.append((i, j))
        i -= 1

    while j > 1:
        path.append((i, j))
        j -= 1

    path.append((1, 1))
    path.reverse()

    return dp[n][m], path

n, m = map(int, input().split())
a = [list(map(int, input().split())) for _ in range(n)]

res, path = func(n, m, a)
print(res)
for x, y in path:
    print(x, y)