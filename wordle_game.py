import requests
import random
import re
import wordle_params

WORD_LIST_URL = "https://raw.githubusercontent.com/tabatkins/wordle-list/main/words"

class WordleGame():
    def __init__(self, chosen_word):
        self.allowed_words = self.__get_allowed_word_list()
        self.chosen_word = chosen_word
        self.total_rounds = wordle_params.ROUND_COUNT
        self.guess = None
        self.clue_str = None

    # private methods
    def __get_allowed_word_list(self):
        return requests.get(WORD_LIST_URL).text.split("\n")

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
                updated_clue_list[position] = wordle_params.WORDLE_CORRECT_MARKER

        for position in guess_correct_letter_position:
            if not(position in correct_position_set) and markings_to_place > 0:
                markings_to_place -= 1
                updated_clue_list[position] = wordle_params.WORDLE_PRESENT_MARKER

        return updated_clue_list
    
    def __case_letter_occurs_less_in_guess_than_answer(self, clue_list, guess_correct_letter_position, correct_answer_correct_letter_position):
        updated_clue_list = clue_list

        markings_to_place = len(guess_correct_letter_position)
        correct_position_set = set(guess_correct_letter_position).intersection(set(correct_answer_correct_letter_position))

        if(correct_position_set):
            for position in correct_position_set:
                markings_to_place -= 1
                updated_clue_list[position] = wordle_params.WORDLE_CORRECT_MARKER

        for position in guess_correct_letter_position:
            if not(position in correct_position_set) and markings_to_place > 0:
                markings_to_place -= 1
                updated_clue_list[position] = wordle_params.WORDLE_PRESENT_MARKER
        return updated_clue_list

    def __get_clue_from_guess(self, guess, correct_answer):
        letters_in_common = set(guess).intersection(set(correct_answer))

        clues = [wordle_params.WORDLE_ABSENT_MARKER] * wordle_params.WORD_LENGTH

        for letter in letters_in_common:
            guess_correct_letter_position = self.__get_correct_letter_positions(guess, letter)
            correct_answer_correct_letter_position = self.__get_correct_letter_positions(correct_answer, letter)

            if(len(guess_correct_letter_position) >= len(correct_answer_correct_letter_position)):
                clues = self.__case_letter_occurs_same_or_more_in_guess_and_answer(clues, guess_correct_letter_position, correct_answer_correct_letter_position)
            else:
                clues = self.__case_letter_occurs_less_in_guess_than_answer(clues, guess_correct_letter_position, correct_answer_correct_letter_position)

        return clues

    # public methods
    def play_one_round(self, guess):
        return self.__get_clue_from_guess(guess, self.chosen_word)
