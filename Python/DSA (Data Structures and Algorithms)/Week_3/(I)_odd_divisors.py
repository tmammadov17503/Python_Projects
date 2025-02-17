import sys

def func(n):
    result = 0
    while n > 0:
        k = (n+1) // 2
        result += k*k
        n //= 2
    return result

val_input = sys.stdin.read().split()

for line in val_input:
    n = int(line)
    print(func(n))