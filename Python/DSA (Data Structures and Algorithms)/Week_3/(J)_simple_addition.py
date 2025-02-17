import sys

def last_nonzero(n):
    if n == 0:
        return 0
    while n % 10 == 0:
        n //= 10
    return n % 10

def sum_F(N):
    if N < 0:
        return 0
    if N < 10:
        return N * (N + 1) // 2
    A, r = divmod(N, 10)
    return sum_F(A - 1) + 45 * A + last_nonzero(A) + (r * (r + 1) // 2)

def main():
    for line in sys.stdin:
        p, q = map(int, line.split())
        if p < 0 and q < 0:
            break
        result = sum_F(q) - sum_F(p - 1)
        print(result)

if __name__ == '__main__':
    main()