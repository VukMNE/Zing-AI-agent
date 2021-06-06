from utils import *
from Heuristic import *
from monte_carlo import *
from tictactoe import *


def play_monte_carlo_vs_random(n,seconds,who_is_first):
    '''
    This plays a game where one player randomly chooses cards and the other plays the best card according to heuristic function.
    Player wins when he reaches at least 101 points.
    :return: 1 if heuristic player wins, otherwise 0
    '''

    my_total_points = 0
    opp_total_points = 0

    while my_total_points < 101 and opp_total_points < 101:
        deck = shuffle_deck(create_deck())
        cards_on_table = list()
        card_underneath = deck[-1]

        if my_total_points > 0 or opp_total_points > 0:
            # we need to switch who plays first everytime the deck gets empty
            if who_is_first == 1:
                who_is_first = 2
            else:
                who_is_first = 1
        # print('Deck is shuffled. Who plays first? If you go first, type in 1, if computer should go first press 2')
        # who_is_first = int(input())
        # print('Your choice: ' + str(who_is_first))
        my_points, opp_points = 0, 0
        my_taken_cards = list()
        opp_taken_cards = list()

        cards_on_table = deck[:4]

        # I put this code here, just to check whether we always shuffle the deck in the same manner
        # if my_total_points == 0 and opp_total_points == 0:
        #     print('First 4 are')
        #     print_cards_inline(cards_on_table)

        deck = deck[4:]


        my_cards, opponent_cards, deck = deal_cards(who_is_first, deck)

        # print('To play a card, press 1 for the first, 2 for second, etc....')

        # we use this variable to see who is the last person who took the cards from the table
        # this is important in order to solve to whom do the cards go at the end of the game
        last_taken_by = 0

        round = 1
        while round <= 6:
            # print('Cards on the cards_on_table are: ')
            # print_cards_inline(cards_on_table)
            while len(my_cards) + len(opponent_cards) > 0:
                if who_is_first == 1:
                    # heuristic agent moves first in this hand
                    # print('--------------------IT IS YOUR MOVE NOW-----------------------------')
                    # print('My Cards are')
                    # print_cards_inline(my_cards)
                    try:
                        monte_carlo_card = monte_carlo_best_card(n,seconds,None, deck, cards_on_table, my_points, my_cards, my_total_points, my_taken_cards, opp_points, opponent_cards, opp_total_points, opp_taken_cards, who_is_first, last_taken_by)
                        # print('my move is: ')
                        # print(my_cards[monte_carlo_card])
                    except Exception as e:
                        e.with_traceback()
                        print('Failed to upload to ftp: '+ str(e))
                        a=3

                    ##print('Monte carlo:')
                    #print(monte_carlo_card)
                    my_move = monte_carlo_card
                    # print(str(len(my_cards)) + '=' + str(my_move))
                    prior_length = len(cards_on_table)
                    # print('I play')
                    # print(my_cards[my_move])
                    # print('my cards before:')
                    # print_cards_inline(my_cards)
                    cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = solve_move(
                        cards_on_table, my_move, 1, my_cards, opponent_cards, my_taken_cards, opp_taken_cards,
                        my_points, opp_points, False)
                    if prior_length > len(cards_on_table):
                        last_taken_by = 1

                    # print('my cards after:')
                    # print_cards_inline(my_cards)
                    # print('-------------------------')

                    prior_length = len(cards_on_table)
                    # code is moved to utils function opp_makes_a_move
                    cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = \
                        opp_makes_a_move(cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards,
                                         my_points, opp_points, show = False)
                    if prior_length > len(cards_on_table):
                        last_taken_by = 2
                    # print('Cards on the cards_on_table are: ')
                    # print_cards_inline(cards_on_table)

                else:
                    # computer (agent that makes random moves) moves first in this hand
                    prior_length = len(cards_on_table)
                    # code is moved to utils function opp_makes_a_move
                    cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = \
                        opp_makes_a_move(cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards,
                                         my_points, opp_points, show = False)
                    if prior_length > len(cards_on_table):
                        last_taken_by = 2
                    # print('Cards on the cards_on_table are: ')
                    # print_cards_inline(cards_on_table)
                    #
                    # print('--------------------IT IS YOUR MOVE NOW-----------------------------')
                    # print('My Cards are')
                    # print_cards_inline(my_cards)
                    try:
                        monte_carlo_card = monte_carlo_best_card(n,seconds,None, deck, cards_on_table, my_points, my_cards,
                                                             my_total_points, my_taken_cards, opp_points, opponent_cards,
                                                             opp_total_points, opp_taken_cards, 0,
                                                             last_taken_by)
                    except Exception as e:
                        e.with_traceback()
                        # print('Failed to upload to ftp: ' + str(e))
                        a=3

                    #print('Monte carlo 2:')
                    #print(monte_carlo_card)
                    my_move = monte_carlo_card
                    # print(str(len(my_cards)) + '=' + str(my_move + 1))
                    # print('I play')
                    # print(my_cards[my_move])
                    prior_length = len(cards_on_table)
                    cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = solve_move(
                        cards_on_table, my_move, 1, my_cards, opponent_cards, my_taken_cards, opp_taken_cards,
                        my_points, opp_points, False)
                    if prior_length > len(cards_on_table):
                        last_taken_by = 1

            # print('Deal the cards....')
            my_cards, opponent_cards, deck = deal_cards(who_is_first, deck)
            # print('Deck size: ' + str(len(deck)))
            round += 1

        # What remains after the last hand goes to the player who last took the cards in the game
        if len(cards_on_table) > 0:
            cards_on_table, my_taken_cards, opp_taken_cards, my_points, opp_points = transfer_cards_and_points(
                cards_on_table, last_taken_by, my_taken_cards, opp_taken_cards, my_points, opp_points)

        if len(my_taken_cards) > len(opp_taken_cards):
            my_points += 3
        elif len(my_taken_cards) < len(opp_taken_cards):
            opp_points += 3
        # print('++++++++++++++++++++++++ ROUND FINISHED ++++++++++++++++')
        # print('Your points: ' + str(my_points))
        # print('Opponent points: ' + str(opp_points))
        my_total_points = my_total_points + my_points
        opp_total_points = opp_total_points + opp_points


    print('Game finished')
    print('Monte-Carlo points: ' + str(my_total_points))
    print('Random agent points: ' + str(opp_total_points))
    print('------------------------')
    if my_total_points > opp_total_points:
        return 1
    return 0


