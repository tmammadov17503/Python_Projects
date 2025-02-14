import time
from turtle import Screen, Turtle
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard

screen = Screen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("Pong Game")
screen.tracer(0)

r_paddle = Paddle((380,0))
l_paddle = Paddle((-390,0))
ball = Ball()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(r_paddle.go_up, "Up")
screen.onkey(r_paddle.go_down, "Down")
screen.onkey(l_paddle.go_up, "w")
screen.onkey(l_paddle.go_down, "s")

game_is_on = True
while game_is_on:
    time.sleep(ball.move_speed)
    screen.update()
    ball.move()

    #wall collision
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()

    #collision with paddle
    if ball.distance(r_paddle) < 30 and ball.xcor() > 340 or ball.distance(l_paddle) < 30 and ball.xcor() < -340:
        ball.bounce_x()

    #ball out
    if ball.xcor() > 380:
        ball.reset_position()
        scoreboard.l_point()
    elif ball.xcor() < -380:
        ball.reset_position()
        scoreboard.r_point()

screen.exitonclick()