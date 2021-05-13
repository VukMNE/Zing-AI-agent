from main import count_points_from, create_deck
from card import Card

def heuristic_function(cards_on_table, my_cards, treshold, cards_already_played, deck):
    '''
    Heuristic function that evaluate how good each card (currently in hands) is.
    :param cards_on_table: Cards currently on the table
    :param my_cards:
    :param treshold: Some value for deciding if point in cards_on_table are high enough
    :return: list of scores for every card in my_cards
    '''

    #First we set all scores to 0
    scores = [0.0 for i in range(len(my_cards))]

    # I initialized the variable here, because it might be useful later // Vuk 12.05.2021
    has_same_card = False
    #check for same card, if you have same card, always throw it.
    if len(cards_on_table) != 0:
        has_same_card, index = check_for_same_card(my_cards, cards_on_table[-1])
        if has_same_card == True:
            # print('We have the same card')
            scores[index] = 1
            return scores

    #check if you have J
    has_J, index = check_for_same_card(my_cards, Card(11,'J', None))
    if has_same_card == False:
        if has_J:
            # print('We have Janez')
            # let's ignore the threshold for now
            # In the ideal heuristic function, threshold would be probability that the other player takes cards from
            # the table if we don't play Janez


            # if count_points_from(cards_on_table) > treshold:
            #     #cards on the table have many points
            #     #TODO
            #     pass
            # else:
            #     #card have a small amount of points so spending J is not a good choice if you have other options
            #     #TODO
            #     pass

            # so right now, if we have Janez, we play it
            scores[index] = 1
            return scores

    # if we don't have neither Janez nor the same card as the one on the table
    # we should play the card that was played most frequently, since there is less probability that the opponent will
    # have it in his/her hands. Also, if there is more than one card that is a candidate,
    # we should play the one that gives least points

    # all_known_cards_to_me, are the cards that I know that were played, with addition of the last card in the deck,
    # which is always shown faced up

    # for the evaluation of each card, we should also include remaining cards that we have in our hand
    # Example:
    # I have 5, 5, 6 and 8 in my hand
    # And if I already know that all of these cards appeared exactly twice already in the game,
    # then I know that the opponent will not have any more 5s so it is safe to play it

    for i, card in enumerate(my_cards):
        my_other_cards = [x for j,x in enumerate(my_cards) if j!=i]
        all_known_cards_to_me = cards_already_played + my_other_cards

        # we should also include the last card in the deck, since it is shown faced-up
        # ofcourse, unless it is already in our hand

        if (len(deck) > 0) and (my_cards[-1] != deck[-1]):
            all_known_cards_to_me.append(deck[-1])

        # we add 0.25, since at most a card can be played 4 times. So if it appeared 3 times in the game,
        # and we have it in our hand, it is definitely safe to play it
        scores[i] = card_frequency(card, all_known_cards_to_me) + 0.25

    # now, lets lower the scores for pictures, and cards that have points
    # why? well, if we are not able to take the cards on the table, we shouldn't throw points to the opponent

    for i, card in enumerate(my_cards):
        if (card.number >= 10) or (card.number == 1):
            scores[i] -= 0.05
            if (card.number == 10) and (card.sign == 'diamond'):
                scores[i] -= 0.05
        if (card.number == 2) and (card.sign == 'club'):
            scores[i] -= 0.05
    if len(deck) > 0:
        return scores



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
    for i,mcard in enumerate(my_cards):
        if mcard.number == card.number:
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

def card_frequency(card, cards_played):
    c = 0
    for cp in cards_played:
        if cp.number == card.number:
            c += 1

    return c / 4