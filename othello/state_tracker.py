import random
from functools import reduce

import numpy as np

from othello.visualise import visualise_board

class OthelloBoard:

    def __init__(self, opponent="random", player_color="w", board_size=8):
        self.board_size = board_size

        self.board = [[None]*board_size for i in range(board_size)]
        self.board[int(board_size/2 - 1)][int(board_size/2 - 1)] = "w"
        self.board[int(board_size/2)][int(board_size/2)] = "w"
        self.board[int(board_size/2)][int(board_size/2 - 1)] = "b"
        self.board[int(board_size/2 - 1)][int(board_size/2)] = "b"

        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        self.opponent = opponent
        self.player_color = player_color
        self.cpu_color = (set(['w', 'b']) - set([player_color])).pop()
    
    def get_board(self):
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
            
            if idx > 1 and self.check_valid_position((new_position[0], new_position[1])) and self.board[new_position[0]][new_position[1]] == None:
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
        if self.opponent == "random":
            possible_moves = self.possible_positions(self.cpu_color)

            if len(possible_moves) > 0:
                cpu_move = random.choice(possible_moves)
            else:
                cpu_move = None

            return cpu_move

        else:
            raise Exception('Invalid opponent selected')
    
    def flip_evaluater(self, color, position):
        flips = []
        for direction in self.directions:
            idx = 1
            new_position = (position[0] + direction[0] * idx, position[1] + direction[1] * idx)

            path = []
            while self.check_valid_position(new_position) and self.board[new_position[0]][new_position[1]] == opposing_color:
                idx += 1
                new_position = (position[0] + direction[0] * idx, position[1] + direction[1] * idx)

                path.append((position[0] + direction[0] * idx, position[1] + direction[1] * idx))

            if idx > 1 and self.check_valid_position((new_position[0], new_position[1])) and self.board[new_position[0]][new_position[1]] == color:
                flips += path
            
        return flips
    
    def invoke_move(self, color, position):
        if position not in self.possible_positions(color):
            raise Exception('Invalid move')

        opposing_color = self.flip_color(color)

        flips = self.determine_flips(color, position)

        for (i, j) in flips:
            self.board[i][j] = color
    
    def run_game(self):
        move_color = 'w'

        no_move_check = 0
        while no_move_check < 2:    

            possible_moves = self.get_possible_moves(move_color)
            if len(possible_moves) > 0:

                if move_color == self.player_color:
                    visualise_board(self.board)
                else:
                    move_position = self.choose_cpu_move()
                    self.invoke_move(self.cpu_color, move_position)
            
            else:
                no_move_check += 1

            move_color = self.flip_color(move_color)
