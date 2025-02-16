import sys
sys.set_int_max_str_digits(70000)
n = int(input())

if n == 1:
    print(1)
elif n == 2:
    print(2)
else:
    fib1, fib2 = 1, 2
    for number in range(3, n + 1):
        cur = fib1 + fib2
        fib1, fib2 = fib2, cur
    print(fib2)