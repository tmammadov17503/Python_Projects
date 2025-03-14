from turtle import Turtle
import random

random_colors = ['blue', 'red', 'green', 'pink', 'orange', 'purple']
class Food(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len= 0.5, stretch_wid= 0.5)
        self.speed("fastest")
        self.refreshed_location()

    def refreshed_location(self):
        random_x = random.randint(-280, 280)
        random_y = random.randint(-280, 280)
        self.goto(random_x, random_y)
        self.color(random.choice(random_colors))

