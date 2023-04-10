import requests
from basic_entropy_bot import BasicEntropyBot
import wordle_params
from wordle_game import WordleGame
from utils import printFriendlyClue

word_list = requests.get(wordle_params.WORD_LIST_URL).text.split("\n")

# basic entropy bot
for word in word_list:
    bot = BasicEntropyBot()
    game = WordleGame(word)
    for i in range(wordle_params.ROUND_COUNT):
        if i == 0:
            bot.initialise_round(is_first_round=True)
        else:
            bot.initialise_round()
        
        clues = game.play_one_round(bot.guess)
        bot.end_round(clues)
        print(word)
        print(bot.guess)
        printFriendlyClue(clues)
    break

