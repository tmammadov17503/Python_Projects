def func(n):
    if n == 1:
        return 2
    elif n == 2:
        return 3

    prev2, prev1 = 2, 3
    for _ in range(3, n + 1):
        current = prev1 + prev2
        prev2, prev1 = prev1, current

    return prev1

n = int(input().strip())
print(func(n))