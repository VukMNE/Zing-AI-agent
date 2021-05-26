import numpy as np
from mctspy.games.common import TwoPlayersAbstractGameState, AbstractGameAction
from utils import *
from mctspy.tree.nodes import TwoPlayersGameMonteCarloTreeSearchNode
from mctspy.tree.search import MonteCarloTreeSearch
import copy

class ZingMove(AbstractGameAction):
    def __init__(self, card, next_to_move):
        self.card = card
        self.next_to_move = next_to_move

    def __repr__(self):
        return "card:{0}".format(
            self.card
        )


class ZingGameState(TwoPlayersAbstractGameState):

    player_0 = 1
    player_1 = -1

    def __init__(self, previous_move, deck, cards_on_table, my_points, my_cards, my_total_points, my_taken_cards, opp_points, opp_cards, opp_total_points, opp_taken_cards,  next_to_move=1, last_taken_by = 0, who_is_first = 1, round = 0):
        self.deck = deck
        self.cards_on_table = cards_on_table
        self.my_points = my_points
        self.my_cards = my_cards
        self.my_total_points = my_total_points
        self.my_taken_cards = my_taken_cards
        self.opp_points = opp_points
        self.opp_cards = opp_cards
        self.opp_total_points = opp_total_points
        self.opp_taken_cards = opp_taken_cards
        self.next_to_move = next_to_move
        self.last_taken_by = last_taken_by
        self.who_is_first = who_is_first
        self.round = round
        self.previous_move = previous_move


    @property
    def game_result(self):
        # check if game is over

        if self.my_total_points >= 101:
            #print('I won')
            return self.player_0

        elif self.opp_total_points >= 101:
            #print('Opp won')
            return self.player_1

        # if not over - no result
        return None

    def is_game_over(self):
        return self.game_result is not None


    def move(self, move):
        last_taken_by = copy.deepcopy(self.last_taken_by)
        round = copy.deepcopy(self.round)
        deck = copy.deepcopy(self.deck)
        my_total_points = copy.deepcopy(self.my_total_points)
        opp_total_points = copy.deepcopy(self.opp_total_points)
        my_taken_cards = copy.deepcopy(self.my_taken_cards)
        opp_taken_cards = copy.deepcopy(self.opp_taken_cards)
        my_points =copy.deepcopy( self.my_points)
        opp_points = copy.deepcopy(self.opp_points)
        my_cards = copy.deepcopy(self.my_cards)
        opp_cards = copy.deepcopy(self.opp_cards)
        next_to_move =copy.deepcopy( self.next_to_move)
        cards_on_table = copy.deepcopy(self.cards_on_table)
        who_is_first = copy.deepcopy(self.who_is_first)



        if next_to_move == 0:
            my_move = my_cards.index(move.card)
        else:
            my_move = opp_cards.index(move.card)

        previous_move = my_move
        prior_length = len(cards_on_table)

        #make a move
        cards_on_table, my_cards, opp_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = solve_move(
            cards_on_table, my_move, next_to_move + 1, my_cards, opp_cards, my_taken_cards, opp_taken_cards,
            my_points, opp_points, False)
        if prior_length > len(cards_on_table):
            last_taken_by = next_to_move

        #if this was the last card in hand
        if len(my_cards)==0 and len(opp_cards) == 0 and len(deck) > 0:
            my_cards, opp_cards, deck = deal_cards(who_is_first, deck)
            round += 1

        #if the deck is empty
        if len(my_cards)==0 and len(opp_cards) == 0 and len(deck) == 0:
            #if there are card on the table
            if len(cards_on_table) > 0:
                cards_on_table, my_taken_cards, opp_taken_cards, my_points, opp_points = transfer_cards_and_points(
                    cards_on_table, last_taken_by, my_taken_cards, opp_taken_cards, my_points, opp_points)

            if len(my_taken_cards) > len(opp_taken_cards):
                my_points += 3
            elif len(my_taken_cards) < len(opp_taken_cards):
                opp_points += 3

            my_total_points  += my_points
            opp_total_points += opp_points

            #new round
            deck = shuffle_deck(create_deck())
            #change who starts
            if who_is_first == 0:
                who_is_first = 1
            else:
                who_is_first = 0
            my_points, opp_points = 0, 0
            my_taken_cards = list()
            opp_taken_cards = list()
            cards_on_table = deck[:4]
            deck = deck[4:]

            my_cards, opp_cards, deck = deal_cards(who_is_first, deck)
            last_taken_by = 0

            round = 1

        if next_to_move == 0:
            next_to_move = 1
        else:
            next_to_move = 0

        return ZingGameState(previous_move, deck, cards_on_table, my_points, my_cards, my_total_points, my_taken_cards, opp_points, opp_cards, opp_total_points, opp_taken_cards, next_to_move, last_taken_by, 1, round)

    def get_legal_actions(self):
        if self.next_to_move == 0:
            cards = self.my_cards
        else:
            cards = self.opp_cards
        return [
            ZingMove(card, self.next_to_move)
            for card in cards
        ]

def monte_carlo_best_card(best_previous, deck, cards_on_table, my_points, my_cards, my_total_points, my_taken_cards, opp_points, opp_cards, opp_total_points, opp_taken_cards, who_is_first, last_taken_by):
    '''Returns the index of the best card, that should be played according to monte carlo simulation'''
    initial = ZingGameState(best_previous, deck, cards_on_table, my_points, my_cards, my_total_points, my_taken_cards,
                            opp_points, opp_cards, opp_total_points, opp_taken_cards, who_is_first, last_taken_by)

    root = TwoPlayersGameMonteCarloTreeSearchNode(state=initial)
    mcts = MonteCarloTreeSearch(root)
    best_node = mcts.best_action(1000)
    move = best_node.state.previous_move
    return move



if __name__ == '__main__':
    my_total_points = 0
    opp_total_points = 0

    deck = shuffle_deck(create_deck())
    #cards_on_table = list()
    card_underneath = deck[-1]

    who_is_first = 1

    cards_on_table = deck[:4]
    deck = deck[4:]

    my_cards, opp_cards, deck = deal_cards(who_is_first, deck)
    my_points, opp_points = 0, 0

    my_taken_cards = list()
    opp_taken_cards = list()

    last_taken_by = 0

    initial = ZingGameState(None, deck, cards_on_table, my_points, my_cards, my_total_points, my_taken_cards, opp_points, opp_cards, opp_total_points, opp_taken_cards, who_is_first, last_taken_by)

    root = TwoPlayersGameMonteCarloTreeSearchNode(state=initial)
    mcts = MonteCarloTreeSearch(root)
    best_node = mcts.best_action(10)
    move = best_node.state.previous_move
