import requests
import random
import re

WORD_LIST_URL = "https://raw.githubusercontent.com/tabatkins/wordle-list/main/words"

class WorldGame():
    def __init__(self, total_rounds=6):
        self.allowed_words = self.__get_allowed_word_list()
        self.chosen_word = self.__choose_word(self.allowed_words)
        self.total_rounds = total_rounds
        self.guess = None
        self.clue_str = None
        self.is_guess_correct = False

    # private methods
    def __get_allowed_word_list(self):
        return requests.get(WORD_LIST_URL).text.split("\n")

    def __choose_word(self, word_list):
        return random.choice(word_list)

    def __is_guess_format_correct(self, guess):
        return not(re.search(r'^[a-z]{5}$', guess, re.IGNORECASE) and (guess in self.allowed_words))

    def __is_letter_correct(self, letter, chosen_word):
        return letter in chosen_word

    def __is_letter_in_correct_position_clue(self, index, guess, chosen_word):
        return guess[index] == chosen_word[index]

    def __get_clue_for_given_index(self, index, guess, chosen_word):
        clue = "X"

        if(self.__is_letter_correct(guess[index], chosen_word)):
            clue = "_"

            if(self.__is_letter_in_correct_position_clue(index, guess, chosen_word)):
                clue = "O"
                
        return clue

    def __get_clue_from_guess(self, guess, chosen_word):
        clue_list = []

        for i in range(5):
            clue_list.append(self.__get_clue_for_given_index(i, guess, chosen_word))
        return "".join(clue_list)

    # public methods
    def play_full_game(self):
        is_correct_guess = False
        print(self.chosen_word)
        for guess_count in range(self.total_rounds):
            self.guess = ""

            while(self.__is_guess_format_correct(self.guess)):
                self.guess = input("Enter a guess (word my be 5 long and contain only A-Z case-insensitive):").lower()
            
            self.clue_str = self.__get_clue_from_guess(self.guess, self.chosen_word)

            print(self.guess)
            print(self.clue_str)

            if(self.guess == self.chosen_word):
                is_correct_guess = True
                break

        if(is_correct_guess):
            print(f"You found the correct word {self.chosen_word} in {guess_count + 1} tries WELL DONE!!!")
        else:
            print(f"The correct guess was {self.chosen_word}, better luck next time")

            

    
