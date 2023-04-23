import requests
import wordle_params

class PositionEntropyBot:
    def __init__(self):
        self.words = requests.get(wordle_params.WORD_LIST_URL).text.split("\n")
        self.known_absent = set()
        self.known_present = {}
        self.known_correct = [""] * wordle_params.WORD_LENGTH
        self.known_incorrect_positions = [set(), set(), set(), set(), set()]
        self.letter_to_occurence_grade = self.initialise_letter_to_occurence_struct()

    def initialise_round(self, is_first_round=False):
        if is_first_round:
            first_round_words = [word for word in self.words if len(set(word)) == len(word)]
            words_grades = self.get_words_grade(first_round_words)
            return first_round_words[words_grades.index(min(words_grades))]

        self.update_words()

        words_grades = self.get_words_grade(self.words)
        return self.words[words_grades.index(min(words_grades))]



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

    def get_pos_pdf(self, words):
        pos_pdf = []

        for i in range(wordle_params.WORD_LENGTH):
            total_letters = 0
            current_pdf = [0] * 26
            for word in words:
                current_pdf[ord(word[i]) - 97] += 1
                total_letters += 1

            pos_pdf.append([letter_probability / total_letters for letter_probability in current_pdf])

        return pos_pdf

    def get_words_grade(self, words):
        words_grade = []
        for word in words:
            grades = []
            for i, letter in enumerate(word):
                grades.append(self.letter_to_occurence_grade[i][ord(letter) - 97])
            words_grade.append(sum(grades)/wordle_params.WORD_LENGTH)
        return words_grade

    def initialise_letter_to_occurence_struct(self):
        letter_to_occurence_struct = []
        pos_pdf = self.get_pos_pdf(self.words)
        for pdf in pos_pdf:
            letter_to_occurence_struct.append(sorted(range(len(pdf)),key=pdf.__getitem__, reverse=True))

        return letter_to_occurence_struct
