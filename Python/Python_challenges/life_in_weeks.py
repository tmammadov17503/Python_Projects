age = input("How old are?\n")
max_age = 100
new_age = int(age)
left_age = max_age - new_age
weeks_left = int(left_age * 52)
print(f"You have {weeks_left} weeks left.")