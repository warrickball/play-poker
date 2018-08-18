""" Make poker hands
"""

import random
from collections import Counter

VALUES = '2 3 4 5 6 7 8 9 10 Jack Queen King Ace'.split()
SUITS = 'Hearts Diamonds Clubs Spades'.split()


def make_new_deck():
    cards = []
    for suit in SUITS:
        for value in VALUES:
            card = value + ' of ' + suit
            cards.append(card)
    return cards


def test_new_deck():
    # We will test the `make_new_deck` function
    deck = make_new_deck()
    assert len(deck) == 52
    first_card = deck[0]
    assert first_card == "2 of Hearts"
    assert deck[12] == "Ace of Hearts"
    assert deck[13] == "2 of Diamonds"
    assert deck[26] == "2 of Clubs"
    assert deck[51] == "Ace of Spades"


def shuffled(deck):
    # A proper shuffle function
    re_ordered = deck.copy()
    random.shuffle(re_ordered)
    return re_ordered


def test_shuffled():
    decks = []
    # Put an ordered deck into the list of decks
    decks.append(make_new_deck())
    for i in range(1000):
        deck = make_new_deck()
        shuffled_deck = shuffled(deck)
        # Compare this deck to all previous ones.  Do any match?
        assert shuffled_deck not in decks
        decks.append(shuffled_deck)


def make_hand():
    return shuffled(make_new_deck())[:5]


def test_hands():
    hands = []
    sames = 0
    for i in range(1000):
        hand = make_hand()
        assert len(hand) == 5
        # Compare this deck to all previous ones.  Do any match?
        if hand in hands:
            sames += 1
        hands.append(hand)
    # Same hand will occur very rarely
    expected_prop = 1 / (52 * 51 * 50 * 49 * 48)
    assert sames / len(hands) < expected_prop * 5


def suit(card):
    return card.split()[2]


def test_suit():
    assert suit('2 of Spades') == 'Spades'
    assert suit('King of Clubs') == 'Clubs'
    assert suit('Ace of Diamonds') == 'Diamonds'
    assert suit('10 of Hearts') == 'Hearts'


def value(card):
    return card.split()[0]


def test_value():
    assert value('2 of Spades') == '2'
    assert value('King of Clubs') == 'King'
    assert value('Ace of Diamonds') == 'Ace'
    assert value('10 of Hearts') == '10'


def rank(card):
    return VALUES.index(value(card))


def test_rank():
    assert rank('2 of Spades') == 0
    assert rank('King of Clubs') == 11
    assert rank('Ace of Diamonds') == 12
    assert rank('10 of Hearts') == 8
    assert rank('Jack of Hearts') == 9


def is_flush(hand):
    suits = [suit(card) for card in hand]
    return len(set(suits)) == 1


def test_flush():
    assert is_flush(['2 of Hearts',
                     'King of Hearts',
                     'Ace of Hearts',
                     '10 of Hearts',
                     '5 of Hearts'])
    assert not is_flush(['2 of Hearts',
                         'King of Hearts',
                         'Ace of Spades',
                         '10 of Hearts',
                         '5 of Hearts'])
    assert not is_flush(['2 of Hearts',
                         'King of Hearts',
                         'Ace of Hearts',
                         '10 of Hearts',
                         '5 of Clubs'])


def is_straight(hand):
    ranks = [rank(card) for card in hand]
    min_rank = min(ranks)
    diff_from_min = [r - min_rank for r in ranks]
    return sorted(diff_from_min) == list(range(len(hand)))


def test_straight():
    assert is_straight(['2 of Spades',
                        '6 of Hearts',
                        '3 of Spades',
                        '4 of Clubs',
                        '5 of Hearts'])
    assert is_straight(['10 of Spades',
                        'Ace of Hearts',
                        'Queen of Spades',
                        'Jack of Clubs',
                        'King of Hearts'])
    assert not is_straight(['2 of Spades',
                            '6 of Hearts',
                            '7 of Spades',
                            '4 of Clubs',
                            '5 of Hearts'])
    assert not is_straight(['10 of Spades',
                            'Ace of Hearts',
                            'Jack of Spades',
                            'Jack of Clubs',
                            'King of Hearts'])


def is_straight_flush(hand):
    return is_straight(hand) and is_flush(hand)


