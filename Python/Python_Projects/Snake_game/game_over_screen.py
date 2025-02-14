from turtle import Turtle

class Game_Over(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.write(f"GAME OVER", align= 'center', font=("Courier", 24, "normal"))
        self.hideturtle()
