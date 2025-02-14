import random
import logo_for_hangman
import stages_for_hangman
import word_list_hangman

print(logo_for_hangman.logo)
print('Welcome to Hangman game!')

lives = 6

random_word = random.choice(word_list_hangman.word_list)

empty_list = []
length = len(random_word)
for position in random_word:
    empty_list += "_"

print(empty_list)

finish = True

while finish:
    first_letter = input("Guess a letter: ").lower()

    if first_letter in empty_list:
        print("You have already guessed this letter, try another letter")

    for position in range(length):
        if random_word[position] == first_letter:
            empty_list[position] = first_letter
            print("You guessed " + first_letter + " that's in the word")

    if first_letter not in empty_list:
        print("You guessed " + first_letter + " that's not in the word. You lose a life.")
        lives -= 1
        if lives == 0:
            finish = False
            print("You Lost.")

    print(empty_list)

    if "_" not in empty_list:
        finish = False
        print("Congratulations! You Won.")

    print(stages_for_hangman.stages[lives])

print("The word guessed was: " + random_word)