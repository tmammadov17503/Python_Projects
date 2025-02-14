import math

def func(a, b, c, d):
    numerator = a * d + c * b
    denominator = b * d

    gcd = math.gcd(numerator, denominator)
    numerator //= gcd
    denominator //= gcd

    if denominator == 1:
        return str(numerator)
    return f"{numerator} {denominator}"

a, b, c, d = map(int, input().split())
print(func(a, b, c, d))