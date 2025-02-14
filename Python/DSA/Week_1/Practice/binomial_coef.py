import math

def binomial_coefficient(n, k):
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))

n, k = map(int, input().split())

print(binomial_coefficient(n, k))


# def factorial(n):
#     result = 1
#     for i in range(2, n + 1):
#         result *= i
#     return result
# 
# def binomial_coefficient(n, k):
#     return factorial(n) // (factorial(k) * factorial(n - k))
#
# n, k = map(int, input().split())
#
# print(binomial_coefficient(n, k))


# import math
# def binom_func(n,k):
#     result= 0
#     result = math.factorial(n) // math.factorial(k) * math.factoial(n-k)
#     return result
#
# n,k = map(int,input().split())
# print(binom_func(n,k))

# def bin_func(n):
#     result =1
#     for i in range(2,n+1):
#         result *= i
#     return result
#
# def binom(n,k):
#     return bin_func(n) // (bin_func(k) * bin_func(n-k))
#
# n,k = map(int,input().split())
# print(binom(n,k))