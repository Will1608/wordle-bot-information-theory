import requests
import random
import re

def is_letter_correct(letter, chosen_word):
    return letter in chosen_word

def is_letter_in_correct_position(index, guess, chosen_word):
    return guess[index] == chosen_word[index]
    
wordle_word_list_url = "https://raw.githubusercontent.com/tabatkins/wordle-list/main/words"
wordle_word_list = requests.get(wordle_word_list_url).text.split("\n")

chosen_word = random.choice(wordle_word_list)

guess = ""
clue_str = "XXXXX"
is_correct_guess = False
for guess_count in range(6):
    while(not(re.search(r'^[a-z]{5}$', guess, re.IGNORECASE) and (guess in wordle_word_list))):
        guess = input("Enter a guess (word my be 5 long and contain only A-Z):")
    
    guess = guess.lower()

    clue_list = list(clue_str)
    for i in range(5):

        guess_letter_check_output = "X"

        if(is_letter_correct(guess[i], chosen_word)):
            guess_letter_check_output = "_"

        if(guess_letter_check_output == "_" and is_letter_in_correct_position(i, guess, chosen_word)):
            guess_letter_check_output = "O"
        
        clue_list[i] = guess_letter_check_output

    clue_str = "".join(clue_list)

    print(guess)
    print(clue_str)

    if(guess == chosen_word):
        is_correct_guess = True
        break

    guess = ""
    clue_str = "XXXXX"

if(is_correct_guess):
    print(f"You guess the correct word {chosen_word} in {guess_count} tries WELL DONE!!!")
else:
    print(f"the correct guess was {chosen_word}, better luck next time")
