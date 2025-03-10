import sys

def find_majority_element(filename):
    try:
        file = open(filename, 'r')
        k = list(map(int, file.readline().split()))
        file.close()
    except FileNotFoundError:
        print("Input file not found.")
        return

    n = len(k)
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
        print(maj)
    else:
        print(-1)

find_majority_element("majority.in.txt")
