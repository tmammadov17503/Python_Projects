def prime(n):
    if n == 1:
        return "No"
    if n == 2:
        return "Yes"
    if n < 2:
        return "No"

    for number in range(2, int(n**0.5)+1):
        if n % number == 0:
            return "No"
    return "Yes"

n = int(input().strip())
print (prime(n))