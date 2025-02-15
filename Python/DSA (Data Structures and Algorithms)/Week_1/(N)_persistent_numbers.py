def func(n):
    total = 0
    while n >= 10:
        product = 1
        for digit in str(n):
            product *= int(digit)
        n = product
        total += 1
    return total

while True:
    try:
        line = input()
    except EOFError:
        break
    if not line:
        break
    n = int(line)
    print(func(n))