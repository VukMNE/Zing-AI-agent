import numpy as np
from mctspy.games.common import TwoPlayersAbstractGameState, AbstractGameAction
from utils import *
from mctspy.tree.nodes import TwoPlayersGameMonteCarloTreeSearchNode
from mctspy.tree.search import MonteCarloTreeSearch

class ZingMove(AbstractGameAction):
    def __init__(self, card, next_to_move):
        self.card = card
        self.next_to_move = next_to_move

    def __repr__(self):
        return "card:{0}".format(
            self.card
        )


class ZingGameState(TwoPlayersAbstractGameState):

    player_1 = 1
    player_2 = -1

    def __init__(self, deck, cards_on_table, my_points, my_cards, my_total_points, my_taken_cards, opp_points, opp_cards, opp_total_points, opp_taken_cards,  next_to_move=1, last_taken_by = 0, round = 0):
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
        self.round = round

    @property
    def game_result(self):
        # check if game is over

        if self.my_total_points >= 101:
            print('I won')
            return self.player_1

        elif self.opp_total_points >= 101:
            print('Opp won')
            return self.player_2

        # if not over - no result
        return None

    def is_game_over(self):
        return self.game_result is not None


    def move(self, move):
        last_taken_by = self.last_taken_by
        round = self.round
        deck = self.deck
        my_total_points = self.my_total_points
        opp_total_points = self.opp_total_points
        try:
            i = self.my_cards.index(move.card)
        except:
            A=3
        if self.next_to_move == 1:
            prior_length = len(self.cards_on_table)

            cards_on_table, my_cards, opp_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = solve_move(
                self.cards_on_table, i, 1, self.my_cards, self.opp_cards, self.my_taken_cards, self.opp_taken_cards,
                self.my_points, self.opp_points, False)
            if prior_length > len(cards_on_table):
                last_taken_by = 1

            prior_length = len(cards_on_table)

            cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = \
                opp_makes_a_move(cards_on_table, my_cards, opp_cards, my_taken_cards, opp_taken_cards,
                                 my_points, opp_points, show=False)
            if prior_length > len(cards_on_table):
                last_taken_by = 2

        else:
            prior_length = len(self.cards_on_table)
            # code is moved to utils function opp_makes_a_move
            cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = \
                opp_makes_a_move(self.cards_on_table, self.my_cards, self.opp_cards, self.my_taken_cards, self.opp_taken_cards,
                                 self.my_points, self.opp_points, show=False)
            if prior_length > len(cards_on_table):
                last_taken_by = 2

            my_move = move

            prior_length = len(cards_on_table)
            cards_on_table, my_cards, opp_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = solve_move(
                cards_on_table, i, 1, my_cards, opponent_cards, my_taken_cards, opp_taken_cards,
                my_points, opp_points, False)
            if prior_length > len(cards_on_table):
                last_taken_by = 1

        if len(my_cards) == 0 or len(self.opp_cards)==0:
            my_cards, opp_cards, deck = deal_cards(self.next_to_move, self.deck)
            round += 1

        if round == 6:
            print('last round')
            if len(cards_on_table) > 0:
                cards_on_table, my_taken_cards, opp_taken_cards, my_points, opp_points = transfer_cards_and_points(
                    cards_on_table, last_taken_by, my_taken_cards, opp_taken_cards, my_points, opp_points)

            if len(my_taken_cards) > len(opp_taken_cards):
                my_points += 3
            elif len(my_taken_cards) < len(opp_taken_cards):
                opp_points += 3

            my_total_points += my_points
            opp_total_points += opp_points
            print(f'my total: {self.my_total_points}')
            print(f'opp total: {self.opp_total_points}')

            #start the game from the beggining
            deck = shuffle_deck(create_deck())
            # cards_on_table = list()
            card_underneath = deck[-1]

            who_is_first = 1

            cards_on_table = deck[:4]
            deck = deck[4:]

            my_cards, opp_cards, deck = deal_cards(who_is_first, deck)
            my_points, opp_points = 0, 0

            my_taken_cards = list()
            opp_taken_cards = list()

            round = 0

            last_taken_by = 0

        return ZingGameState(deck, cards_on_table, my_points, my_cards, my_total_points, my_taken_cards, opp_points, opp_cards, opp_total_points, opp_taken_cards, self.next_to_move, last_taken_by, round)

    def get_legal_actions(self):
        cards = self.my_cards
        return [
            ZingMove(card, self.next_to_move)
            for card in cards
        ]

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

    initial = ZingGameState(deck, cards_on_table, my_points, my_cards, my_total_points, my_taken_cards, opp_points, opp_cards, opp_total_points, opp_taken_cards, who_is_first, last_taken_by)

    root = TwoPlayersGameMonteCarloTreeSearchNode(state=initial)
    mcts = MonteCarloTreeSearch(root)
    best_node = mcts.best_action(100)
    print(best_node)