# def prime(g):
#     if g < 2:
#         return False
#     for number in range(2, int(g ** 0.5) + 1):
#         if g % number == 0:
#             return False
#     return True
#
# def prime_counter(n,m):
#     count = 0
#     for num in range(n,m+1):
#         if prime(num):
#             count+=1
#     return count
#
# n,m = map(int,input().split())
# print(prime_counter(n,m))

def prime(g):
    if g < 2:
        return False
    for number in range(2, int(g**0.5)+1):
        if g % number == 0:
            return False
    return True

def counter(n,m):
    counter = 0
    for num in range(n,m+1):
        if prime(num):
            counter+=1
    return counter

n,m = map(int,input().split())
print(counter(n,m))