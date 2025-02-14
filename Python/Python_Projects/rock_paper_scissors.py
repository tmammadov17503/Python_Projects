import random
import sys

print("Welcome to Rock Paper Scissors game")
selection_first = input("What do you choose? Type 0 for Rock, 1 for Paper, or 2 for Scissors.\n")
random_bot = random.randint(0,2)

rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

if selection_first < "0" or selection_first > "2":
    print("Invalid, Please input a number between 0 and 2")
else:
    if selection_first == "0":
        print("You chose:\n" + rock)
    if selection_first == "1":
        print("You chose:\n" + paper)
    if selection_first == "2":
        print("You chose:\n" + scissors)

    if selection_first == "0":
        random_bot
        if random_bot == 0:
            print("Computer chose:\n" + rock)
        elif random_bot == 1:
            print("Computer chose:\n" + paper)
        else:
            print("Computer chose:\n" + scissors)

    if selection_first == "1":
        random_bot
        if random_bot == 0:
            print("Computer chose:\n" + rock)
        elif random_bot == 1:
            print("Computer chose:\n" + paper)
        else:
            print("Computer chose:\n" + scissors)

    if selection_first == "2":
        random_bot
        if random_bot == 0:
            print("Computer chose:\n" + rock)
        elif random_bot == 1:
            print("Computer chose:\n" + paper)
        else:
            print("Computer chose:\n" + scissors)

    if selection_first == "0" and random_bot == 2:
        print("You win")
    elif selection_first > str(random_bot):
        print("You win")
    elif selection_first < str(random_bot):
        print("You lose")
    else:
        print("Draw")


#
# import random
#
# rock = '''
#     _______
# ---'   ____)
#       (_____)
#       (_____)
#       (____)
# ---.__(___)
# '''
#
# paper = '''
#     _______
# ---'   ____)____
#           ______)
#           _______)
#          _______)
# ---.__________)
# '''
#
# scissors = '''
#     _______
# ---'   ____)____
#           ______)
#        __________)
#       (____)
# ---.__(___)
# '''
#
# game_images = [rock, paper, scissors]
#
# user_choice = int(input("What do you choose? Type 0 for Rock, 1 for Paper or 2 for Scissors.\n"))
# print(game_images[user_choice])
#
# computer_choice = random.randint(0, 2)
# print("Computer chose:")
# print(game_images[computer_choice])
#
# if user_choice >= 3 or user_choice < 0:
#   print("You typed an invalid number, you lose!")
# elif user_choice == 0 and computer_choice == 2:
#   print("You win!")
# elif computer_choice == 0 and user_choice == 2:
#   print("You lose")
# elif computer_choice > user_choice:
#   print("You lose")
# elif user_choice > computer_choice:
#   print("You win!")
# elif computer_choice == user_choice:
#   print("It's a draw")

####### Debugging challenge: #########
#Try running this code and type 5.
#It will give you an IndexError and point to line 32 as the issue.
#But on line 38 we are trying to prevent a crash by detecting
#any numbers great than or equal to 3 or less than 0.
#So what's going on?
#Can you debug the code and fix it?
#Solution: https://repl.it/@appbrewery/rock-paper-scissors-debugged-end