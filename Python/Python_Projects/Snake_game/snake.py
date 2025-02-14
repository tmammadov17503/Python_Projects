from turtle import Screen
from snake_helper import Snake
import time
from snake_food import Food
from snake_scoreboard import Scoreboard
from game_over_screen import Game_Over

screen = Screen()
screen.setup(700,700)
screen.bgcolor("black")
screen.title("Welcome to a Snake game")
screen.tracer(0)

snake = Snake()
food = Food()
scoreboard = Scoreboard()
#game_over = Game_Over()

screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(0.1)
    snake.move()

    #Distance checker
    if snake.head.distance(food) < 15:
        print("Hopla, got ya")
        food.refreshed_location()
        snake.extend()
        scoreboard.increase_score()

    #Wall collision
    if snake.head.xcor() > 340 or snake.head.xcor() < -340 or snake.head.ycor() > 340 or snake.head.ycor() < -340:
        game_is_on = False
        Game_Over()

    #Tail collisition
    for segment in snake.segments:
        if segment == snake.head:
            pass
        elif snake.head.distance(segment) < 10:
            game_is_on = False
            Game_Over()

screen.exitonclick()



# sn_1 = Turtle("square")
# sn_1.color("white")
#
# sn_2 = Turtle("square")
# sn_2.color("white")
# sn_2.goto(-20,0)
#
# sn_3 = Turtle("square")
# sn_3.color("white")
# sn_3.goto(-40,0)