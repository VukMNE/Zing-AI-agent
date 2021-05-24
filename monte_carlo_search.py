import numpy as np
from collections import defaultdict
from utils import *

class ZingGameAction():
    def __init__(self, card_index, whose_move_it_is):
        self.card_index = card_index
        self.whose_move_it_is = whose_move_it_is

class ZingGameState():
    def __init__(self, deck, cards_on_table, whose_next_move, my_cards, opp_cards, my_taken_cards,
             opp_taken_cards, my_points, opp_points, last_taken_by):

        self.deck = deck
        self.cards_on_table = cards_on_table
        self.whose_next_move = whose_next_move
        self.my_cards = my_cards
        self.opp_cards = opp_cards
        self.my_taken_cards = my_taken_cards
        self.opp_taken_cards = opp_taken_cards
        self.my_points = my_points
        self.opp_points = opp_points
        self.last_taken_by = last_taken_by

    def get_legal_actions(self):
        '''
        Modify according to your game or
        needs. Constructs a list of all
        possible actions from current state.
        Returns a list.
        '''
        if self.whose_next_move == 1:
            legal_actions = [dict(card_index= i, card= card, whose_move_it_is= self.whose_next_move) for i,card in enumerate(self.my_cards)]
        else:
            legal_actions = [dict(card_index= i, card= card, whose_move_it_is= self.whose_next_move) for i, card in enumerate(self.opp_cards)]

        return legal_actions

    def is_game_over(self):
        '''
        Modify according to your game or
        needs. It is the game over condition
        and depends on your game. Returns
        true or false
        '''

        return self.my_points >= 101 or self.opp_points >= 101

    def game_result(self):
        '''
        Modify according to your game or
        needs. Returns 1 or 0 or -1 depending
        on your state corresponding to win,
        tie or a loss.
        '''
        if self.my_points > self.opp_points:
            return 1
        if self.my_points == self.opp_points:
            return 0
        if self.opp_points > self.my_points:
            return -1

    def new_state(self, whose_next_move):
        deck = shuffle_deck(create_deck())
        cards_on_table = deck[:4]
        deck = deck[4:]
        whose_next_move = 3 - whose_next_move
        my_cards, opponent_cards, deck = deal_cards(whose_next_move, self.deck)
        return  ZingGameState(deck, cards_on_table, whose_next_move, my_cards, opponent_cards, [], [], self.my_points, self.opp_points, 0)

    def print_state(self):
        print('---------------- State status: ------------------')
        print('Len deck:' + str(len(self.deck)))
        print('Cards on table: ')
        print_cards_inline(self.cards_on_table)
        print('Next to move: ' + str(self.whose_next_move))
        print('My cards are: ')
        print_cards_inline(self.my_cards)
        print('Opp cards are: ')
        print_cards_inline(self.opp_cards)
        print('Result')
        print('Me: ' + str(self.my_points) + ' | Opponent: ' + str(self.opp_points))

    def move(self, action: ZingGameAction):
        '''
        Modify according to your game or
        needs. Changes the state of your
        board with a new value. For a normal
        Tic Tac Toe game, it can be a 3 by 3
        array with all the elements of array
        being 0 initially. 0 means the board
        position is empty. If you place x in
        row 2 column 3, then it would be some
        thing like board[2][3] = 1, where 1
        represents that x is placed. Returns
        the new state after making a move.
        '''
        deck = self.deck
        cards_on_table = list()
        try:
            cards_on_table, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points = solve_move(self.cards_on_table,
                    action['card_index'], action['whose_move_it_is'],
                    self.my_cards, self.opp_cards, self.my_taken_cards, self.opp_taken_cards,
                    self.my_points, self.opp_points, False)
        except:
            cards_on_table = self.cards_on_table
            my_cards = self.my_cards
            opponent_cards = self.opp_cards
            my_taken_cards = self.my_taken_cards
            opp_taken_cards = self.opp_taken_cards
            my_points = self.my_points
            opp_points = self.opp_points
            # self.print_state()


        if len(cards_on_table) < len(self.cards_on_table):
            self.last_taken_by = action['whose_move_it_is']

        whose_next_move = 0
        if action['whose_move_it_is'] == 1:
            whose_next_move = 2
        else:
            whose_next_move = 1

        # check if cards need to be dealt
        if len(my_cards) == 0 and len(opponent_cards) == 0:
            if len(deck) > 0:
                print('Cards are dealt')
                my_cards, opponent_cards, deck = deal_cards(whose_next_move, self.deck)
            else:
                # deck needs to be reshuffled
                # also, we need to add 3 additional points to the player who took more cards in this round
                # and if the table is not empty, we also need to add it to the player that took last

                if len(cards_on_table) > 0:
                    cards_on_table, my_taken_cards, opp_taken_cards, my_points, opp_points = transfer_cards_and_points(
                        cards_on_table, self.last_taken_by, my_taken_cards, opp_taken_cards, my_points, opp_points)

                if len(my_taken_cards) > len(opp_taken_cards):
                    my_points += 3
                elif len(my_taken_cards) < len(opp_taken_cards):
                    opp_points += 3

                if (my_points < 101) and (opp_points < 101):
                    print('Deck got reshuffled')
                    deck = shuffle_deck(create_deck())
                    cards_on_table = deck[:4]
                    deck = deck[4:]
                    whose_next_move = 3 - whose_next_move
                    my_cards, opponent_cards, deck = deal_cards(whose_next_move, deck)
                else:
                    print('Game ended')
                    print(self.game_result())
                    # return self



        return  ZingGameState(deck, cards_on_table, whose_next_move, my_cards, opponent_cards, my_taken_cards, opp_taken_cards, my_points, opp_points, self.last_taken_by)




