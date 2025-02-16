def func(a, b, m):
    total = 0
    MOD = m
    for i in range(a, b + 1):
        total = (total + pow(i, 3, MOD)) % MOD
    return total

def product_of_nonzero_digits(a, b, m):
    total_value = func(a, b, m)

    product = 1
    for digit in str(total_value):
        if digit != '0':
            product *= int(digit)
    return product

a, b, m = map(int, input().split())
print(product_of_nonzero_digits(a, b, m))