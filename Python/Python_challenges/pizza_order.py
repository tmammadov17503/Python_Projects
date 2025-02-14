print("Thank you for choosing Python Pizza Deliveries!")
print("What size pizza do you want? S, M, or L")
size = input()
print("Do you want pepperoni? Y or N")
add_pepperoni = input()
print("Do you want extra cheese? Y or N")
extra_cheese = input()

total_price = 0
if size == "S":
    total_price += 15
elif size == "M":
    total_price += 20
else:
    total_price += 25

if add_pepperoni == "Y" and size == "S":
    total_price += 2
elif add_pepperoni == "Y" and size == "M" or add_pepperoni == "Y" and size == "L":
    total_price += 3
else:
    total_price += 0

if extra_cheese == "Y":
    total_price += 1
else:
    total_price += 0

print(f"Your final bill is: ${total_price}.")