class MonteCarloTreeSearchNode():
    def __init__(self, state: ZingGameState, parent=None, parent_action=None):
        """
        state: It represents the state of the game. In our case it is an object consisting of:
            cards_on_table, whose_next_move, my_cards, opp_cards, my_taken_cards,
             opp_taken_cards, my_points, opp_points
        parent: It is None for the root node and for other nodes it is equal to the node it is derived from.
        children: It contains all possible actions from the current node.
        parent_action: None for the root node and for other nodes it is equal to the action which it’s parent carried out.
        _number_of_visits: Number of times current node is visited
        results: It’s a dictionary
        _untried_actions: Represents the list of all possible actions
        action: Move which has to be carried out.
        """
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return

    # Returns untried moves/actions at this position in the game
    def untried_actions(self):
        self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    # Returns the difference between wins and losses if this move is played
    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    # number of times we visited this position
    def n(self):
        return self._number_of_visits

    def expand(self):
        action = self._untried_actions.pop()
        next_state = self.state.move(action)
        child_node = MonteCarloTreeSearchNode(
            next_state, parent=self, parent_action=action)

        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_game_over()

    # From the current state, entire game is simulated till there is an outcome for the game.
    # This outcome of the game is returned. For example if it results in a win,
    # the outcome is 1. Otherwise it is -1 if it results in a loss. And it is 0 if it is a tie.
    # If the entire game is randomly simulated, that is at each turn the move is randomly selected out of set of possible moves, it is called light playout.
    def rollout(self):
        current_rollout_state = self.state

        while not current_rollout_state.is_game_over():
            possible_moves = current_rollout_state.get_legal_actions()
            # for pm in possible_moves:
            #     print(pm['card'])
            #
            # print('**************************')
            if len(possible_moves) > 0:
                action = self.rollout_policy(possible_moves)
                current_rollout_state = current_rollout_state.move(action)
            else:
                # print(current_rollout_state.my_cards)
                # print(current_rollout_state.opp_cards)
                # print(current_rollout_state.my_points)
                # print(current_rollout_state.opp_points)
                # print('************************')
                current_rollout_state = current_rollout_state.new_state(3 - current_rollout_state.whose_next_move)
                possible_moves = current_rollout_state.get_legal_actions()
                for pm in possible_moves:
                    print(pm)
                # action = self.rollout_policy(possible_moves)
                # current_rollout_state = current_rollout_state.move(action)

        print('Game result: ' )
        print(current_rollout_state.my_points)
        print(current_rollout_state.opp_points)
        return current_rollout_state.game_result()

    # In this step all the statistics for the nodes are updated. Untill the parent node is reached,
    # the number of visits for each node is incremented by 1.
    # If the result is 1, that is it resulted in a win, then the win is incremented by 1.
    # Otherwise if result is a loss, then loss is incremented by 1.
    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

    # All the actions are poped out of _untried_actions one by one. When it becomes empty,
    # that is when the size is zero, it is fully expanded.
    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    # Once fully expanded, this function selects the best child out of the children array.
    # The first term in the formula corresponds to exploitation and the second term corresponds to exploration.
    def best_child(self, c_param=0.1):
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self):
        current_node = self
        while not current_node.is_terminal_node():

            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        simulation_no = 100

        for i in range(simulation_no):
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)

        return self.best_child(c_param=0.)




