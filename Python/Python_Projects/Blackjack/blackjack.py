import random
import logo
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

print(logo.logo)
cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

def deal_card():
    random_card = random.choice(cards)
    return random_card

def calculate_score(cards):
    score = sum(cards)
    if score == 21 and len(cards) == 2:
        return 0
    if 11 in cards and score > 21:
        cards.remove(11) and cards.append(1)
    return score

def compare(user_score, comp_score):
    if user_score == comp_score:
        return 'Draw'
    elif comp_score == 0:
        return 'You lose, computer has blackjack'
    elif user_score == 0:
        return 'You win, you have blackjack'
    elif user_score > 21:
        return 'You lose, you went over the limit'
    elif comp_score > 21:
        return 'You win, computer went over the limit'
    elif user_score > comp_score:
        return 'You win, you have more than computer'
    else:
        return 'You lose, you have less than computer'

def play_game():

    rand_user_cards = []
    rand_comp_cards = []

    for i in range(2):
        rand_user_cards.append(deal_card())
        rand_comp_cards.append(deal_card())

    game_over = True
    while game_over == True:
        user_score = calculate_score(rand_user_cards)
        comp_score = calculate_score(rand_comp_cards)
        print(f"Your cards are {rand_user_cards}, current score is {user_score}")
        print(f"Computer's fist card is {rand_comp_cards[0]}")

        if user_score == 0 or comp_score == 0 or user_score > 21:
            game_over = False
        else:
            continue_rand = input("Type 'y' to get another card or type 'n' to pass:\n")
            if continue_rand == 'y':
                rand_user_cards.append(deal_card())
            else:
                game_over = False

    while comp_score != 0 and comp_score < 17:
        rand_comp_cards.append(deal_card())
        comp_score = calculate_score(rand_comp_cards)

    print(f"Your final card is {rand_user_cards}, your final score is {user_score}")
    print(f"Computer's final hand is {rand_comp_cards}, computer's final score is {comp_score}")
    print(compare(user_score, comp_score))
    print("Thanks for playing!")

while input("Do you want to play a game of Blackjack? Type 'y' or 'n':\n") == "y":
    clear_console()
    play_game()
