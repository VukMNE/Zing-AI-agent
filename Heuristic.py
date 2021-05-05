from main import count_points_from
from card import Card

def heuristic(cards_on_table, my_cards, treshold, cards_already_played):
    '''
    Heuristic function that evaluate how good each card (currently in hands) is.
    :param cards_on_table: Cards currently on the table
    :param my_cards:
    :param treshold: Some value for deciding if point in cards_on_table are high enough
    :return: Score for every card in my_cards
    '''

    #First we set all scores to 0
    scores = [0 for i in range(len(my_cards))]

    #check for same card, if you have same card, always throw it.
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
        else:
            #card have a small amount of points so spending J is not a good choice if you have other options
            #TODO












def check_for_same_card(my_cards, evaluate_card):
    '''
    Checks if we have the same value of a card in my_cards.
    :param my_cards: Cards in hand
    :param evaluate_card: Card we want to check
    :return: True if we have the same card, otherwise False and index of a card found (-1 if False)
    '''
    has_same_card = False
    index = -1
    for i,card in enumerate(my_cards):
        if card.number == evaluate_card.number:
            has_same_card = True
            index = i
            break
    return has_same_card, index