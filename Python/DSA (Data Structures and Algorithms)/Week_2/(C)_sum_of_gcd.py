import math

def func(n, numbers):
    total = 0
    for i in range(n):
        for j in range(i + 1, n):
            total += math.gcd(numbers[i], numbers[j])
    return total

t = int(input())
for _ in range(t):
    data = list(map(int, input().split()))
    n = data[0]
    numbers = data[1:]
    print(func(n, numbers))