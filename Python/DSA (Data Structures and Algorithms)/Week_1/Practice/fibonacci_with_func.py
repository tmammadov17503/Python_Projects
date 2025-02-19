# def func(n):
#     if n == 0:
#         return 2
#     elif n == 1:
#         return 5
#
#     a, b = 2, 5
#     for i in range(2, n + 1):
#         a, b = b, a + b
#     return b
#
# n = int(input())
# print(func(n))

# def func(n):
#     if n == 0:
#         return 1
#     elif n == 1:
#         return 2
#
#     a, b = 1, 2
#     for i in range(2, n + 1):
#         a, b = b, a + b
#     return b
#
# n = int(input())
# print(func(n))

def fib_func(n):
    if n == 0:
        return 2
    elif n == 1:
        return 5

    a,b = 2,5
    for i in range(2,n+1):
        a,b = b,a+b
    return b

n = int(input())
print(fib_func(n))

# def fib_func(n):
#     if n == 0:
#         return 2
#     elif n == 1:
#         return 5
#
#     a,b = 2,5
#     for i in range(2,n+1):
#         a,b = b,a+b
#     return b
#
# n = int(input())
# print(fib_func(n))