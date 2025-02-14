import random
from Mains import experimental_file

# print("Hello " + input("What is your name?\n"))
# hello_word = len("Hello world")
# print(hello_word)
# print("hello" [0])
# name_len = len(input("What is your name?\n"))
# print("Your name consists of " + str(name_len) + " characters")

# print(round(8 / 3 ,2))
# random_integer = random.randint(1,100)
# print(random_integer)
# random_float = random.random()
# random_1_5 = random.randint(1,5)
# print(random_float)
# print(experimental_file.pi)
# print(random_1_5)

rayons_of_baku = ["Nahchivan", "Gusar"]
rayons_of_baku.append("Susha")
rayons_of_baku.extend(["Gebele", "Surahani"])
print(rayons_of_baku)
random_rayon = random.choice(rayons_of_baku)
print(random_rayon)

print(experimental_file.pi)

#For loops
fruits = ["apple", "banana", "pear", "orange", "grape"]
for fruit in fruits:
    print(fruit)

for number in range(0,11,2):
    print(number)

#FUNCTIONS
def new_function():
    print("Hello World")
    len_hello = len("Hello World")
    print(len_hello)

new_function()

#WHILE LOOP
num = 6
while num > 0:
    #do something
    num -= 1
    print(num)

    

