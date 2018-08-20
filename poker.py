""" Make poker hands
"""

import random

VALUES = "2 3 4 5 6 7 8 9 10 Jack Queen King Ace".split()
SUITS = "Spades Hearts Diamonds Clubs".split()

def test_new_deck():
    # We will test the `make_new_deck` function
    deck = make_new_deck()
    assert len(deck) == 52
    assert deck[0] == "2 of Spades"
    assert deck[13] == "2 of Hearts"
    assert deck[-1] == "Ace of Clubs"


def test_shuffled():
    decks = [make_new_deck(), make_new_deck()]
    for i in range(1, 1000):
        decks[i%2] = shuffle(decks[i%2])
        assert decks[0] != decks[1]


def shuffle(deck):
    shuffled = deck.copy()
    random.shuffle(shuffled)
    return shuffled

def make_new_deck():
    cards = []
    for suit in SUITS:
        for value in VALUES:
            cards.append(value + " of " + suit)

    return cards


if __name__ == "__main__":
    print("Running tests")
    test_new_deck()
    test_shuffled()
    print("Finished")