def play_random_vs_heuristic(who_is_first):
    '''
    This plays a game where one player randomly chooses cards and the other plays the best card according to heuristic function.
    Player wins when he reaches at least 101 points.
    :return: 1 if heuristic player wins, otherwise 0
    '''

    my_total_points = 0
    opp_total_points = 0

    while my_total_points < 101 and opp_total_points < 101:
        deck = shuffle_deck(create_deck())
        cards_on_table = list()
        card_underneath = deck[-1]

        if my_total_points > 0 or opp_total_points > 0:
            # we need to switch who plays first everytime the deck gets empty
            if who_is_first == 1:
                who_is_first = 2
            else:
                who_is_first = 1
        # print('Deck is shuffled. Who plays first? If you go first, type in 1, if computer should go first press 2')
        # who_is_first = int(input())
        # print('Your choice: ' + str(who_is_first))
        my_points, opp_points = 0, 0
        my_taken_cards = list()
        opp_taken_cards = list()

        cards_on_table = deck[:4]

        # I put this code here, just to check whether we always shuffle the deck in the same manner
        # if my_total_points == 0 and opp_total_points == 0:
        #     print('First 4 are')
        #     print_cards_inline(cards_on_table)

        deck = deck[4:]


        my_cards, opponent_cards, deck = deal_cards(who_is_first, deck)

        # print('To play a card, press 1 for the first, 2 for second, etc....')

        # we use this variable to see who is the last person who took the cards from the table
        # this is important in order to solve to whom do the cards go at the end of the game
        last_taken_by = 0

        round = 1
        while round <= 6:
            # print('Cards on the cards_on_table are: ')
            # print_cards_inline(cards_on_table)
            while len(my_cards) + len(opponent_cards) > 0:
                if who_is_first == 1:
                    # heuristic agent moves first in this hand
                    # print('--------------------IT IS YOUR MOVE NOW-----------------------------')
                    # print('My Cards are')
                    # print_cards_inline(my_cards)
                    heuristic_score = heuristic_function(cards_on_table, my_cards, opponent_cards, 0.25, my_taken_cards + opp_taken_cards,
                                                         deck)
                    # print('Heuristic scores:')
                    # print(heuristic_score)
                    my_move = heuristic_score.index(max(heuristic_score))
                    prior_length = len(cards_on_table)
                    # print('I play')
                    # print(my_cards[my_move])
                    cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = solve_move(
                        cards_on_table, my_move, 1, my_cards, opponent_cards, my_taken_cards, opp_taken_cards,
                        my_points, opp_points, False)
                    if prior_length > len(cards_on_table):
                        last_taken_by = 1

                    prior_length = len(cards_on_table)
                    # code is moved to utils function opp_makes_a_move
                    cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = \
                        opp_makes_a_move(cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards,
                                         my_points, opp_points, show = False)
                    if prior_length > len(cards_on_table):
                        last_taken_by = 2
                    # print('Cards on the cards_on_table are: ')
                    # print_cards_inline(cards_on_table)

                else:
                    # computer (agent that makes random moves) moves first in this hand
                    prior_length = len(cards_on_table)
                    # code is moved to utils function opp_makes_a_move
                    cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = \
                        opp_makes_a_move(cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards,
                                         my_points, opp_points, show = False)
                    if prior_length > len(cards_on_table):
                        last_taken_by = 2
                    # print('Cards on the cards_on_table are: ')
                    # print_cards_inline(cards_on_table)
                    # 
                    # print('--------------------IT IS YOUR MOVE NOW-----------------------------')
                    # print('My Cards are')
                    # print_cards_inline(my_cards)
                    heuristic_score = heuristic_function(cards_on_table, my_cards, opponent_cards, 0.25, my_taken_cards + opp_taken_cards,
                                                         deck)
                    # print('Heuristic scores:')
                    # print(heuristic_score)
                    my_move = heuristic_score.index(max(heuristic_score))
                    # print('I play')
                    # print(my_cards[my_move])
                    prior_length = len(cards_on_table)
                    cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = solve_move(
                        cards_on_table, my_move, 1, my_cards, opponent_cards, my_taken_cards, opp_taken_cards,
                        my_points, opp_points, False)
                    if prior_length > len(cards_on_table):
                        last_taken_by = 1

            # print('Deal the cards....')
            my_cards, opponent_cards, deck = deal_cards(who_is_first, deck)
            # print('Deck size: ' + str(len(deck)))
            round += 1

        # What remains after the last hand goes to the player who last took the cards in the game
        if len(cards_on_table) > 0:
            cards_on_table, my_taken_cards, opp_taken_cards, my_points, opp_points = transfer_cards_and_points(
                cards_on_table, last_taken_by, my_taken_cards, opp_taken_cards, my_points, opp_points)

        if len(my_taken_cards) > len(opp_taken_cards):
            my_points += 3
        elif len(my_taken_cards) < len(opp_taken_cards):
            opp_points += 3
        # print('++++++++++++++++++++++++ ROUND FINISHED ++++++++++++++++')
        # print('Your points: ' + str(my_points))
        # print('Opponent points: ' + str(opp_points))
        my_total_points = my_total_points + my_points
        opp_total_points = opp_total_points + opp_points


    # print('Game finished')
    # print('Heuristic points: ' + str(my_total_points))
    # print('Random agent points: ' + str(opp_total_points))
    # print('------------------------')
    if my_total_points > opp_total_points:
        return 1
    return 0

