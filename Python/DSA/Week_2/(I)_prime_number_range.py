def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    for number in range(2, int(n ** 0.5) + 1):
        if n % number == 0:
            return False
    return True

m, n = map(int, input().strip().split())

primes_in_range = [i for i in range(m, n + 1) if is_prime(i)]

if primes_in_range:
    print("\n".join(map(str, primes_in_range)))
else:
    print("Absent")