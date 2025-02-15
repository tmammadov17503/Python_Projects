def func(n):
    factors = []

    power = 0
    while n % 2 == 0:
        power += 1
        n //= 2
    if power > 0:
        factors.append(f"2^{power}" if power > 1 else "2")

    for i in range(3, int(n ** 0.5) + 1, 2):
        power = 0
        while n % i == 0:
            power += 1
            n //= i
        if power > 0:
            factors.append(f"{i}^{power}" if power > 1 else f"{i}")

    if n > 1:
        factors.append(str(n))

    print("*".join(factors))


n = int(input().strip())
func(n)