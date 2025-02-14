import turtle
import random
from turtle import Turtle, Screen

directions = [0, 90, 180, 270]
new_turtle = Turtle()
new_screen = Screen()

new_screen.colormode(255)

new_turtle.shape("turtle")
new_turtle.pensize(20)
new_turtle.speed("fastest")

def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    random_color = (r, g, b)
    return random_color

for i in range(200):
    new_turtle.forward(30)
    new_turtle.color(random_color())
    new_turtle.setheading(random.choice(directions))

new_screen.exitonclick()
