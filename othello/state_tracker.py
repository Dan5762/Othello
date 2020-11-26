import random
from functools import reduce

import numpy as np

class OthelloBoard:

    def __init__(self, opponent="random", player_color="w", board_size=8):
        self.board_size = board_size

        self.board = [[None]*board_size for i in range(board_size)]
        self.board[int(board_size/2 - 1)][int(board_size/2 - 1)] = "w"
        self.board[int(board_size/2)][int(board_size/2)] = "w"
        self.board[int(board_size/2)][int(board_size/2 - 1)] = "b"
        self.board[int(board_size/2 - 1)][int(board_size/2)] = "b"

        self.opponent = opponent
        self.player_color = player_color
        self.cpu_color = (set(['w', 'b']) - set([player_color])).pop()
    
    def get_board(self):
        return self.board
    
    def update_board(self, update_value, position):
        self.board[position[0]][position[1]] = update_value
    
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
    
    def position_evaluater(self, position, color):
        """This function evaluates the possible moves of a specific position and color

        Args:
            position (tuple): The co-ordinates of the position
            color (str): "b" or "w"
        """
        opposing_color = (set(['w', 'b']) - set([color])).pop()

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        possible_moves = []
        for direction in directions:
            idx = 1
            new_position = (position[0] + direction[0] * idx, position[1] + direction[1] * idx)
            while self.check_valid_position(new_position) and self.board[new_position[0]][new_position[1]] == opposing_color:
                
                idx += 1
                new_position = (position[0] + direction[0] * idx, position[1] + direction[1] * idx)
            
            if idx > 1 and self.check_valid_position((new_position[0], new_position[1])) and self.board[new_position[0]][new_position[1]] == None:
                possible_moves.append(new_position)
        
        return possible_moves
    
    def check_valid_position(self, position):
        if len(self.board) > position[0] >= 0 and len(self.board) > position[1] >= 0:
            return True

    def choose_cpu_move(self):
        ## Move to a separate class
        if self.opponent == "random":
            possible_moves = self.possible_positions(self.cpu_color)

            if len(possible_moves) > 0:
                cpu_move = random.choice(possible_moves)
            else:
                cpu_move = None

            return cpu_move
    
    def invoke_move(self):
        pass


if __name__=="__main__":
    othello_game = OthelloGame()
    othello_game.possible_moves()