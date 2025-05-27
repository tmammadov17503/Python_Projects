# def sum_of_digits(num):
#     return sum(int(digit) for digit in str(num))
#
# numbers = list(map(int, input().split()))
#
# numbers.sort(key=lambda x: sum_of_digits(x))
#
# result = 0
# mod_value = 122345
#
# for i, num in enumerate(numbers, 1):
#     result = (result + pow(num, i, mod_value)) % mod_value
#
# print(result)

# WITH FILE HANDLING
def sum_of_digits(num):
    return sum(int(digit) for digit in str(num))

with open('input (2).txt', 'r') as file:
    numbers = list(map(int, file.readline().split()))

numbers.sort(key=lambda x: sum_of_digits(x))

result = 0
mod_value = 122345

for i, num in enumerate(numbers, 1):
    result = (result + pow(num, i, mod_value)) % mod_value

print(result)

