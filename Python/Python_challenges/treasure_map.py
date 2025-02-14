line1 = ["⬜️","️⬜️","️⬜️"]
line2 = ["⬜️","⬜️","️⬜️"]
line3 = ["⬜️️","⬜️️","⬜️️"]
map = [line1, line2, line3]
print("Hiding your treasure! X marks the spot.")
position = input()

A = position.count("A")
B = position.count("B")
C = position.count("C")

one = sum(1 for position in position if '1' in position)
two = sum(2 for position in position if '2' in position)
three = sum(3 for position in position if '3' in position)

if A == 1 and one == 1:
  map[0][0] = "X"
if A == 1 and two == 2:
  map[1][0] = "X"
if A == 1 and three == 3:
  map[2][0] = "X"

if B == 1 and one == 1:
  map[0][1] = "X"
if B == 1 and two == 2:
  map[1][1] = "X"
if B == 1 and three == 3:
  map[2][1] = "X"

if C == 1 and one == 1:
  map[0][2] = "X"
if C == 1 and two == 2:
  map[1][2] = "X"
if C == 1 and three == 3:
  map[2][2] = "X"

print(f"{line1}\n{line2}\n{line3}")


# Alternative method for solving this:
# line1 = ["⬜️","️⬜️","️⬜️"]
# line2 = ["⬜️","⬜️","️⬜️"]
# line3 = ["⬜️️","⬜️️","⬜️️"]
# map = [line1, line2, line3]
# print("Hiding your treasure! X marks the spot.")
# position = input() # Where do you want to put the treasure?
# # Your code below
# letter = position[0].lower()
# abc = ["a", "b", "c"]
# letter_index = abc.index(letter)
# number_index = int(position[1]) - 1
# map[number_index][letter_index] = "X"
#
# print(f"{line1}\n{line2}\n{line3}")