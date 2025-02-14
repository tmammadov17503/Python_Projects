import turtle
import random
from turtle import Turtle, Screen
colours = ["CornflowerBlue", "DarkOrchid", "IndianRed", "DeepSkyBlue", "LightSeaGreen", "wheat", "SlateGray", "SeaGreen"]
directions = [0, 90, 180, 270]
new_turtle = Turtle()
new_turtle.shape("turtle")
new_turtle.pensize(20)
new_turtle.speed("fastest")
for i in range(200):
    new_turtle.forward(30)
    new_turtle.color(random.choice(colours))
    new_turtle.setheading(random.choice(directions))

new_screen = Screen()
new_screen.exitonclick()
