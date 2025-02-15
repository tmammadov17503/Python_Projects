def func(a,b,c):
    result = pow(a,b,c)
    return result

a,b,c = map(int,input().split())
print(func(a,b,c))