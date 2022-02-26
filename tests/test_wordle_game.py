from wordle_game import WordleGame

def test_clue_is_correct_1_correct_letter_incorrect_position_no_duplicates():
    test_guess = "abcde"
    test_word = "faghi"

    wordle_game = WordleGame()
    wordle_game.chosen_word = test_word

    expected_results = "_XXXX"
    true_results = wordle_game.play_one_round(test_guess)

    assert expected_results == true_results

def test_clue_is_correct_1_correct_letter_correct_position():
    test_guess = "abcde"
    test_word = "afgij"

    wordle_game = WordleGame()
    wordle_game.chosen_word = test_word

    expected_results = "OXXXX"
    true_results = wordle_game.play_one_round(test_guess)

    assert expected_results == true_results

def test_clue_is_correct_1_duplicate_correct_letter_incorrect_position():
    test_guess = "abade"
    test_word = "gfija"

    wordle_game = WordleGame()
    wordle_game.chosen_word = test_word

    expected_results = "_XXXX"
    true_results = wordle_game.play_one_round(test_guess)

    assert expected_results == true_results

def test_clue_is_correct_1_duplicate_correct_letter_correct_position():
    test_guess = "abade"
    test_word = "afijb"

    wordle_game = WordleGame()
    wordle_game.chosen_word = test_word

    expected_results = "OXXXX"
    true_results = wordle_game.play_one_round(test_guess)

    assert expected_results == true_results
