from lib2to3.pytree import LeafPattern
from wordle_game import WordleGame
import math

def probability_of_each_letter(word_list):
    letter_occurence_ditionary = {}
    total_letters = 0

    for word in word_list:

        for letter in word:

            letter_occurence_ditionary.setdefault(letter, 0)
            letter_occurence_ditionary[letter] += 1
            total_letters += 1
    
    return { letter:occurence/total_letters for (letter, occurence) in letter_occurence_ditionary.items()}

def get_entropy_for_word(word, letter_probability_distribution):
    entropy = 0
    symbol_count = len(letter_probability_distribution)
    for letter in word:
        letter_probability = letter_probability_distribution[letter]
        entropy += letter_probability * math.log(letter_probability, symbol_count)

    return -entropy

def get_entropy_for_word_list(word_list, letter_probability_distribution):
    word_list_entropy = []
    for word in word_list:
        word_list_entropy.append(get_entropy_for_word(word, letter_probability_distribution))

    return word_list_entropy

def get_max_entopy_word(word_list):

    letter_probability_distribution = probability_of_each_letter(word_list)

    word_list_entropy = get_entropy_for_word_list(word_list, letter_probability_distribution)

    max_entropy_index = word_list_entropy.index(max(word_list_entropy))
    
    return word_list[max_entropy_index]

def update_word_list(word_list, previous_guess, known_bad_letters, known_letters, know_incorrect_position_letters, know_correct_position_letters):
    updated_word_list = []
    word_list.remove(previous_guess)
    duplicate_letter_set = set(known_bad_letters).intersection(set(known_letters))
    
    for letter in duplicate_letter_set:
        word_list = [word for word in word_list if word.count(letter) == 1]
        known_bad_letters.remove(letter)

    for word in word_list:
        word_to_keep = True

        for (letter, position) in know_correct_position_letters:
            if not(word[position] == letter):
                word_to_keep = False

        if(word_to_keep):
            for letter in known_bad_letters:
                if(letter in word):
                    word_to_keep = False
        
        if(word_to_keep):
            for (letter, position) in know_incorrect_position_letters:
                if word[position] == letter:
                    word_to_keep = False

        if(word_to_keep):
            for letter in known_letters:
                if not(letter in word):
                    word_to_keep = False
    
        if(word_to_keep):
            updated_word_list.append(word)

    return updated_word_list

test_game = WordleGame()

word_list = test_game.allowed_words

known_bad_letters = []
know_correct_position_letters = []
know_incorrect_position_letters = []
known_letters = []

print(test_game.chosen_word)
for round in range(6):
    is_won = False
    print(len(word_list))
    if(round == 0):
        round_0_word_list = [word for word in word_list if len(set(word)) == len(word)]
        guess = get_max_entopy_word(round_0_word_list)
    else:
        guess = get_max_entopy_word(word_list)
    
    clue = test_game.play_one_round(guess)

    print(f"Bot guessed : {guess}")
    print(f"Got clue {clue}")

    if(clue == "OOOOO"):
        is_won = True
        break
    
    for idx, value in enumerate(clue):
        if(value == 'X' and (guess[idx] not in known_bad_letters)):
            known_bad_letters.append(guess[idx])
        elif(value=="_" and (guess[idx] not in known_letters)):
            known_letters.append(guess[idx])
            know_incorrect_position_letters.append((guess[idx], idx))
        elif(value=="O"):
            know_correct_position_letters.append((guess[idx], idx))
            known_letters.append(guess[idx])

    word_list = update_word_list(word_list, guess, known_bad_letters, known_letters, know_incorrect_position_letters, know_correct_position_letters)

if(is_won):
    print(f"Bot won in {round + 1} rounds with {test_game.chosen_word}")
else:
    print(f"Bot lost the correct guess was {test_game.chosen_word}")


