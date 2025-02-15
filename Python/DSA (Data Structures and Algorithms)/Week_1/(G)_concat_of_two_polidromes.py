def func(n, k):
    mod = 10 ** 9 + 7
    total = 0
    for i in range(1, n):
        left_len = (i + 1) // 2
        right_len = ((n - i) + 1) // 2
        total += (pow(k, left_len, mod)) * ((pow(k, right_len, mod)) % mod)
        total %= mod
    return total


n, k = map(int, input().split())
print(func(n, k))