def play_random_vs_basic(who_is_first):
    '''
    This plays a game where one player randomly chooses cards and the other plays the best card according to heuristic function.
    Player wins when he reaches at least 101 points.
    :return: 1 if heuristic player wins, otherwise 0
    '''

    my_total_points = 0
    opp_total_points = 0

    while my_total_points < 101 and opp_total_points < 101:
        deck = shuffle_deck(create_deck())
        cards_on_table = list()
        card_underneath = deck[-1]

        if my_total_points > 0 or opp_total_points > 0:
            # we need to switch who plays first everytime the deck gets empty
            if who_is_first == 1:
                who_is_first = 2
            else:
                who_is_first = 1
        # print('Deck is shuffled. Who plays first? If you go first, type in 1, if computer should go first press 2')
        # who_is_first = int(input())
        # print('Your choice: ' + str(who_is_first))
        my_points, opp_points = 0, 0
        my_taken_cards = list()
        opp_taken_cards = list()

        cards_on_table = deck[:4]

        # I put this code here, just to check whether we always shuffle the deck in the same manner
        # if my_total_points == 0 and opp_total_points == 0:
        #     print('First 4 are')
        #     print_cards_inline(cards_on_table)

        deck = deck[4:]


        my_cards, opponent_cards, deck = deal_cards(who_is_first, deck)

        # print('To play a card, press 1 for the first, 2 for second, etc....')

        # we use this variable to see who is the last person who took the cards from the table
        # this is important in order to solve to whom do the cards go at the end of the game
        last_taken_by = 0

        round = 1
        while round <= 6:
            # print('Cards on the cards_on_table are: ')
            # print_cards_inline(cards_on_table)
            while len(my_cards) + len(opponent_cards) > 0:
                if who_is_first == 1:
                    # heuristic agent moves first in this hand
                    # print('--------------------IT IS YOUR MOVE NOW-----------------------------')
                    # print('My Cards are')
                    # print_cards_inline(my_cards)
                    heuristic_score = basic_heuristic_function(cards_on_table, my_cards, None, my_taken_cards + opp_taken_cards,
                                                         deck)
                    # print('Heuristic scores:')
                    # print(heuristic_score)
                    my_move = heuristic_score.index(max(heuristic_score))
                    prior_length = len(cards_on_table)
                    # print('I play')
                    # print(my_cards[my_move])
                    cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = solve_move(
                        cards_on_table, my_move, 1, my_cards, opponent_cards, my_taken_cards, opp_taken_cards,
                        my_points, opp_points, False)
                    if prior_length > len(cards_on_table):
                        last_taken_by = 1

                    prior_length = len(cards_on_table)
                    # code is moved to utils function opp_makes_a_move
                    cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = \
                        opp_makes_a_move(cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards,
                                         my_points, opp_points, show = False)
                    if prior_length > len(cards_on_table):
                        last_taken_by = 2
                    # print('Cards on the cards_on_table are: ')
                    # print_cards_inline(cards_on_table)

                else:
                    # computer (agent that makes random moves) moves first in this hand
                    prior_length = len(cards_on_table)
                    # code is moved to utils function opp_makes_a_move
                    cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = \
                        opp_makes_a_move(cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards,
                                         my_points, opp_points, show = False)
                    if prior_length > len(cards_on_table):
                        last_taken_by = 2
                    # print('Cards on the cards_on_table are: ')
                    # print_cards_inline(cards_on_table)
                    #
                    # print('--------------------IT IS YOUR MOVE NOW-----------------------------')
                    # print('My Cards are')
                    # print_cards_inline(my_cards)
                    heuristic_score = basic_heuristic_function(cards_on_table, my_cards, None, my_taken_cards + opp_taken_cards,
                                                         deck)
                    # print('Heuristic scores:')
                    # print(heuristic_score)
                    my_move = heuristic_score.index(max(heuristic_score))
                    # print('I play')
                    # print(my_cards[my_move])
                    prior_length = len(cards_on_table)
                    cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = solve_move(
                        cards_on_table, my_move, 1, my_cards, opponent_cards, my_taken_cards, opp_taken_cards,
                        my_points, opp_points, False)
                    if prior_length > len(cards_on_table):
                        last_taken_by = 1

            # print('Deal the cards....')
            my_cards, opponent_cards, deck = deal_cards(who_is_first, deck)
            # print('Deck size: ' + str(len(deck)))
            round += 1

        # What remains after the last hand goes to the player who last took the cards in the game
        if len(cards_on_table) > 0:
            cards_on_table, my_taken_cards, opp_taken_cards, my_points, opp_points = transfer_cards_and_points(
                cards_on_table, last_taken_by, my_taken_cards, opp_taken_cards, my_points, opp_points)

        if len(my_taken_cards) > len(opp_taken_cards):
            my_points += 3
        elif len(my_taken_cards) < len(opp_taken_cards):
            opp_points += 3
        # print('++++++++++++++++++++++++ ROUND FINISHED ++++++++++++++++')
        # print('Your points: ' + str(my_points))
        # print('Opponent points: ' + str(opp_points))
        my_total_points = my_total_points + my_points
        opp_total_points = opp_total_points + opp_points


    # print('Game finished')
    # print('Heuristic points: ' + str(my_total_points))
    # print('Random agent points: ' + str(opp_total_points))
    # print('------------------------')
    if my_total_points > opp_total_points:
        return 1
    return 0


