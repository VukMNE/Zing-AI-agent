from main import count_points_from, create_deck
from card import Card

def heuristic(cards_on_table, my_cards, treshold, cards_already_played, deck):
    '''
    Heuristic function that evaluate how good each card (currently in hands) is.
    :param cards_on_table: Cards currently on the table
    :param my_cards:
    :param treshold: Some value for deciding if point in cards_on_table are high enough
    :return: list of scores for every card in my_cards
    '''

    #First we set all scores to 0
    scores = [0 for i in range(len(my_cards))]


    #check for same card, if you have same card, always throw it.
    if len(cards_on_table) != 0:
        has_same_card, index = check_for_same_card(my_cards, cards_on_table[0])
        if has_same_card:
            scores[index] = 1
            return scores

    #check if you have J
    has_J, index = check_for_same_card(my_cards, Card(11,'J', None))
    if has_J:
        if count_points_from(cards_on_table) > treshold:
            #cards on the table have many points
            #TODO
            pass
        else:
            #card have a small amount of points so spending J is not a good choice if you have other options
            #TODO
            pass

    # EMPTY DECK
    # if the deck is empty, we should now know the last cards our opponent has
    if len(deck) == 0:
        opponents_cards = get_opponents_cards(cards_already_played + cards_on_table + my_cards)

        # if there are no cards on the table, we should NOT throw a card that our opponent has, because that would get zing for him
        has_same_card, indexes = check_for_same_cards(my_cards, opponents_cards)
        if has_same_card:
            # we set scores of others cards to a little more
            scores = [score + 1 for score in scores]
            for i in indexes:
                scores[i] = 0  # the same card to zero score (or maybe just decrease current value?)

    return scores



def check_for_same_card(my_cards, card):
    '''
    Checks if we have the same value of a card in my_cards.
    :param my_cards: Cards in hand
    :param card: Card we want to check
    :return: True if we have the same card, otherwise False and index of a card found (-1 if False)
    '''
    has_same_card = False
    index = -1
    for i,card in enumerate(my_cards):
        if card.number == card.number:
            has_same_card = True
            index = i
            break
    return has_same_card, index

def check_for_same_cards(my_cards, cards):
    '''
    Same as check_for_same_card, just allowing multiple
    :param my_cards: Cards in hand
    :param card: List of cards we want to check
    :return: True if we have the same card, otherwise False and list of indexes of a cards found (-1 if False)
    '''
    has_same_cards = False
    indexes = []
    for i,card in enumerate(my_cards):
        for c in cards:
            if card.number == c.number:
                has_same_cards = True
                indexes.append(i)
                break
    return has_same_cards, indexes

def get_opponents_cards(cards_already_used):
    '''
    Calculates the opponents cards from cards that we have already seen. If the deck is empty, this ARE exactly the opponents cards.
    :param cards_already_used: List of cards that were already seen somehow
    :return: List of cards opponent COULD have
    '''
    possible_cards = create_deck()
    for card in cards_already_used:
        possible_cards.remove(card)
    return possible_cards