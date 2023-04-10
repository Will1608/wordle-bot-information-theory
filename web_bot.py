from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from basic_entropy_bot import BasicEntropyBot
import wordle_params

def printFriendlyClue(clues):
    for clue in clues:
        if clue == "present":
            print("_", end="")
        elif clue == "absent":
            print("X", end="")
        else:
            print("O", end="")
    print("")

browser = webdriver.Firefox()

browser.get("https://www.nytimes.com/games/wordle/index.html")

# Closing cookies pop up and instruction window
browser.find_element("id", "pz-gdpr-btn-reject").click()
browser.find_element("class name", "Modal-module_closeIcon__TcEKb").click()

# Start playing
bot = BasicEntropyBot()

for round in range(wordle_params.ROUND_COUNT):
    if round == 0:
        bot.initialise_round(is_first_round=True)
    else:
        bot.initialise_round()

    is_won = False
    print(f"Bot guessed:\n{bot.guess}")
    
    browser.find_element("css selector", "body").click()
    browser.find_element("css selector", "body").send_keys(bot.guess, Keys.ENTER)
    time.sleep(2)
    tiles = browser.find_elements("class name", "Tile-module_tile__UWEHN")

    clues = [tiles[i].get_attribute("data-state") for i in range(round * wordle_params.WORD_LENGTH, round * wordle_params.WORD_LENGTH + wordle_params.WORD_LENGTH)]
    printFriendlyClue(clues)

    if clues == ["correct"] * wordle_params.WORD_LENGTH:
        is_won = True
        break

    bot.end_round(clues)

if is_won:
    print(f"Bot Wins in {round + 1} rounds")
else:
    print("Bot lost no way a human can win today")

browser.close()
