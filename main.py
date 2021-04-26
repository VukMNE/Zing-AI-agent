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
            deck.append(Card(val, sign))

    return deck

def shuffle_deck(deck):
    rand_sequence = random.choices(list(range(52)), k = 52)
    shuffled_deck = [deck[i] for i in rand_sequence]
    return shuffled_deck

# TODO
# def construct_complete_graph(n):
#     

if __name__ == '__main__':

    deck = shuffle_deck(create_deck())

    for card in deck:
        print(card)