import requests
from basic_entropy_bot import BasicEntropyBot
from position_entropy_bot import PositionEntropyBot
import wordle_params
from wordle_game import WordleGame
import wordle_params

words = requests.get(wordle_params.WORD_LIST_URL).text.split("\n")

correct_words, incorrect_words = [], []
correct_rounds = 0
print(f"Running test for Basic entropy bot")
for round, word in enumerate(words):
    bot = PositionEntropyBot() # replace this with the bot to test
    game = WordleGame(word)
    bot_won = False
    for i in range(wordle_params.ROUND_COUNT):
        if i == 0:
            guess = bot.initialise_round(is_first_round=True)
        else:
            guess = bot.initialise_round()
        
        clues = game.play_one_round(guess)

        if clues == [wordle_params.WORDLE_CORRECT_MARKER] * 5:
            bot_won = True
            break

        bot.end_round(clues, guess)
    if bot_won:
        correct_words.append(word)
        correct_rounds += i + 1
    else:
        incorrect_words.append(word)

print(len(correct_words) / (len(correct_words) + len(incorrect_words)))
print(correct_rounds/(len(correct_words)))