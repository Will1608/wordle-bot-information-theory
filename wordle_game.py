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

    def __get_correct_letter_positions(self, _list, element):
        occurences = []
        for idx, item in enumerate(_list):
            if(item == element):
                occurences.append(idx)
        return occurences

    def __case_letter_occurs_same_or_more_in_guess_and_answer(self, clue_list, guess_correct_letter_position, correct_answer_correct_letter_position):
        updated_clue_list = clue_list

        markings_to_place = len(correct_answer_correct_letter_position)
        correct_position_set = set(guess_correct_letter_position).intersection(set(correct_answer_correct_letter_position))
        if(correct_position_set):
            for position in correct_position_set:
                markings_to_place -= 1
                updated_clue_list[position] = "O"

        for position in guess_correct_letter_position:
            if not(position in correct_position_set) and markings_to_place > 0:
                markings_to_place -= 1
                updated_clue_list[position] = "_"

        return updated_clue_list
    
    def __case_letter_occurs_less_in_guess_than_answer(self, clue_list, guess_correct_letter_position, correct_answer_correct_letter_position):
        updated_clue_list = clue_list

        markings_to_place = len(guess_correct_letter_position)
        correct_position_set = set(guess_correct_letter_position).intersection(set(correct_answer_correct_letter_position))

        if(correct_position_set):
            for position in correct_position_set:
                markings_to_place -= 1
                updated_clue_list[position] = "O"

        for position in guess_correct_letter_position:
            if not(position in correct_position_set) and markings_to_place > 0:
                markings_to_place -= 1
                updated_clue_list[position] = "_"
        return updated_clue_list

    def __get_clue_from_guess(self, guess, correct_answer):
        letters_in_common = set(guess).intersection(set(correct_answer))

        clue_list = ["X", "X", "X", "X", "X"]

        for letter in letters_in_common:
            guess_correct_letter_position = self.__get_correct_letter_positions(guess, letter)
            correct_answer_correct_letter_position = self.__get_correct_letter_positions(correct_answer, letter)

            if(len(guess_correct_letter_position) >= len(correct_answer_correct_letter_position)):
                clue_list = self.__case_letter_occurs_same_or_more_in_guess_and_answer(clue_list, guess_correct_letter_position, correct_answer_correct_letter_position)
            else:
                clue_list = self.__case_letter_occurs_less_in_guess_than_answer(clue_list, guess_correct_letter_position, correct_answer_correct_letter_position)

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

            

    
