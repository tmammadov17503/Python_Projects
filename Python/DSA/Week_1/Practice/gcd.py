def gcd_func(a,b):
    while b:
        a,b = b, a%b
    return a

a,b = map(int,input().split())
print(gcd_func(a,b))