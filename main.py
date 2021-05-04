from card import Card
import random

def create_deck():
    deck = list()
    for i in range(1,5):
        sign = ''
        if i % 4 == 1:
            # spade
            sign = 'spade'
        if i % 4 == 2:
            sign = 'club'
        if i % 4 == 3:
            sign = 'heart'
        if i % 4 == 0:
            sign = 'diamond'
        for j in range(1, 14):
            val = str(j)
            if j > 10:
                if j == 11:
                    val = 'J'
                if j == 12:
                    val = 'Q'
                if j == 13:
                    val = 'K'
            deck.append(Card(j,val, sign))

    return deck

def shuffle_deck(deck):
    rand_sequence = random.sample(list(range(52)), k = 52)
    shuffled_deck = [deck[i] for i in rand_sequence]
    return shuffled_deck

def deal_cards(who_is_first, deck):
    if who_is_first == 1:
        my_cards = deck[:4]
        deck = deck[4:]
        opp_cards = deck[:4]
        deck = deck[4:]
    else:
        opp_cards = deck[:4]
        deck = deck[4:]
        my_cards = deck[:4]
        deck = deck[4:]

    return my_cards, opp_cards

def print_cards(cards):
    for c in cards:
        print(c)

def print_cards_inline(cards):
    s = ''
    i = 0
    for c in cards:
        if i > 0:
            s += ', '
        s += str(c)
        i += 1

    print(s)

def opp_plays(cards):
    # here opponent/computer selects his move
    # currently this code is using random choice
    selected_card_index = random_choice(cards)
    return selected_card_index

def random_choice(cards):
    selected_card_index = random.choice(list(range(len(cards))))
    return selected_card_index

def solve_move(cards_on_table, move, whose_move, my_cards, opp_cards, my_taken_cards, opp_taken_cards, my_points, opp_points):
    # checks whether you take, or not
    # also, it checks whether it is a zing or not
    card_played = None
    if whose_move == 1:
        card_played = my_cards[move]
        my_cards.pop(move)
    else:
        card_played = opp_cards[move]
        opp_cards.pop(move)

    if len(cards_on_table) == 0:
        cards_on_table.append(card_played)
    elif len(cards_on_table) == 1:
        if cards_on_table[0].value != card_played.value:
            cards_on_table.append(card_played)
            if card_played.value == 'J':
                # print('debug 1')
                cards_on_table,my_taken_cards, opp_taken_cards, my_points, opp_points = collect_cards(cards_on_table, whose_move, my_taken_cards, opp_taken_cards, my_points, opp_points)
    else:
        if (cards_on_table[-1].value == card_played.value) or (card_played.value == 'J'):
            # print('debug 2')
            # print(card_played.value)
            # print(str(card_played))
            cards_on_table.append(card_played)
            cards_on_table,my_taken_cards, opp_taken_cards, my_points, opp_points = collect_cards(cards_on_table, whose_move, my_taken_cards, opp_taken_cards, my_points, opp_points)
        else:
            cards_on_table.append(card_played)

    return cards_on_table, my_cards, opp_cards, my_taken_cards, opp_taken_cards, my_points, opp_points



def collect_cards(cards_on_table, whose_move, my_taken_cards, opp_taken_cards, my_points, opp_points):
    print('COLLECTION HAPPENS')
    print_cards_inline(cards_on_table)
    if len(cards_on_table) == 2:
        # check if it is a zing, check if both cards have the same value
        if cards_on_table[0].value == cards_on_table[1].value:
            # it is a zing
            zing_points = 10
            if cards_on_table[1].value == 'J':
                zing_points = 20
            if whose_move == 1:
                my_points += zing_points
            else:
                opp_points += zing_points

    return transfer_cards_and_points(cards_on_table, whose_move, my_taken_cards, opp_taken_cards, my_points, opp_points)

def transfer_cards_and_points(cards_on_table, whose_move, my_taken_cards, opp_taken_cards, my_points, opp_points):
    if whose_move == 1:
        for i, t in enumerate(cards_on_table):
            my_points += count_points_from(cards_on_table)
            my_taken_cards.append(t)
    else:
        for i, t in enumerate(cards_on_table):
            opp_points += count_points_from(cards_on_table)
            opp_taken_cards.append(t)

    cards_on_table = []
    return cards_on_table,my_taken_cards, opp_taken_cards, my_points, opp_points

def count_points_from(cards):
    pts = 0
    for card in cards:
        if card.number >= 10 or (card.number == 2 and card.sign == 'club'):
            pts += 1
            if card.number == 10 and card.sign == 'diamond':
                pts += 1

    return pts


if __name__ == '__main__':

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



    deck = shuffle_deck(create_deck())
    cards_on_table = list()
    card_underneath = deck[-1]

    print('Deck is shuffled. Who plays first? If you go first, type in 1, if computer should go first press 2')
    who_is_first = int(input())
    print('Your choice: ' + str(who_is_first))
    my_points, opp_points = 0,0
    my_taken_cards = list()
    opp_taken_cards = list()

    cards_on_table = deck[:4]
    deck = deck[4:]
    print('Cards on the cards_on_table are: ')
    print_cards(cards_on_table)

    my_cards, opponent_cards = deal_cards(who_is_first, deck)

    print('To play a card, press 1 for the first, 2 for second, etc....')

    round = 1
    while round <= 6:
        while len(my_cards) + len(opponent_cards) > 0:
            if who_is_first == 1:
                # -1 is because indexing goes from 0
                print('--------------------IT IS YOUR MOVE NOW-----------------------------')
                print('My Cards are')
                print_cards_inline(my_cards)
                my_move = int(input()) - 1
                cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = solve_move(cards_on_table, my_move, 1, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points)
                opp_move = opp_plays(opponent_cards)
                print('**************************')
                print('OPPONENT CARDS')
                print_cards_inline(opponent_cards)
                print('**************************')
                print('opp move: ' + str(opp_move))
                print('Oponent plays: ' + str(opponent_cards[opp_move]))
                cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = solve_move(cards_on_table, opp_move, 2, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points)
                print('-------------------------------------------------')
                print('Now the cards_on_table is:')
                print_cards_inline(cards_on_table)

                print('++ Your cards are ++')
                print_cards_inline(my_cards)
        print('Deal the cards....')
        my_cards, opponent_cards = deal_cards(who_is_first, deck)
        round += 1


    print('++++++++++++++++++++++++ ROUND FINISHED ++++++++++++++++')
    print('Your points: ' + str(my_points))
    print('Opponent points: ' + str(opp_points))

