def func():
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()
    if n == 2:
        print(a[1] - a[0])
        return
    if n == 3:
        print(a[2] - a[0])
        return
    dp = [0] * (n + 1)
    dp[2] = a[1] - a[0]
    dp[3] = a[2] - a[0]

    for i in range(4, n + 1):
        dp[i] = min(dp[i - 2], dp[i - 1]) + (a[i - 1] - a[i - 2])
    print(dp[n])

if __name__ == '__main__':
    func()