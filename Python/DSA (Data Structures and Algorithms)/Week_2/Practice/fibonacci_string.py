def func(n):
    if n == 0:
        return "a"
    elif n == 1:
        return "b"
    else:
        return func(n - 1) + func(n - 2)

n = int(input().strip())
result = func(n)
print(result.count("b"))
