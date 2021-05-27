from flask import Flask
from Heuristic import *
from flask import jsonify
from card import CardEncoder
from flask import request
from flask_cors import CORS, cross_origin



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

    heuristic_score = heuristic_function(cards_on_table, my_cards, 0.25, cards_already_played,
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



def transform_to_python_deck(deck_dict):
    cards = list()
    for d in deck_dict:
        cards.append(Card(d['number'], d['value'], d['sign']))

    return cards