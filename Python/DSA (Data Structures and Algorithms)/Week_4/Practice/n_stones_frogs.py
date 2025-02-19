import sys

def frog_jump(n, h):
    dp = [0] * n
    dp[1] = abs(h[1] - h[0])

    for i in range(2, n):
        dp[i] = min(dp[i - 1] + abs(h[i] - h[i - 1]), dp[i - 2] + abs(h[i] - h[i - 2]))

    return dp[n - 1]

with open("input(27).txt", "r") as f:
    n = int(f.readline().strip())
    h = list(map(int, f.readline().split()))

print(frog_jump(n, h))