def test_straight_flush():
    assert is_straight_flush(['2 of Hearts',
                              '6 of Hearts',
                              '3 of Hearts',
                              '4 of Hearts',
                              '5 of Hearts'])
    assert is_straight_flush(['10 of Spades',
                              'Ace of Spades',
                              'Queen of Spades',
                              'Jack of Spades',
                              'King of Spades'])
    assert not is_straight_flush(['2 of Hearts',
                                  '6 of Hearts',
                                  '3 of Hearts',
                                  '4 of Clubs',
                                  '5 of Hearts'])
    assert not is_straight_flush(['2 of Spades',
                                  '6 of Spades',
                                  '7 of Spades',
                                  '4 of Spades',
                                  '5 of Spades'])
    assert not is_straight_flush(['10 of Spades',
                                  'Ace of Spades',
                                  'Jack of Spades',
                                  'Jack of Spades',
                                  'King of Spades'])


def cmp_ranks(first_hand, second_hand):
    first_ranks = sorted(rank(card) for card in first_hand)
    second_ranks = sorted(rank(card) for card in second_hand)
    for first, second in zip(first_ranks, second_ranks):
        if first == second:
            continue
        return 1 if first > second else -1
    return 0


def test_cmp_ranks():
    hand1 = ['2 of Spades',
             '6 of Spades',
             'Queen of Spades',
             '7 of Spades',
             '5 of Spades']
    hand2 = ['2 of Spades',
             '6 of Spades',
             'Jack of Spades',
             '7 of Spades',
             '5 of Spades']
    assert cmp_ranks(hand1, hand2) == 1
    assert cmp_ranks(hand2, hand1) == -1
    assert cmp_ranks(hand1, hand1) == 0
    assert cmp_ranks(hand2, hand2) == 0
    # Suit doesn't matter
    hand3 = ['2 of Hearts',
             '6 of Clubs',
             'Queen of Spades',
             '7 of Spades',
             '5 of Spades']
    assert cmp_ranks(hand1, hand3) == 0


def value_counts(hand):
    values = [value(card) for card in hand]
    return sorted(Counter(values).values())


def test_value_counts():
    hand1 = ['2 of Spades',
             '6 of Spades',
             'Queen of Spades',
             '7 of Spades',
             '5 of Spades']
    assert value_counts(hand1) == [1] * 5
    assert value_counts(['2 of Spades',
                         '6 of Hearts',
                         'Queen of Clubs',
                         '7 of Hearts',
                         '5 of Spades']) == [1] * 5
    assert value_counts(['2 of Spades',
                         '2 of Hearts',
                         'Queen of Clubs',
                         'Queen of Hearts',
                         '5 of Spades']) == [1, 2, 2]
    assert value_counts(['4 of Spades',
                         '2 of Hearts',
                         'Queen of Clubs',
                         'Queen of Hearts',
                         'Queen of Spades']) == [1, 1, 3]


def hand_rank(hand):
    flush = is_flush(hand)
    straight = is_straight(hand)
    if straight and flush:
        return 8
    counts = value_counts(hand)
    if 4 in counts:
        return 7
    if counts == [2, 3]:  # full house
        return 6
    if flush:
        return 5
    if straight:
        return 4
    if 3 in counts:  # three of a kind
        return 3
    if counts == [1, 2, 2]:  # two pairs
        return 2
    if 2 in counts:
        return 1
    return 0


def test_hand_rank():
    # Nothing
    assert hand_rank(['2 of Spades',
                      '6 of Spades',
                      'Queen of Spades',
                      '7 of Spades',
                      '5 of Hearts']) == 0
    # One pair
    assert hand_rank(['2 of Spades',
                      '2 of Hearts',
                      'Queen of Spades',
                      '7 of Spades',
                      '5 of Hearts']) == 1
    # Two pairs
    assert hand_rank(['2 of Spades',
                      '2 of Hearts',
                      'Queen of Spades',
                      'Queen of Diamonds',
                      '5 of Hearts']) == 2
    # Three of a kind
    assert hand_rank(['Queen of Hearts',
                      '2 of Hearts',
                      'Queen of Spades',
                      'Queen of Diamonds',
                      '3 of Spades']) == 3
    # Straight
    assert hand_rank(['2 of Spades',
                      '6 of Clubs',
                      '5 of Spades',
                      '3 of Spades',
                      '4 of Spades']) == 4
    # Flush
    assert hand_rank(['2 of Spades',
                      '10 of Spades',
                      '5 of Spades',
                      '3 of Spades',
                      '4 of Spades']) == 5
    # Full house
    assert hand_rank(['Queen of Hearts',
                      '2 of Hearts',
                      'Queen of Spades',
                      'Queen of Diamonds',
                      '2 of Spades']) == 6
    # Four of a kind
    assert hand_rank(['2 of Spades',
                      '2 of Hearts',
                      '5 of Spades',
                      '2 of Clubs',
                      '2 of Diamonds']) == 7
    # Straight flush
    assert hand_rank(['2 of Spades',
                      '6 of Spades',
                      '5 of Spades',
                      '3 of Spades',
                      '4 of Spades']) == 8


