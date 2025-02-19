def sum_digits(x):
    s = 0
    while x > 0:
        s += x % 10
        x //= 10
    return s

def sieve(n):
    arr = [True]*(n+1)
    arr[0] = arr[1] = False
    for i in range(2, int(n**0.5)+1):
        if arr[i]:
            for j in range(i*i, n+1, i):
                arr[j] = False
    return arr

n, m = map(int, input().split())
pr = sieve(n)
ans = 0
for i in range(2, n+1):
    if pr[i]:
        f = i
    else:
        f = sum_digits(i)
    ans = (ans + pow(i, f, m))%m
print(ans)