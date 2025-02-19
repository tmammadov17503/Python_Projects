def smallest_prime_factor(n):
    if n % 2 == 0:
        return 2
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return i
    return n

def count_divisors(n):
    count = 0
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            count += 1
            if i != n // i:
                count += 1
    return count

def compute_sum(n, m):
    S = 0
    for i in range(2, n + 1):
        f_i = smallest_prime_factor(i)
        d_i = count_divisors(i)
        S = (S + pow(d_i, f_i, m)) % m
    return S

n, m = map(int, input().split())
print(compute_sum(n, m))