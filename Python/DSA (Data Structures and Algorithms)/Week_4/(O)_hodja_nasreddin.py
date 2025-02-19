import math

MOD = 9929

def binomial(n, k, mod):
    if k > n:
        return 0
    num = math.factorial(n) % mod
    denom = (math.factorial(k) * math.factorial(n - k)) % mod
    return (num * pow(denom, -1, mod)) % mod

def func(n):
    total_ways = 0
    for x in range(1, n + 1):
        for y in range(1, n + 1):
            ways_hodja = binomial(x + y - 2, x - 1, MOD)
            ways_donkey = binomial(2 * n - x - y, n - x, MOD)
            total_ways = (total_ways + ways_hodja * ways_donkey) % MOD
    return total_ways

n = int(input().strip())
print(func(n))