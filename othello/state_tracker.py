import random
from functools import reduce

from othello.agents.minimax import run_minimax


class OthelloBoard:
    def __init__(self, opponent="random", player_color="w"):
        self.board = [[None] * 8 for _ in range(8)]
        self.board[3][3] = self.board[4][4] = 'w'
        self.board[3][4] = self.board[4][3] = 'b'

        self.directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

        self.opponent = opponent
        self.player_color = player_color
        self.cpu_color = (set(['w', 'b']) - set([player_color])).pop()

    def get_board(self, show_move_color=None):
        return self.board

    def update_board(self, update_value, position):
        self.board[position[0]][position[1]] = update_value

    def flip_color(self, color):
        return (set(['w', 'b']) - set([color])).pop()

    def position_evaluater(self, position, color):
        """This function evaluates the possible moves of a specific position and color

        Args:
            position (tuple): The co-ordinates of the position
            color (str): "b" or "w"
        """
        opposing_color = self.flip_color(color)

        possible_moves = []
        for direction in self.directions:
            idx = 1
            new_position = (position[0] + direction[0] * idx, position[1] + direction[1] * idx)

            while self.check_valid_position(new_position) and self.board[new_position[0]][new_position[1]] == opposing_color:
                idx += 1
                new_position = (position[0] + direction[0] * idx, position[1] + direction[1] * idx)

            if idx > 1 and self.check_valid_position((new_position[0], new_position[1])) and self.board[new_position[0]][new_position[1]] is None:
                possible_moves.append(new_position)

        return possible_moves

    def get_possible_moves(self, color):
        """This method gets the possible moves for the board state

        Args:
            color (str): The color for which possiible moves are determined

        Returns:
            possible_positions (list): The possible positions for the board state
        """
        positions = [[(i, j) for j in range(len(self.board[i])) if self.board[i][j] == color] for i in range(len(self.board))]
        positions = reduce(lambda x, y: x + y, positions)

        possible_moves = []
        for position in positions:
            possible_moves += self.position_evaluater(position, color)

        return possible_moves

    def check_valid_position(self, position):
        if len(self.board) > position[0] >= 0 and len(self.board) > position[1] >= 0:
            return True

    def choose_cpu_move(self):
        possible_moves = self.get_possible_moves(self.cpu_color)

        if self.opponent == "random":
            cpu_move = random.choice(possible_moves)

            return cpu_move

        elif self.opponent == "greedy":
            max_flips = 0
            for possible_move in possible_moves:
                flips = self.flip_evaluater(self.cpu_color, possible_move)

                if len(flips) > max_flips:
                    cpu_move = possible_move

            return cpu_move

        elif self.opponent == 'minimax':
            cpu_move = run_minimax(self, 'b', 4)
            print(cpu_move)
            return cpu_move

        else:
            raise Exception('Invalid opponent selected')

    def flip_evaluater(self, color, position):
        opposing_color = self.flip_color(color)

        flips = []
        for direction in self.directions:
            idx = 1
            new_position = (position[0] + direction[0] * idx, position[1] + direction[1] * idx)

            path = []
            while self.check_valid_position(new_position) and self.board[new_position[0]][new_position[1]] == opposing_color:
                path.append(new_position)

                idx += 1
                new_position = (position[0] + direction[0] * idx, position[1] + direction[1] * idx)

            if idx > 1 and self.check_valid_position((new_position[0], new_position[1])) and self.board[new_position[0]][new_position[1]] == color:
                flips += path

        return flips

    def invoke_move(self, color, position):
        if position not in self.get_possible_moves(color):
            raise Exception('Invalid move')

        flips = self.flip_evaluater(color, position)

        flips.append(position)

        for (i, j) in flips:
            self.board[i][j] = color

    def get_score(self, color):
        return sum([len([tile for tile in row if tile == color]) for row in self.board])
