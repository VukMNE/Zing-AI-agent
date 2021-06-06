from flask import Flask
from Heuristic import *
from flask import jsonify
from card import CardEncoder
from flask import request
from flask_cors import CORS, cross_origin
from monte_carlo import *


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/heuristic", methods=['POST'])
@cross_origin()
def heuristic():
    # deck = create_deck()
    # jdeck = list()
    # for card in deck:
    #     jdeck.append(CardEncoder().default(card))
    #
    # return jsonify(jdeck)
    body = request.json
    cards_on_table = transform_to_python_deck(body['cards_on_table'])
    my_cards = transform_to_python_deck(body['my_cards'])
    cards_already_played = transform_to_python_deck(body['cards_already_played'])
    deck = transform_to_python_deck(body['deck'])
    opponent_cards = transform_to_python_deck(body['opp_cards'])


    heuristic_score = heuristic_function(cards_on_table, my_cards, opponent_cards, 0.25, cards_already_played,
                                         deck)

    return jsonify(heuristic_score)

@app.route("/basic-heuristic", methods=['POST'])
@cross_origin()
def basic_h():
    body = request.json
    cards_on_table = transform_to_python_deck(body['cards_on_table'])
    my_cards = transform_to_python_deck(body['my_cards'])
    cards_already_played = transform_to_python_deck(body['cards_already_played'])
    deck = transform_to_python_deck(body['deck'])


    heuristic_score = basic_heuristic_function(cards_on_table, my_cards, 0.25, cards_already_played,
                                         deck)

    return jsonify(heuristic_score)

@app.route("/monte-carlo", methods=['POST'])
@cross_origin()
def monte_carlo_score():
    body = request.json
    cards_on_table = transform_to_python_deck(body['cards_on_table'])
    my_cards = transform_to_python_deck(body['my_cards'])
    cards_already_played = transform_to_python_deck(body['cards_already_played'])
    deck = transform_to_python_deck(body['deck'])

    my_taken_cards = transform_to_python_deck(body['my_taken_cards'])
    opp_taken_cards = transform_to_python_deck(body['opp_taken_cards'])
    opponent_cards = transform_to_python_deck(body['opp_cards'])
    whose_turn = body['whose_turn']


    my_points = body['my_points_in_round']
    opp_points = body['opp_points_in_round']
    my_total_points = body['my_points']
    opp_total_points = body['opp_points']
    last_taken_by = body['last_taken_by']
    print('My cards: ')
    print_cards_inline(my_cards)
    print(' Opponent has these cards ')
    print_cards_inline(opponent_cards)
    print('---------------------------------------------')

    s = time.time()
    mc_best_card = monte_carlo_best_card(10000, None, None, deck, cards_on_table, my_points, my_cards,
                          my_total_points, my_taken_cards, opp_points, opponent_cards, opp_total_points,
                          opp_taken_cards, whose_turn, last_taken_by)
    e = time.time()

    print('Time elapsed: ' + str(e - s))
    # print(mc_best_card)
    scores = np.zeros(len(my_cards))
    scores[mc_best_card] = 1
    print('Best card is:')
    print(mc_best_card)
    return jsonify(scores.tolist())


def transform_to_python_deck(deck_dict):
    cards = list()
    for d in deck_dict:
        cards.append(Card(d['number'], d['value'], d['sign']))

    return cards