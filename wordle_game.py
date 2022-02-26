import requests
import random
import re

WORD_LIST_URL = "https://raw.githubusercontent.com/tabatkins/wordle-list/main/words"

class WordleGame():
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

    def __get_occurence_positions(self, _list, element):
        occurences = []
        for idx, item in enumerate(_list):
            if(item == element):
                occurences.append(idx)
        return occurences

    def __get_clue_from_guess(self, guess, chosen_word):
        letters_in_common = set(guess).intersection(set(chosen_word))
        clue_list = ["X", "X", "X", "X", "X"]
        for letter in letters_in_common:
            guess_occurence_position = self.__get_occurence_positions(guess, letter)
            chosen_word_occurence_position = self.__get_occurence_positions(chosen_word, letter)

            if(len(guess_occurence_position) == len(chosen_word_occurence_position)):
                for i in range(len(guess_occurence_position)):
                    clue_list[guess_occurence_position[i]] = "_"
                    if(guess_occurence_position[i] in chosen_word_occurence_position):
                        clue_list[guess_occurence_position[i]] = "O"
            else:
                if(len(guess_occurence_position) > len(chosen_word_occurence_position)):
                    markings_to_place = len(guess_occurence_position) - len(chosen_word_occurence_position)
                else:
                    markings_to_place = len(guess_occurence_position)

                for i in range(len(guess_occurence_position)):
                    if(guess_occurence_position[i] in chosen_word_occurence_position):
                        clue_list[guess_occurence_position[i]] = "O"
                markings_to_place -= len(self.__get_occurence_positions(clue_list, "O"))

                while(markings_to_place > 0):
                    if(not(clue_list[guess_occurence_position[i]] == "O") and guess[guess_occurence_position[i]] == letter):
                            clue_list[guess_occurence_position[i]] = "_"
                            markings_to_place -= 1
        return "".join(clue_list)

    # public methods
    def play_one_round(self, guess):
        return self.__get_clue_from_guess(guess, self.chosen_word)

    def play_full_game(self):
        is_correct_guess = False

        for guess_count in range(self.total_rounds):
            self.guess = ""

            while(self.__is_guess_format_correct(self.guess)):
                self.guess = input("Enter a guess (word may be 5 long and contain only A-Z case-insensitive):").lower()
            
            self.clue_str = self.play_one_round(self.guess)

            if(self.guess == self.chosen_word):
                is_correct_guess = True
                break
            
            print(self.guess)
            print(self.clue_str)

        if(is_correct_guess):
            print(f"You found the correct word {self.chosen_word} in {guess_count + 1} tries WELL DONE!!!")
        else:
            print(f"The correct guess was {self.chosen_word}, better luck next time")

            

    
