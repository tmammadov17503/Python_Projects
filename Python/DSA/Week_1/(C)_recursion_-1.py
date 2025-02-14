def k(abs_n):
    total = 0
    for i in range(1, abs_n + 1):
        total += i
    return total

    '''
    if(abs_n==0):
        return 0
    else:
        return k(abs_n-1)+ abs_n 
    '''


n = int(input())
abs_n = abs(n)
print(k(abs_n))