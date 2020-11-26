import json

from othello.state_tracker import OthelloGame

if __name__ == "__main__":
    with open('config.json', 'r') as f:
        conf = json.load(f)

    othello_game = OthelloGame(**conf)

    

    