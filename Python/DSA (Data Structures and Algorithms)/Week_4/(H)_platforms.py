def func():
    n = int(input())
    h = list(map(int, input().split()))
    dp = [0] * n
    par = [-1] * n
    dp[0] = 0
    dp[1] = abs(h[1] - h[0])
    par[1] = 0
    for i in range(2, n):
        c1 = dp[i - 1] + abs(h[i] - h[i - 1])
        c2 = dp[i - 2] + 3 * abs(h[i] - h[i - 2])
        if c1 <= c2:
            dp[i] = c1
            par[i] = i - 1
        else:
            dp[i] = c2
            par[i] = i - 2
    path = []
    i = n - 1
    while i != -1:
        path.append(i + 1)
        i = par[i]
    path.reverse()
    print(dp[n - 1])
    print(len(path))
    print(" ".join(map(str, path)))

if __name__ == '__main__':
    func()