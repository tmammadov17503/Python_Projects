# def lcm(a,b):
#     result = max(a, b)
#     while True:
#         if result % a == 0 and result % b == 0:
#             return result
#         result += 1
#
# a,b = map(int,input().split())
# print(lcm(a,b))

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return (a * b) // gcd(a, b)

a,b = map(int,input().split())
print(lcm(a,b))
