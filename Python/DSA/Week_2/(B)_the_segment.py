import math
def func(x1, y1, x2, y2):
    gcd_value = math.gcd(abs(x2 - x1), abs(y2 - y1))
    return gcd_value + 1

x1, y1, x2, y2 = map(int, input().split())
print(func(x1, y1, x2, y2))