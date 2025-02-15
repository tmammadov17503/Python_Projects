import math

def count_points_on_line(x1, y1, x2, y2):
    return math.gcd(abs(x2 - x1), abs(y2 - y1)) + 1

def func(x1, y1, x2, y2, x3, y3):
    perimeter_points = (
        count_points_on_line(x1, y1, x2, y2) +
        count_points_on_line(x2, y2, x3, y3) +
        count_points_on_line(x3, y3, x1, y1) - 3
    )
    return perimeter_points

x1, y1, x2, y2, x3, y3 = map(int, input().strip().split())

print(func(x1, y1, x2, y2, x3, y3))