def play_h1_vs_h2(who_is_first):
    '''
    This plays a game between two AI agents that use different heuristic functions.
    h1 - is a heuristic function using a special case for Janez
    h2 - Doesn't use Janez special case (in other words, it plays Janez as soon as it gets it)
    Player wins when he reaches at least 101 points.
    :return: 1 if heuristic player wins, otherwise 0
    '''

    my_total_points = 0
    opp_total_points = 0

    while my_total_points < 101 and opp_total_points < 101:
        deck = shuffle_deck(create_deck())
        cards_on_table = list()
        card_underneath = deck[-1]

        if my_total_points > 0 or opp_total_points > 0:
            # we need to switch who plays first everytime the deck gets empty
            if who_is_first == 1:
                who_is_first = 2
            else:
                who_is_first = 1
        # print('Deck is shuffled. Who plays first? If you go first, type in 1, if computer should go first press 2')
        # who_is_first = int(input())
        # print('Your choice: ' + str(who_is_first))
        my_points, opp_points = 0, 0
        my_taken_cards = list()
        opp_taken_cards = list()

        cards_on_table = deck[:4]

        # I put this code here, just to check whether we always shuffle the deck in the same manner
        # if my_total_points == 0 and opp_total_points == 0:
        #     print('First 4 are')
        #     print_cards_inline(cards_on_table)

        deck = deck[4:]


        my_cards, opponent_cards, deck = deal_cards(who_is_first, deck)

        # print('To play a card, press 1 for the first, 2 for second, etc....')

        # we use this variable to see who is the last person who took the cards from the table
        # this is important in order to solve to whom do the cards go at the end of the game
        last_taken_by = 0

        round = 1
        while round <= 6:
            # print('Cards on the cards_on_table are: ')
            # print_cards_inline(cards_on_table)
            while len(my_cards) + len(opponent_cards) > 0:
                if who_is_first == 1:
                    # heuristic agent moves first in this hand
                    # print('--------------------IT IS YOUR MOVE NOW-----------------------------')
                    # print('My Cards are')
                    # print_cards_inline(my_cards)
                    heuristic_score = heuristic_function(cards_on_table, my_cards, opponent_cards, 0.25, my_taken_cards + opp_taken_cards,
                                                         deck)
                    # print('Heuristic scores:')
                    # print(heuristic_score)
                    my_move = heuristic_score.index(max(heuristic_score))
                    prior_length = len(cards_on_table)
                    # print('I play')
                    # print(my_cards[my_move])
                    cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = solve_move(
                        cards_on_table, my_move, 1, my_cards, opponent_cards, my_taken_cards, opp_taken_cards,
                        my_points, opp_points, False)
                    if prior_length > len(cards_on_table):
                        last_taken_by = 1

                    prior_length = len(cards_on_table)
                    # code is moved to utils function opp_makes_a_move
                    h2_score = basic_heuristic_function(cards_on_table, opponent_cards, None,
                                                               my_taken_cards + opp_taken_cards,
                                                               deck)
                    opp_move = h2_score.index(max(h2_score))
                    cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = \
                        solve_move(cards_on_table, opp_move, 2, my_cards, opponent_cards, my_taken_cards, opp_taken_cards,
                            my_points, opp_points, False)
                    if prior_length > len(cards_on_table):
                        last_taken_by = 2
                    # print('Cards on the cards_on_table are: ')
                    # print_cards_inline(cards_on_table)

                else:
                    # computer (agent that makes random moves) moves first in this hand
                    prior_length = len(cards_on_table)
                    # code is moved to utils function opp_makes_a_move
                    h2_score = basic_heuristic_function(cards_on_table, opponent_cards, None,
                                                        my_taken_cards + opp_taken_cards,
                                                        deck)
                    opp_move = h2_score.index(max(h2_score))

                    cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = \
                        solve_move(cards_on_table, opp_move, 2, my_cards, opponent_cards, my_taken_cards,
                                   opp_taken_cards,
                                   my_points, opp_points, False)
                    if prior_length > len(cards_on_table):
                        last_taken_by = 2
                    # print('Cards on the cards_on_table are: ')
                    # print_cards_inline(cards_on_table)
                    #
                    # print('--------------------IT IS YOUR MOVE NOW-----------------------------')
                    # print('My Cards are')
                    # print_cards_inline(my_cards)
                    heuristic_score = heuristic_function(cards_on_table, my_cards, opponent_cards, 0.25, my_taken_cards + opp_taken_cards,
                                                         deck)
                    # print('Heuristic scores:')
                    # print(heuristic_score)
                    my_move = heuristic_score.index(max(heuristic_score))
                    # print('I play')
                    # print(my_cards[my_move])
                    prior_length = len(cards_on_table)
                    cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = solve_move(
                        cards_on_table, my_move, 1, my_cards, opponent_cards, my_taken_cards, opp_taken_cards,
                        my_points, opp_points, False)
                    if prior_length > len(cards_on_table):
                        last_taken_by = 1

            # print('Deal the cards....')
            my_cards, opponent_cards, deck = deal_cards(who_is_first, deck)
            # print('Deck size: ' + str(len(deck)))
            round += 1

        # What remains after the last hand goes to the player who last took the cards in the game
        if len(cards_on_table) > 0:
            cards_on_table, my_taken_cards, opp_taken_cards, my_points, opp_points = transfer_cards_and_points(
                cards_on_table, last_taken_by, my_taken_cards, opp_taken_cards, my_points, opp_points)

        if len(my_taken_cards) > len(opp_taken_cards):
            my_points += 3
        elif len(my_taken_cards) < len(opp_taken_cards):
            opp_points += 3
        # print('++++++++++++++++++++++++ ROUND FINISHED ++++++++++++++++')
        # print('Your points: ' + str(my_points))
        # print('Opponent points: ' + str(opp_points))
        my_total_points = my_total_points + my_points
        opp_total_points = opp_total_points + opp_points


    # print('Game finished')
    # print('Heuristic points: ' + str(my_total_points))
    # print('Random agent points: ' + str(opp_total_points))
    # print('------------------------')
    if my_total_points > opp_total_points:
        return 1
    return 0


