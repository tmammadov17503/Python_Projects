import turtle
from prettytable import PrettyTable
# from turtle import Turtle, Screen
# timmy = Turtle()
# print(timmy)
# timmy.shape("turtle")
# timmy.color("green")
# timmy.forward(100)
# for i in range(3):
#     timmy.left(90)
#     timmy.forward(100)
#
# my_screen = Screen()
# print(my_screen.canvheight)
# my_screen.exitonclick()

table = PrettyTable()
table.add_column("Nazu Names", ["Meymun", "Abobus", "Abulfas", "Nazuuuu"])
table.add_column("Responsibilities of Nazu", ["Sleep", "Annoy Brother", "Drink", "Pretend to Study"])
table.align = "c" #give you center right or left positions
print(table)