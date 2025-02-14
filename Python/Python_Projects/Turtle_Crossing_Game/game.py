import time
from turtle import Screen
from turtle_player import Player
from cars_on_road import CarManager
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

tutle = Player()
new_cars = CarManager()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(tutle.go_up, "Up")
screen.onkey(tutle.go_down, "Down")

game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()

    new_cars.create_cars()
    new_cars.move_cars()

    #collision
    for car in new_cars.cars:
        if car.distance(tutle) < 20:
            game_is_on = False
            scoreboard.game_over()

    #successful cross
    if tutle.is_at_finish_line():
        tutle.start()
        new_cars.level_up()
        scoreboard.increase_level()

screen.exitonclick()