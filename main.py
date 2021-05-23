from utils import *
from heuristic import *


def play_random_vs_heuristic():
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

        # print('Deck is shuffled. Who plays first? If you go first, type in 1, if computer should go first press 2')
        # who_is_first = int(input())
        # print('Your choice: ' + str(who_is_first))
        who_is_first = 1
        my_points, opp_points = 0, 0
        my_taken_cards = list()
        opp_taken_cards = list()

        cards_on_table = deck[:4]
        deck = deck[4:]
        # print('Cards on the cards_on_table are: ')
        # print_cards(cards_on_table)

        my_cards, opponent_cards, deck = deal_cards(who_is_first, deck)

        # print('To play a card, press 1 for the first, 2 for second, etc....')

        # we use this variable to see who is the last person who took the cards from the table
        # this is important in order to solve to whom do the cards go at the end of the game
        last_taken_by = 0

        round = 1
        while round <= 6:
            while len(my_cards) + len(opponent_cards) > 0:
                if who_is_first == 1:
                    # -1 is because indexing goes from 0
                    # print('--------------------IT IS YOUR MOVE NOW-----------------------------')
                    # print('My Cards are')
                    # print_cards_inline(my_cards)
                    # my_move = int(input()) - 1
                    heuristic_score = heuristic_function(cards_on_table, my_cards, 3, my_taken_cards + opp_taken_cards, deck)
                    my_move = heuristic_score.index(max(heuristic_score))
                    prior_length = len(cards_on_table)
                    cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = solve_move(
                        cards_on_table, my_move, 1, my_cards, opponent_cards, my_taken_cards, opp_taken_cards,
                        my_points, opp_points, False)
                    if prior_length > len(cards_on_table):
                        last_taken_by = 1
                    opp_move = opp_plays(opponent_cards)
                    # print('**************************')
                    # print('OPPONENT CARDS')
                    # print_cards_inline(opponent_cards)
                    # print('**************************')
                    # print('opp move: ' + str(opp_move))
                    # print('Oponent plays: ' + str(opponent_cards[opp_move]))
                    prior_length = len(cards_on_table)
                    cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = solve_move(
                        cards_on_table, opp_move, 2, my_cards, opponent_cards, my_taken_cards, opp_taken_cards,
                        my_points, opp_points, False)
                    if prior_length > len(cards_on_table):
                        last_taken_by = 2
                    # print('-------------------------------------------------')
                    # print('Now the cards_on_table is:')
                    # print_cards_inline(cards_on_table)

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

        my_total_points += my_points
        opp_total_points += opp_points

    if my_total_points > opp_points:
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
    while round <= 6:
        while len(my_cards) + len(opponent_cards) > 0:
            if who_is_first == 1:
                # -1 is because indexing goes from 0
                print('--------------------IT IS YOUR MOVE NOW-----------------------------')
                print('My Cards are')
                print_cards_inline(my_cards)
                my_move = int(input()) - 1
                prior_length = len(cards_on_table)
                cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = solve_move(
                    cards_on_table, my_move, 1, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points,
                    opp_points)
                if prior_length > len(cards_on_table):
                    last_taken_by = 1
                opp_move = opp_plays(opponent_cards)
                print('**************************')
                print('OPPONENT CARDS')
                print_cards_inline(opponent_cards)
                print('**************************')
                # print('opp move: ' + str(opp_move))
                print('Oponent plays: ' + str(opponent_cards[opp_move]))
                prior_length = len(cards_on_table)
                cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = solve_move(
                    cards_on_table, opp_move, 2, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points,
                    opp_points)
                if prior_length > len(cards_on_table):
                    last_taken_by = 2
                print('-------------------------------------------------')
                print('Now the cards_on_table is:')
                print_cards_inline(cards_on_table)

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
    n = 10000
    for _ in range(n):
        wins += play_random_vs_heuristic()
    print(f"Wins: {wins/n}")

