def count_ways(m, n):
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    dp[m][1] = 1
    for j in range(1, n + 1):
        for i in range(m, 0, -1):
            if i == m and j == 1:
                continue
            ways = 0
            if i + 1 <= m:
                ways += dp[i + 1][j]
            if j - 1 >= 1:
                ways += dp[i][j - 1]
            if i + 1 <= m and j - 1 >= 1:
                ways += dp[i + 1][j - 1]
            dp[i][j] = ways
    return dp[1][n]

m, n = map(int, input().split())
print(count_ways(m, n))
