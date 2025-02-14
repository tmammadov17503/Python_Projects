import turtle
import random
from turtle import Turtle, Screen
colours = ["CornflowerBlue", "DarkOrchid", "IndianRed", "DeepSkyBlue", "LightSeaGreen", "wheat", "SlateGray", "SeaGreen"]
new_turtle = Turtle()
new_turtle.shape("turtle")
new_turtle.pensize(20)
new_turtle.speed("fastest")
for i in range(4):
    new_turtle.color("green")
    new_turtle.forward(90)
    new_turtle.left(90)
new_screen = Screen()
new_screen.exitonclick()