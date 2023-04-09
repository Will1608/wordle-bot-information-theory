from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from wordle_game import WordleGame
import entropy_calculator

bot_brain = WordleGame(total_rounds=6)

known_bad_letters = []
known_correct_position_letters = []
known_incorrect_position_letters = []
known_letters = []

def dataStateToGameState(dataState):
    if dataState == "present":
        return "_"
    if dataState == "absent":
        return "X"
    return "O"

browser = webdriver.Firefox()

browser.get("https://www.nytimes.com/games/wordle/index.html")

# Closing cookies pop up and instruction window
browser.find_element("id", "pz-gdpr-btn-reject").click()
browser.find_element("class name", "Modal-module_closeIcon__TcEKb").click()

# Start playing
word_list = [word for word in bot_brain.allowed_words if len(set(word)) == len(word)]
for round in range(6):
    is_won = True
    guess =  entropy_calculator.get_max_entopy_word(word_list)
    print(f"Bot guessed:\n{guess}")

    browser.find_element("css selector", "body").click()
    browser.find_element("css selector", "body").send_keys(guess, Keys.ENTER)
    time.sleep(2)
    tiles = browser.find_elements("class name", "Tile-module_tile__UWEHN")

    for i in range(round * 5, round * 5 + 5):
        letter_clue = dataStateToGameState(tiles[i].get_attribute("data-state"))

        if(letter_clue == 'X' and (guess[i % 5] not in known_bad_letters)):
            known_bad_letters.append(guess[i % 5])
        elif(letter_clue=="_" and (guess[i % 5] not in known_letters)):
            known_letters.append(guess[i % 5])
            known_incorrect_position_letters.append((guess[i % 5], i % 5))
        elif(letter_clue=="O"):
            known_correct_position_letters.append((guess[i % 5], i % 5))
            known_letters.append(guess[i % 5])

        if letter_clue != "O":
            is_won = False
        print(letter_clue, end="")

    print("")
    word_list = entropy_calculator.update_word_list(word_list, known_bad_letters, known_letters, known_incorrect_position_letters, known_correct_position_letters)

    if is_won:
        break

if is_won:
    print(f"Bot Wins in {round + 1} rounds")
else:
    print("Bot lost no way a human can win today")

browser.close()