def play():
    # Introducing some variables
    # deck is the shuffled list of cards with which we play
    # cards_on_table is the table at which we trow cards
    # my_cards are cards that I have currently in hand
    # opponent_cards are cards that opponent has currently in hand
    # my_taken_cards are cards that I have taken (we count points from them)
    # opponent_taken_cards are cards that opponent have taken (we countr points from them)
    # my_points - type int, just the number of my points
    # opp_points - type int, just the number of opp points
    # card_underneath - it is the last card in the deck. It is visible to both players

    # cards = [
    #     Card(12, 'Q', 'heart'),
    #     Card(12, 'Q', 'clubs'),
    # ]

    # print(count_points_from(cards))

    # CODE COMMENTED BELLOW IS JUST FOR TESTING
    # cards_on_table, my_taken_cards, opp_taken_cards, my_points, opp_points = collect_cards(cards, 1, my_taken_cards, opp_taken_cards, my_points, opp_points)
    # print('Points after')
    # print('Your points: ' + str(my_points))
    # print('Opponent points: ' + str(opp_points))

    deck = shuffle_deck(create_deck())
    cards_on_table = list()
    card_underneath = deck[-1]

    print('Deck is shuffled. Who plays first? If you go first, type in 1, if computer should go first press 2')
    who_is_first = int(input())
    print('Your choice: ' + str(who_is_first))
    my_points, opp_points = 0, 0
    my_taken_cards = list()
    opp_taken_cards = list()

    cards_on_table = deck[:4]
    deck = deck[4:]
    print('Cards on the cards_on_table are: ')
    print_cards(cards_on_table)

    my_cards, opponent_cards, deck = deal_cards(who_is_first, deck)

    print('To play a card, press 1 for the first, 2 for second, etc....')

    # we use this variable to see who is the last person who took the cards from the table
    # this is important in order to solve to whom do the cards go at the end of the game
    last_taken_by = 0

    round = 1
    # round <= 6, this is just pure mathematic, after 4 four cards are put on table, deck remains with 48,
    # so in each round, 8 cards are dealt in total, 4 to each player
    while round <= 6:
        while len(my_cards) + len(opponent_cards) > 0:
            if who_is_first == 1:
                # I, the human player, move first
                # code is moved to utils function i_make_a_move

                prior_length = len(cards_on_table)
                cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points =\
                    i_make_a_move(cards_on_table, my_cards,opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points)
                if prior_length > len(cards_on_table):
                    last_taken_by = 1

                prior_length = len(cards_on_table)
                # code is moved to utils function opp_makes_a_move
                cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = \
                    opp_makes_a_move(cards_on_table, my_cards,opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points)
                if prior_length > len(cards_on_table):
                    last_taken_by = 2

                print('-------------------------------------------------')
                print('Now the cards_on_table is:')
                print_cards_inline(cards_on_table)
            else:
                # In this case, computer makes the first move in each hand
                # code is moved to utils function opp_makes_a_move
                prior_length = len(cards_on_table)
                cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = \
                    opp_makes_a_move(cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points,
                                  opp_points)
                if prior_length > len(cards_on_table):
                    last_taken_by = 1

                print('-------------------------------------------------')
                print('Now the cards_on_table is:')
                print_cards_inline(cards_on_table)

                prior_length = len(cards_on_table)
                # code is moved to utils function i_make_a_move
                cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = \
                    i_make_a_move(cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards,
                                     my_points, opp_points)

                if prior_length > len(cards_on_table):
                    last_taken_by = 2

        print('Deal the cards....')
        my_cards, opponent_cards, deck = deal_cards(who_is_first, deck)
        print('Deck size: ' + str(len(deck)))
        round += 1

    # What remains after the last hand goes to the player who last took the cards in the game
    if len(cards_on_table) > 0:
        cards_on_table, my_taken_cards, opp_taken_cards, my_points, opp_points = transfer_cards_and_points(
            cards_on_table, last_taken_by, my_taken_cards, opp_taken_cards, my_points, opp_points)

    if len(my_taken_cards) > len(opp_taken_cards):
        my_points += 3
    elif len(my_taken_cards) < len(opp_taken_cards):
        opp_points += 3
    print('++++++++++++++++++++++++ ROUND FINISHED ++++++++++++++++')
    print('Your points: ' + str(my_points))
    print('Opponent points: ' + str(opp_points))


if __name__ == '__main__':
    wins = 0
    n = 50
    m = None
    # seconds = 0.5

    for _ in range(n):
        print(_)
        s = time.time()
        plays_first = (_ % 2) + 1
        # wins += play_monte_carlo_vs_random(m,seconds,plays_first)
        wins += play_monte_carlo_vs_random(10000, None, plays_first)
        e = time.time()
        time_spent = e - s
        print('Game finished, time spent: ' + str(time_spent))
        print('Current win ratio: ' + str(wins) + ' / ' + str(_ + 1))
    print(f"Wins: {wins/n}")

    # state = np.zeros((3, 3))
    # initial_board_state = TicTacToeGameState(state=state, next_to_move=1)
    #
    # root = TwoPlayersGameMonteCarloTreeSearchNode(state=initial_board_state)
    # mcts = MonteCarloTreeSearch(root)
    # best_node = mcts.best_action(10000)
    # print(best_node.state.board)



    # play()

