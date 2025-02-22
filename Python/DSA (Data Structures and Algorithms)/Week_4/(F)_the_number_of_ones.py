def func():
    n = int(input())
    dp = [0] * (n + 1)
    dp[1] = 1
    for num in range(2, n + 1):
        best = float("inf")
        for i in range(1, num // 2 + 1):
            best = min(best, dp[i] + dp[num - i])
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                best = min(best, dp[i] + dp[num // i])
        dp[num] = best
    print(dp[n])

if __name__ == '__main__':
    func()