def sieve(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(limit ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False
    return is_prime


def preprocess_prime_counts(limit):
    is_prime = sieve(limit)
    prime_count = [0] * (limit + 1)

    for i in range(1, limit + 1):
        prime_count[i] = prime_count[i - 1] + (1 if is_prime[i] else 0)

    return is_prime, prime_count


def find_max_a(b, c, prime_count):
    for a in range(b, 0, -1):
        num_primes = prime_count[b] - prime_count[a - 1]
        if num_primes == c:
            return a
    return -1


b, c = map(int, input().split())
is_prime, prime_count = preprocess_prime_counts(b)
print(find_max_a(b, c, prime_count))
