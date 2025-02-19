import sys

def func(n, arr):
    if n == 0:
        return 0
    if n == 1:
        return arr[0]

    res = [0] * (n + 1)
    res[1] = arr[0]

    if n > 1:
        res[2] = max(arr[0], arr[1])

    for i in range(3, n + 1):
        res[i] = max(res[i - 2] + arr[i - 1], res[i - 1])

    return res[n]

n = int(input().strip())
arr = list(map(int, input().split()))

print(func(n, arr))