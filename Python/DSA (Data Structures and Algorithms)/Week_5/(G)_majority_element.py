import sys

def func(n, k):
    maj = None
    cnt = 0

    for num in k:
        if cnt == 0:
            maj = num
            cnt = 1
        elif num == maj:
            cnt += 1
        else:
            cnt -= 1

    if k.count(maj) > n // 2:
        return maj
    return -1

n = int(input().strip())
k = list(map(int, sys.stdin.readline().split()))
print(func(n, k))