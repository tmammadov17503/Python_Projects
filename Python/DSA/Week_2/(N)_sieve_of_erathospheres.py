def func(limit):
    primes = [True] * (limit + 1)
    primes[0] = primes[1] = False

    for i in range(2, int(limit**0.5) + 1):
        if primes[i]:
            for j in range(i * i, limit + 1, i):
                primes[j] = False

    return primes

MAX = 100001
primes = func(MAX)

a, b = map(int, input().strip().split())
primes_in_range = [str(i) for i in range(a, b + 1) if primes[i]]
print(" ".join(primes_in_range))