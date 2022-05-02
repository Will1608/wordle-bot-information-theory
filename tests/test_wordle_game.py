from wordle_game import WordleGame

def test_clue_is_correct_duplicate_in_guess_and_word_with_1_correct_position():
    test_guess = "madam"
    test_word = "alarm"

    wordle_game = WordleGame()
    wordle_game.chosen_word = test_word

    expected_results = "_XOXX"
    true_results = wordle_game.play_one_round(test_guess)

    assert expected_results == true_results
