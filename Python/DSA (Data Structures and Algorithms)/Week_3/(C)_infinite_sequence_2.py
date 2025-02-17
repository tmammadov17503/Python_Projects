import sys
from functools import lru_cache

sys.setrecursionlimit(10 ** 7)


def main():
    data = sys.stdin.read().split()
    n, p, q, x, y = map(int, data)

    @lru_cache(maxsize=None)
    def f(n):
        if n <= 0:
            return 1
        return f(n // p - x) + f(n // q - y)

    print(f(n))


if __name__ == '__main__':
    main()
