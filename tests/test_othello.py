import unittest

from othello.state_tracker import OthelloBoard
from othello.visualise import visualise_board


class OthelloTest(unittest.TestCase):

    def test_possible_moves(self):
        othello_board = OthelloBoard(board_size=8)
        new_board = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, 'w', 'w', 'b', None, None, None],
            [None, 'b', 'w', 'b', None, None, 'w', None],
            [None, 'w', 'b', None, 'b', None, 'b', None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
        ]
        for i in range(len(new_board)):
            for j in range(len(new_board[i])):
                othello_board.update_board(new_board[i][j], (i, j))

        possible_moves = othello_board.get_possible_moves(color="w")

        correct_possible_moves = [(4, 3), (2, 5), (5, 2), (3, 4), (3, 0), (5, 6), (2, 1), (4, 3)]

        self.assertEqual(possible_moves, correct_possible_moves, "Incorrect possible move evaluation")

if __name__ == '__main__':
    unittest.main()