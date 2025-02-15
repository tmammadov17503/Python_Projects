def powers(n,m):
    total = 0
    for i in range (1,100):
        total += ((pow((i+1),n,m) * i)%m)
        total %= m
    return total + 1

n, m = map(int, input().split())
print(powers(n,m))