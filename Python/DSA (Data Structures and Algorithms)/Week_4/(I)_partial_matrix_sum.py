import sys

def func(n, m, a):
    s = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            s[i][j] = s[i][j - 1] + s[i - 1][j] - s[i - 1][j - 1] + a[i - 1][j - 1]

    for i in range(1, n + 1):
        print(" ".join(map(str, s[i][1:])))

n, m = map(int, input().split())
a = [list(map(int, input().split())) for _ in range(n)]

func(n, m, a)