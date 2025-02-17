import sys
import functools

sys.setrecursionlimit(10000)

@functools.lru_cache(maxsize=None)
def calc(n, p, q):
    if n == 0:
        return 1
    return calc(n // p, p, q) + calc(n // q, p, q)

def main():
    n, p, q = map(int, sys.stdin.readline().split())
    result = calc(n, p, q)
    print(result)

if __name__ == "__main__":
    main()