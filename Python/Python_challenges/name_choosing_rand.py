import random
names = ["Tom", "John", "Smith"]

num_items = len(names)
print(num_items)
random_choice = random.randint(0, num_items - 1)
print(names[random_choice])