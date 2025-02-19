def func(n, p):
    dp = [0] * n
    dp[n - 1] = p[n - 1]

    for i in range(n - 2, -1, -1):
        dp[i] = max(p[i], dp[i + 1])

    res = 0
    for i in range(n):
        res += dp[i] - p[i]

    return res

n = int(input().strip())
p = list(map(int, input().split()))
print(func(n, p))