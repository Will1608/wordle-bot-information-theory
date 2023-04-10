import math
import requests
import wordle_params

class BasicEntropyBot:
    def __init__(self):
        self.word_list = requests.get(wordle_params.WORD_LIST_URL).text.split("\n")
        self.word_list_entropy = None
        self.pdf = [0] * 26
        self.known_absent, self.known_present = set(), set()
        self.known_correct = [""] * wordle_params.WORD_LENGTH
        self.known_incorrect_positions = [set(), set(), set(), set(), set()]
        self.guess = ""

    def initialise_round(self, is_first_round=False):
        if is_first_round:
            self.word_list = [word for word in self.word_list if len(set(word)) == len(word)]
        else:
            self.update_word_list()
        
        self.update_word_list_entropy()
        self.guess = self.word_list[self.word_list_entropy.index(max(self.word_list_entropy))]

    def end_round(self, returned_clue):
        for index, indicator in enumerate(returned_clue):
            if indicator == wordle_params.WORDLE_ABSENT_MARKER:
                self.known_absent.add(self.guess[index])
            elif indicator == wordle_params.WORDLE_CORRECT_MARKER:
                self.known_present.discard(self.guess[index])
                self.known_correct[index] = self.guess[index]

        for index, indicator in enumerate(returned_clue):
            if indicator == wordle_params.WORDLE_PRESENT_MARKER:
                self.known_present.add(self.guess[index])
                self.known_incorrect_positions[index].add(self.guess[index])

    def update_word_list(self):
        updated_word_list = []

        for word in self.word_list:
            is_word_to_keep = True

            if len(set(word).intersection(self.known_present)) == len(self.known_present): 

                for index, letter in enumerate(word):
                    if self.known_correct[index] != "":
                        if self.known_correct[index] != letter:
                            is_word_to_keep = False
                            break
                    
                    if letter in self.known_incorrect_positions[index]:
                        is_word_to_keep = False
                        break

                    if letter in self.known_absent:
                        is_word_to_keep = False
                        break

                if is_word_to_keep:
                    updated_word_list.append(word)

        self.word_list = updated_word_list

    def update_pdf(self):
        total_letters = 0

        for word in self.word_list:
            for letter in word:
                # 97 is a in ascii so -97 to offset to 0
                self.pdf[ord(letter) - 97] += 1
                total_letters += 1
        
        self.pdf = [letter_probability / total_letters for letter_probability in self.pdf]

    def update_word_list_entropy(self):
        self.update_pdf()
        self.word_list_entropy = []
        for word in self.word_list:
            self.word_list_entropy.append(self.get_entropy_for_word(word))
    
    def get_entropy_for_word(self, word):
        entropy = 0

        for letter in word:
            entropy += self.pdf[ord(letter) - 97] * math.log(self.pdf[ord(letter) - 97], 26)

        return -entropy

