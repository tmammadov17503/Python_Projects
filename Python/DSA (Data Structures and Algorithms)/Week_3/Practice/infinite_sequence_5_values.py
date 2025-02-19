import sys
import functools

sys.setrecursionlimit(10000)

@functools.lru_cache(maxsize=None)
def calc(n, p, q, x, y):
    if n <= 0:
        return 1
    if n >= 1:
        return calc((n // p)-x, p, q, x, y) + calc((n // q) - y, p, q, x, y)

def main():
    n, p, q, x, y= map(int, sys.stdin.readline().split())
    result = calc(n, p, q, x, y)
    print(result)

if __name__ == "__main__":
    main()





# import sys
# import functools
#
# sys.setrecursionlimit(10000)
#
# @functools.lru_cache(maxsize=None)
# def calc(n, p, q, x, y):
#     if n <= 0:
#         return 1
#     left_index = max((n // p) - x, 0)
#     right_index = max((n // q) - y, 0)
#     return calc(left_index, p, q, x, y) + calc(right_index, p, q, x, y)
#
# def main():
#     n, p, q, x, y = map(int, input().split())
#     print(calc(n, p, q, x, y))
#
# if __name__ == "__main__":
#     main()
