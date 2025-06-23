from turtle import Turtle, Screen
import random

screen = Screen()
screen.setup(width=500, height=400)

def reset_game():
    screen.clearscreen()
    screen.setup(width=500, height=400)
    run_game()

def run_game():
    is_race_on = False
    user_bet = screen.textinput(title="Make your bet", prompt="Which turtle will win the race? Enter a color: ")
    colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    y_positions = [-70, -40, -10, 20, 50, 80]
    all_turtles = []

    # Create 6 turtles
    for turtle_index in range(0, len(colors)):
        new_turtle = Turtle(shape="turtle")
        new_turtle.penup()
        new_turtle.color(colors[turtle_index])
        new_turtle.goto(x=-230, y=y_positions[turtle_index])
        all_turtles.append(new_turtle)

    if user_bet:
        is_race_on = True

    while is_race_on:
        for turtle in all_turtles:
            # 230 is 250 - half the width of the turtle.
            if turtle.xcor() > 230:
                is_race_on = False
                winning_color = turtle.pencolor()
                if winning_color == user_bet:
                    print(f"You've won! The {winning_color} turtle is the winner!")
                else:
                    print(f"You've lost! The {winning_color} turtle is the winner!")

            rand_distance = random.randint(0, 10)
            turtle.forward(rand_distance)

if __name__ == "__main__":
    run_game()
    screen.onkey(reset_game, "r")
    screen.listen()
    screen.exitonclick()