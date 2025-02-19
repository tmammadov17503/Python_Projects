import sys
import functools

sys.setrecursionlimit(10000)

@functools.lru_cache(maxsize=None)
def func(p):
    if p == 0:
        return 0
    t = p % 10
    return ((t * (t + 1)) // 2) + (45 * (p // 10)) + func(p // 10)

p = int(input())
print(func(p))
