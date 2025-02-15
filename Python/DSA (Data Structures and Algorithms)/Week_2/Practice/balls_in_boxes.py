def func(n, m):
    return (n * pow(n-1, n-1, m)) % m

n, m = map(int, input().strip().split())

print(func(n, m))
