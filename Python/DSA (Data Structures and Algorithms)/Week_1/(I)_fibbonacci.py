def k(n):
    if n == 0:
        return 1
    elif n == 1:
        return 1

    prev_val = 1
    curr_val = 1
    for i in range(2, n + 1):
        prev_val, curr_val = curr_val, prev_val + curr_val
    return curr_val

n = int(input())
print(k(n))