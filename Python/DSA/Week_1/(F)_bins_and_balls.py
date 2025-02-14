def k(n):
    mod = 10**9 + 7
    total = 0
    total += (n* pow((n-1), n-1, mod))%mod
    return total

n = int(input())
print(k(n))