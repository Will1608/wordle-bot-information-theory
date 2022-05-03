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

def get_max_entopy_word(word_list_entropy, word_list):
    max_entropy_index = word_list_entropy.index(max(word_list_entropy))
    
    return word_list[max_entropy_index]

test_game = WordleGame()

word_list = test_game.allowed_words

updated_word_list = []
known_letters_not_in_word = ['r','s','o','n','d','p', 't', 'g', 'm', 'i', 'c']
know_correct_position_letters_in_word = {'e': 2, 'a':3}
known_letters_in_word = ['l']
known_letters_in_word.extend(know_correct_position_letters_in_word.keys())

for word in word_list:

    word_to_keep = True

    for letter in known_letters_in_word:
        if not(letter in word):
            word_to_keep = False

    if(word_to_keep):
        for letter, position in know_correct_position_letters_in_word.items():
            if not(word[position] == letter):
                word_to_keep = False

    if(word_to_keep):
        for letter in known_letters_not_in_word:
            if(letter in word):
                word_to_keep = False

    if(word_to_keep):
        updated_word_list.append(word)

word_list = updated_word_list
word_list = [word for word in word_list if len(set(word)) == len(word)]

letter_probability_distribution = probability_of_each_letter(word_list)
word_list_entropy = get_entropy_for_word_list(word_list, letter_probability_distribution)
print(get_max_entopy_word(word_list_entropy, word_list))


