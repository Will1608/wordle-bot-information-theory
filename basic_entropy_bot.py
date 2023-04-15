import math
import requests
import wordle_params

class BasicEntropyBot:
    def __init__(self):
        self.words = requests.get(wordle_params.WORD_LIST_URL).text.split("\n")
        self.known_absent = set()
        self.known_present = {}
        self.known_correct = [""] * wordle_params.WORD_LENGTH
        self.known_incorrect_positions = [set(), set(), set(), set(), set()]

    def initialise_round(self, is_first_round=False):
        if is_first_round:
            first_round_words = [word for word in self.words if len(set(word)) == len(word)]
            firs_round_words_entropy = self.get_words_entropy(first_round_words)
            return first_round_words[firs_round_words_entropy.index(max(firs_round_words_entropy))]
        
        self.update_words()
        words_entropy = self.get_words_entropy(self.words)
        return self.words[words_entropy.index(max(words_entropy))]


    def end_round(self, clues, guess):
        self.known_present = {}

        for index, indicator in enumerate(clues):
            if indicator == wordle_params.WORDLE_CORRECT_MARKER:
                self.known_correct[index] = guess[index]

                if self.known_present.get(guess[index], False):
                    self.known_present[guess[index]] -= 1

        for index, indicator in enumerate(clues):
            if indicator == wordle_params.WORDLE_PRESENT_MARKER:
                self.known_present .setdefault(guess[index], 0)
                self.known_present [guess[index]] += 1

                self.known_incorrect_positions[index].add(guess[index])

        for index, indicator in enumerate(clues):
            if indicator == wordle_params.WORDLE_ABSENT_MARKER and guess[index] not in self.known_present.keys() and guess[index] not in self.known_correct:
                self.known_absent.add(guess[index])

    def update_words(self):
        updated_word_list = []

        for word in self.words:
            is_word_to_keep = True
            for index, letter in enumerate(word):
                if self.known_correct[index] != "" and self.known_correct[index] != letter:
                    is_word_to_keep = False
                    break
                if letter in self.known_incorrect_positions[index]:
                    is_word_to_keep = False
                    break
                if letter in self.known_absent:
                    is_word_to_keep = False
                    break

            if is_word_to_keep:
                for letter, occurence in self.known_present.items():
                    if occurence > word.count(letter):
                        is_word_to_keep = False
                        break

            if is_word_to_keep:
                updated_word_list.append(word)
        self.words = updated_word_list

    def get_pdf(self, words):
        total_letters = 0
        pdf = [0] * 26
        for word in words:
            for letter in word:
                # 97 is a in ascii so -97 to offset to 0
                pdf[ord(letter) - 97] += 1
                total_letters += 1

        return [letter_probability / total_letters for letter_probability in pdf]

    def get_words_entropy(self, words):
        pdf = self.get_pdf(words)
        words_entropies = []
        for word in words:
            words_entropies.append(self.get_entropy_for_word(word, pdf))
        return words_entropies

    def get_entropy_for_word(self, word, pdf):
        entropy = 0

        for letter in word:
            entropy += pdf[ord(letter) - 97] * math.log(pdf[ord(letter) - 97], 26)

        return -entropy

