def func():
    import sys
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    mod = 10**9 + 7
    dp = [0] * (n + 1)
    dp[0] = 1
    if n >= 1:
        dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = (dp[i - 1] + (i - 1) * dp[i - 2]) % mod
    sys.stdout.write(str(dp[n]))

if __name__ == '__main__':
    func()