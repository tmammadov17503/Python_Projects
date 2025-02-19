import math

def func(n, m):
    dp = [0] * (n + 1)
    dp[0] = 1

    for i in range(1, n + 1):
        val_1 = math.floor(i - math.sqrt(i))
        val_2 = math.floor(math.log(i)) if i > 1 else 0
        val_3 = math.floor(i * (math.sin(i) ** 2))
        dp[i] = (dp[val_1] + dp[val_2] + dp[val_3]) % m

    return dp[n]

n, m = map(int, input().split())

print(func(n, m))