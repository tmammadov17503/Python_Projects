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


def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    color = (r, g, b)
    return color

def spirograph(gap_size):
    for i in range(int(360 / gap_size)):
        new_turtle.color(random_color())
        new_turtle.circle(100)
        new_turtle.setheading(new_turtle.heading() + gap_size)

spirograph(5)
new_screen.exitonclick()
