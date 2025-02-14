import LogoAndVS
import random
import GameData
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def formatted_data(account):
    account_name = account["name"]
    account_desc = account["description"]
    account_country = account["country"]
    return f"{account_name}, a {account_desc}, from {account_country}"


attempts = 3
print("Welcome to Higher Lower game")
print(LogoAndVS.logo)


def game():
    global attempts
    while attempts > 0:
        random_data_1 = random.choice(GameData.data)
        random_data_2 = random.choice(GameData.data)
        while random_data_1 == random_data_2:
            random_data_2 = random.choice(GameData.data)

        follower_count_1 = random_data_1["follower_count"]
        follower_count_2 = random_data_2["follower_count"]
        print("Compare A: " + formatted_data(random_data_1))
        print(LogoAndVS.vs)
        print(f"Compare B: {formatted_data(random_data_2)}\n")
        followers_check = input("Who has more followers? A or B: ").lower()

        if followers_check == 'a':
            if follower_count_1 > follower_count_2:
                print("You were right")
                print(
                    f"{random_data_1['name']} has {random_data_1['follower_count']} thousand followers and {random_data_2['name']} has {random_data_2['follower_count']} thousand followers.\n")
            else:
                attempts -= 1
                print(f"You were wrong, you have {attempts} attempts left")
                print(
                    f"{random_data_1['name']} has {random_data_1['follower_count']} thousand followers and {random_data_2['name']} has {random_data_2['follower_count']} thousand followers.\n")

        if followers_check == 'b':
            if follower_count_2 > follower_count_1:
                print("You were right")
                print(
                    f"{random_data_1['name']} has {random_data_1['follower_count']} thousand followers and {random_data_2['name']} has {random_data_2['follower_count']} thousand followers.\n")
            else:
                attempts -= 1
                print(f"You were wrong, you have {attempts} attempts left")
                print(
                    f"{random_data_1['name']} has {random_data_1['follower_count']} thousand followers and {random_data_2['name']} has {random_data_2['follower_count']} thousand followers.\n")


while True:
    game()
    if attempts == 0:
        print("Thanks for playing!")
        game_again = input("Do you want to play again? Type 'Yes' or 'No' to continue: ").lower()
        if game_again == 'no':
            print("Bye Bye")
            break
        elif game_again == 'yes':
            attempts = 3
            clear_console()




# OTHER SOLUTION
# from game_data import data
# import random
# from art import logo, vs
# from replit import clear
#
#
# def get_random_account():
#     """Get data from random account"""
#     return random.choice(data)
#
#
# def format_data(account):
#     """Format account into printable format: name, description and country"""
#     name = account["name"]
#     description = account["description"]
#     country = account["country"]
#     # print(f'{name}: {account["follower_count"]}')
#     return f"{name}, a {description}, from {country}"
#
#
# def check_answer(guess, a_followers, b_followers):
#     """Checks followers against user's guess
#     and returns True if they got it right.
#     Or False if they got it wrong."""
#     if a_followers > b_followers:
#         return guess == "a"
#     else:
#         return guess == "b"
#
#
# def game():
#     print(logo)
#     score = 0
#     game_should_continue = True
#     account_a = get_random_account()
#     account_b = get_random_account()
#
#     while game_should_continue:
#         account_a = account_b
#         account_b = get_random_account()
#
#         while account_a == account_b:
#             account_b = get_random_account()
#
#         print(f"Compare A: {format_data(account_a)}.")
#         print(vs)
#         print(f"Against B: {format_data(account_b)}.")
#
#         guess = input("Who has more followers? Type 'A' or 'B': ").lower()
#         a_follower_count = account_a["follower_count"]
#         b_follower_count = account_b["follower_count"]
#         is_correct = check_answer(guess, a_follower_count, b_follower_count)
#
#         clear()
#         print(logo)
#         if is_correct:
#             score += 1
#             print(f"You're right! Current score: {score}.")
#         else:
#             game_should_continue = False
#             print(f"Sorry, that's wrong. Final score: {score}")
#
#
# game()
#
# '''
#
# FAQ: Why does choice B always become choice A in every round, even when A had more followers?
#
# Suppose you just started the game and you are comparing the followers of A - Instagram (364k) to B - Selena Gomez (174k). Instagram has more followers, so choice A is correct. However, the subsequent comparison should be between Selena Gomez (the new A) and someone else. The reason is that everything in our list has fewer followers than Instagram. If we were to keep Instagram as part of the comparison (as choice A) then Instagram would stay there for the rest of the game. This would be quite boring. By swapping choice B for A each round, we avoid a situation where the number of followers of choice A keeps going up over the course of the game. Hope that makes sense :-)
#
# '''
#
# # Generate a random account from the game data.
#
# # Format account data into printable format.
#
# # Ask user for a guess.
#
# # Check if user is correct.
# ## Get follower count.
# ## If Statement
#
# # Feedback.
#
# # Score Keeping.
#
# # Make game repeatable.
#
# # Make B become the next A.
#
# # Add art.
#
# # Clear screen between rounds.
