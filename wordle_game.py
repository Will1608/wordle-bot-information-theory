import requests
import random
import re

WORD_LIST_URL = "https://raw.githubusercontent.com/tabatkins/wordle-list/main/words"

class WorldGame():
    def __init__(self, total_rounds=6):
        self.allowed_words = self.__get_allowed_word_list()
        self.chosen_word = self.__choose_word(self.allowed_words)
        self.total_rounds = total_rounds
        self.round_count = 0

    # private methods
    def __get_allowed_word_list(self):
        return requests.get(WORD_LIST_URL).text.split("\n")

    def __choose_word(self, word_list):
        return random.choice(word_list)

    def __is_letter_correct(self,letter, chosen_word):
        return letter in chosen_word

    def __is_letter_in_correct_position(self, index, guess, chosen_word):
        return guess[index] == chosen_word[index]

    # public methods
    def play_full_game(self):
        guess = ""
        clue_str = "XXXXX"
        is_correct_guess = False
        for guess_count in range(self.total_rounds):
            while(not(re.search(r'^[a-z]{5}$', guess, re.IGNORECASE) and (guess in self.allowed_words))):
                guess = input("Enter a guess (word my be 5 long and contain only A-Z case-insensitive):")
            
            guess = guess.lower()
            clue_list = list(clue_str)
            for i in range(5):

                guess_letter_check_output = "X"

                if(self.__is_letter_correct(guess[i], self.chosen_word)):
                    guess_letter_check_output = "_"

                if(guess_letter_check_output == "_" and self.__is_letter_in_correct_position(i, guess, self.chosen_word)):
                    guess_letter_check_output = "O"
                
                clue_list[i] = guess_letter_check_output

            clue_str = "".join(clue_list)

            print(guess)
            print(clue_str)

            if(guess == self.chosen_word):
                is_correct_guess = True
                break

            guess = ""
            clue_str = "XXXXX"

        if(is_correct_guess):
            print(f"You guess the correct word {self.chosen_word} in {guess_count + 1} tries WELL DONE!!!")
        else:
            print(f"the correct guess was {self.chosen_word}, better luck next time")

            

    
