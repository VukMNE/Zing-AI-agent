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

    return my_cards, opp_cards, deck

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

def solve_move(cards_on_table, move, whose_move, my_cards, opp_cards, my_taken_cards, opp_taken_cards, my_points, opp_points, show = True):
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
                cards_on_table,my_taken_cards, opp_taken_cards, my_points, opp_points = collect_cards(cards_on_table, whose_move, my_taken_cards, opp_taken_cards, my_points, opp_points, show)
        else:
            cards_on_table, my_taken_cards, opp_taken_cards, my_points, opp_points = collect_cards(cards_on_table,whose_move,my_taken_cards, opp_taken_cards,my_points, opp_points, show)
    else:
        if (cards_on_table[-1].value == card_played.value) or (card_played.value == 'J'):
            cards_on_table.append(card_played)
            cards_on_table,my_taken_cards, opp_taken_cards, my_points, opp_points = collect_cards(cards_on_table, whose_move, my_taken_cards, opp_taken_cards, my_points, opp_points, show)
        else:
            cards_on_table.append(card_played)

    return cards_on_table, my_cards, opp_cards, my_taken_cards, opp_taken_cards, my_points, opp_points

def collect_cards(cards_on_table, whose_move, my_taken_cards, opp_taken_cards, my_points, opp_points, show = True):
    if show:
        print('COLLECTION HAPPENS')
        print('Points before collection: ')
        print('My points: ' + str(my_points) + ' | Computer points: ' + str(opp_points))
        print_cards_inline(cards_on_table)
    if len(cards_on_table) == 2:
        # check if it is a zing, check if both cards have the same value
        if cards_on_table[0].number == cards_on_table[1].number:
            # it is a zing
            zing_points = 10
            if cards_on_table[1].value == 'J':
                zing_points = 20
            if whose_move == 1:
                my_points += zing_points
            else:
                opp_points += zing_points


    cards_on_table,my_taken_cards, opp_taken_cards, my_points, opp_points =  transfer_cards_and_points(cards_on_table, whose_move, my_taken_cards, opp_taken_cards, my_points, opp_points)
    if show:
        print('Points after collection: ')
        print('My points: ' + str(my_points) + ' | Computer points: ' + str(opp_points))
    return cards_on_table,my_taken_cards, opp_taken_cards, my_points, opp_points

def transfer_cards_and_points(cards_on_table, whose_move, my_taken_cards, opp_taken_cards, my_points, opp_points):
    if whose_move == 1:
        my_points += count_points_from(cards_on_table)
        for i, t in enumerate(cards_on_table):
            my_taken_cards.append(t)
    else:
        opp_points += count_points_from(cards_on_table)
        for i, t in enumerate(cards_on_table):
            opp_taken_cards.append(t)

    cards_on_table = []
    return cards_on_table,my_taken_cards, opp_taken_cards, my_points, opp_points


def count_points_from(cards):
    pts = 0
    for card in cards:
        if card.number == 1:
            pts += 1
        if card.number >= 10 or (card.number == 2 and card.sign == 'club'):
            pts += 1
            if card.number == 10 and card.sign == 'diamond':
                pts += 1

    return pts
