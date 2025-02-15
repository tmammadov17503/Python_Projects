def func(n, k):
    if n == k:
        return 1
    elif k == 0:
        return 1
    return func(n - 1, k - 1) + func(n - 1, k)

n, k = map(int, input().split())
print(func(n,k))