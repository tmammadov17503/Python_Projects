import random

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


print("Welcome to the Python Password Generator")
lenght_final = int(input("How many letters would you like in your password?\n"))
symbols_final = int(input("How many symbols would you like?\n"))
numbers_final = int(input("How many numbers would you like?\n"))

final_password = []
for l in range(0, lenght_final + 1):
    final_password.append(random.choice(letters))

for s in range(0, symbols_final + 1):
    final_password.append(random.choice(symbols))

for n in range(0, numbers_final + 1):
    final_password.append(random.choice(numbers))

random.shuffle(final_password) #for LISTS only random.shuffle

password_str = ""
for char in final_password:
    password_str += char
print(f'Here is the password: {password_str}')