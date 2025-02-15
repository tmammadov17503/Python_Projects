def func(n):
    res = 1
    i = 2

    while i * i <= n:
        if n % i == 0:
            c = 0
            while n % i == 0:
                n //= i
                c += 1
            res *= (c + 1)
        i += 1

    if n > 1:
        res *= 2

    return res - 2

n = int(input().strip())
print(func(n))