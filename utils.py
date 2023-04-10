def printFriendlyClue(clues):
    for clue in clues:
        if clue == "present":
            print("_", end="")
        elif clue == "absent":
            print("X", end="")
        else:
            print("O", end="")
    print("")