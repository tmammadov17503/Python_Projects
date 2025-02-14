def count_min_sum_digits(m, n):
    min_sum = 10000
    min_numbers = []

    for num in range(m, n + 1):
        sum_of_digits = sum(int(digit) for digit in str(num))
        if sum_of_digits < min_sum:
            min_sum = sum_of_digits
            min_numbers = [num]
        elif sum_of_digits == min_sum:
            min_numbers.append(num)

    return len(min_numbers)

m, n = map(int, input().split())
print(count_min_sum_digits(m, n)) 