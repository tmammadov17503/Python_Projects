import turtle
import random
from turtle import Turtle, Screen
colours = ["CornflowerBlue", "DarkOrchid", "IndianRed", "DeepSkyBlue", "LightSeaGreen", "wheat", "SlateGray", "SeaGreen"]
new_turtle = Turtle()
new_turtle.shape("turtle")
new_turtle.pensize(20)
new_turtle.speed("fastest")
for i in range(3):
    new_turtle.color("red")
    new_turtle.forward(100)
    new_turtle.right(120)

for i in range(4):
    new_turtle.color("green")
    new_turtle.forward(100)
    new_turtle.right(90)

for i in range(5):
    new_turtle.color("blue")
    new_turtle.forward(100)
    new_turtle.right(72)

for i in range(6):
    new_turtle.color("orange")
    new_turtle.forward(100)
    new_turtle.right(60)

for i in range(8):
    new_turtle.color("pink")
    new_turtle.forward(100)
    new_turtle.right(45)

new_screen = Screen()
new_screen.exitonclick()

#SECOND SOLUTION
# colours = ["CornflowerBlue", "DarkOrchid", "IndianRed", "DeepSkyBlue", "LightSeaGreen", "wheat", "SlateGray", "SeaGreen"]
#
# def draw_shape(num_sides):
#     angle = 360 / num_sides
#     for _ in range(num_sides):
#         tim.forward(100)
#         tim.right(angle)
#
# for shape_side_n in range(3, 10):
#     tim.color(random.choice(colours))
#     draw_shape(shape_side_n)