def cmp_hand(first, second):
    first_hr = hand_rank(first)
    second_hr = hand_rank(second)
    if first_hr == second_hr:
        return cmp_ranks(first, second)
    return 1 if first_hr > second_hr else -1



def check_two_hands(first, second, betters):
    assert cmp_hand(first, second) == -1
    for better in betters:
        for worse in (first, second):
            assert cmp_hand(worse, worse) == 0
            assert cmp_hand(better, worse) == 1
            assert cmp_hand(worse, better) == -1


def test_cmp_hand():
    sf1 = ['2 of Spades',
           '6 of Spades',
           '5 of Spades',
           '3 of Spades',
           '4 of Spades']
    sf2 = ['3 of Spades',
           '7 of Spades',
           '6 of Spades',
           '4 of Spades',
           '5 of Spades']
    check_two_hands(sf1, sf2, [])
    betters = [sf1, sf2]
    four1 = ['2 of Spades',
             '2 of Hearts',
             '5 of Spades',
             '2 of Clubs',
             '2 of Diamonds']
    four2 = ['3 of Spades',
             '3 of Hearts',
             '5 of Spades',
             '3 of Clubs',
             '3 of Diamonds']
    check_two_hands(four1, four2, betters)
    betters += [four1, four2]
    fh1 = ['2 of Spades',
           '2 of Hearts',
           '5 of Spades',
           '5 of Clubs',
           '2 of Diamonds']
    fh2 = ['2 of Spades',
           '2 of Hearts',
           '5 of Spades',
           '5 of Clubs',
           '5 of Diamonds']
    check_two_hands(fh1, fh2, betters)
    betters += [fh1, fh2]
    f1 = ['3 of Spades',
          '7 of Spades',
          'Ace of Spades',
          'Jack of Spades',
          '10 of Spades']
    f2 = ['3 of Spades',
          '7 of Spades',
          'Ace of Spades',
          'Queen of Spades',
          '10 of Spades']
    check_two_hands(f1, f2, betters)
    betters += [f1, f2]
    s1 = ['3 of Spades',
          '7 of Hearts',
          '6 of Clubs',
          '4 of Spades',
          '5 of Spades']
    s2 = ['5 of Spades',
          '8 of Hearts',
          '9 of Clubs',
          '6 of Spades',
          '7 of Spades']
    check_two_hands(s1, s2, betters)
    betters += [s1, s2]
    tok1 = ['2 of Spades',
            '2 of Hearts',
            '5 of Spades',
            '6 of Clubs',
            '2 of Diamonds']
    tok2 = ['2 of Spades',
            '2 of Hearts',
            '5 of Spades',
            '7 of Clubs',
            '2 of Diamonds']
    check_two_hands(tok1, tok2, betters)
    betters += [tok1, tok2]
    tp1 = ['2 of Spades',
           '2 of Hearts',
           '5 of Spades',
           '6 of Clubs',
           '5 of Diamonds']
    tp2 = ['2 of Spades',
           '2 of Hearts',
           '5 of Spades',
           '7 of Clubs',
           '5 of Diamonds']
    check_two_hands(tp1, tp2, betters)
    betters += [tp1, tp2]
    betters += [tok1, tok2]
    p1 = ['2 of Spades',
          '10 of Hearts',
          '5 of Spades',
          '6 of Clubs',
          '5 of Diamonds']
    p2 = ['2 of Spades',
          'Queen of Hearts',
          '5 of Spades',
          '7 of Clubs',
          '5 of Diamonds']
    check_two_hands(p1, p2, betters)
    betters += [p1, p2]
    zero1 = ['2 of Spades',
             '3 of Hearts',
             '5 of Spades',
             'Jack of Clubs',
             'King of Diamonds']
    zero2 = ['2 of Spades',
             '3 of Hearts',
             '6 of Spades',
             'Queen of Clubs',
             'King of Diamonds']
    check_two_hands(zero1, zero2, betters)


if __name__ == "__main__":
    print("Running tests")
    test_new_deck()
    test_shuffled()
    test_hands()
    test_suit()
    test_flush()
    test_value()
    test_rank()
    test_straight()
    test_straight_flush()
    test_cmp_ranks()
    test_value_counts()
    test_hand_rank()
    test_cmp_hand()
    print("Finished")
