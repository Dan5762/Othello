import json

from othello.state_tracker import OthelloBoard

if __name__ == "__main__":
    with open('config.json', 'r') as f:
        conf = json.load(f)

    othello_board = OthelloBoard(**conf)

    othello_board.run_game()

    