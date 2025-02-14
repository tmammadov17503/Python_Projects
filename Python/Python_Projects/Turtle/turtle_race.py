from turtle import Turtle, Screen
import random

race_on = False
riad_screen = Screen()
riad_screen.setup(width=500, height=400)
start = riad_screen.textinput("What is your bet?", "Which turtle will be the first?Enter a color: ").lower()
print(start)
colors = ["red", "orange", "yellow", "green", "blue", "purple"]
y_positions = [-70, -40, -10, 20, 50, 80]
turtle_team = []

for t in range(0,6):
    riad_t = Turtle(shape="turtle")
    riad_t.color(colors[t])
    riad_t.penup()
    riad_t.goto(-230,y_positions[t])
    riad_t.pendown()
    turtle_team.append(riad_t)
    # print(riad_t)

if start:
    race_on = True

while race_on:
    for turtle in turtle_team:
        if turtle.xcor() > 230:
            race_on = False
            win_color = turtle.pencolor()
            if win_color == start:
                print(f"You've won! The {win_color} turtle is the winner!")
            else:
                print(f"You've lost! The {win_color} turtle is the winner!")

        rand_distance = random.randint(0,10)
        turtle.forward(rand_distance)








    # def movement():
    #     riad_t.forward(10)
    #
    # def back():
    #     riad_t.backward(10)
    #
    # def turn_left():
    #     # new_move = riad_t.heading()+10
    #     # riad_t.setheading(new_move)
    #     riad_t.left(10)
    # def turn_right():
    #     # new_move = riad_t.heading()-10
    #     # riad_t.setheading(new_move)
    #     riad_t.right(10)
    #
    # def clear():
    #     riad_t.clear()
    #     riad_t.penup()
    #     riad_t.home()
    #     riad_t.pendown()
    #
    # riad_screen.listen()
    # riad_screen.onkey(key="w", fun=movement)
    # riad_screen.onkey(key="s", fun=back)
    # riad_screen.onkey(key="d", fun=turn_right)
    # riad_screen.onkey(key="a", fun=turn_left)
    # riad_screen.onkey(key="c", fun=clear)
    # riad_screen.exitonclick()
