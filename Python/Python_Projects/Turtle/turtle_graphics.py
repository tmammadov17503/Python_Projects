import turtle
import random
from turtle import Turtle, Screen

directions = [0, 90, 180, 270]
new_turtle = Turtle()
new_screen = Screen()

new_screen.colormode(255)

new_turtle.shape("turtle")
new_turtle.pensize(2)
new_turtle.speed("fastest")
new_turtle.penup()
new_turtle.back(200)
new_turtle.right(90)
new_turtle.forward(200)
new_turtle.left(90)
new_turtle.pendown()
def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    color = (r, g, b)
    return color

def circle():
    new_turtle.color(random_color())
    for i in range(1,15):
        new_turtle.circle(i)
    new_turtle.penup()
    new_turtle.forward(50)
    new_turtle.pendown()

def movement():
    for n in range(8):
        circle()
    new_turtle.penup()
    new_turtle.back(400)
    new_turtle.left(90)
    new_turtle.forward(50)
    new_turtle.right(90)
    new_turtle.pendown()

for t in range(8):
    movement()
new_screen.exitonclick()

#OTHER SOLUTION
# import turtle as turtle_module
# import random
#
# turtle_module.colormode(255)
# tim = turtle_module.Turtle()
# tim.speed("fastest")
# tim.penup()
# tim.hideturtle()
# color_list = [(202, 164, 109), (238, 240, 245), (150, 75, 49), (223, 201, 135), (52, 93, 124), (172, 154, 40), (140, 30, 19), (133, 163, 185), (198, 91, 71), (46, 122, 86), (72, 43, 35), (145, 178, 148), (13, 99, 71), (233, 175, 164), (161, 142, 158), (105, 74, 77), (55, 46, 50), (183, 205, 171), (36, 60, 74), (18, 86, 90), (81, 148, 129), (148, 17, 20), (14, 70, 64), (30, 68, 100), (107, 127, 153), (174, 94, 97), (176, 192, 209)]
# tim.setheading(225)
# tim.forward(300)
# tim.setheading(0)
# number_of_dots = 100
#
# for dot_count in range(1, number_of_dots + 1):
#     tim.dot(20, random.choice(color_list))
#     tim.forward(50)
#
#     if dot_count % 10 == 0:
#         tim.setheading(90)
#         tim.forward(50)
#         tim.setheading(180)
#         tim.forward(500)
#         tim.setheading(0)
#
# screen = turtle_module.Screen()
# screen.exitonclick()