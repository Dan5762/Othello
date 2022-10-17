import tkinter as tk
import sys
import os
sys.path.insert(0, os.getcwd())

from othello.state_tracker import OthelloBoard


class Game(tk.Frame):
    def __init__(self, parent, rows=8, columns=8, size=64, cell_border=1, color="green", border_color='gray', vs_cpu=True, cpu_algorithm="greedy", player_idx=0):
        self.rows = rows
        self.columns = columns
        self.size = size
        self.cell_border = cell_border
        self.color = color
        self.border_color = border_color
        self.player_idx = player_idx
        self.player_colors = ['w', 'b']
        self.vs_cpu = vs_cpu
        self.cpu_algorithm = cpu_algorithm
        
        self.othello_board = OthelloBoard(opponent=self.cpu_algorithm)

        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background=self.border_color)
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        # this binding will cause a refresh if the user interactively
        # changes the window size
        self.canvas.bind("<Configure>", self.refresh)
        self.canvas.bind("<Button-1>", self.input_move)

    def input_move(self, event):
        # Get rectangle diameters
        col_width = self.canvas.winfo_width() / self.columns
        row_height = self.canvas.winfo_height() / self.rows
        # Calculate column and row number
        col = int(event.x // col_width)
        row = int(event.y // row_height)
        
        opponent_idx = (self.player_idx + 1) % 2

        if len(self.othello_board.get_possible_moves(self.player_colors[self.player_idx])) > 0 and self.othello_board.check_valid_position((row, col)):
            self.othello_board.invoke_move(self.player_colors[self.player_idx], (row, col))

            self.refresh(event=None)

        if len(self.othello_board.get_possible_moves(self.player_colors[opponent_idx])) > 0:
            if self.vs_cpu:
                cpu_move = self.othello_board.choose_cpu_move()
                self.othello_board.invoke_move(self.player_colors[opponent_idx], cpu_move)

                self.refresh(event=None)
            else:
                self.player_idx = opponent_idx

    def refresh(self, event, show_move_color=None):
        '''Redraw the board, possibly in response to window being resized'''
        if event is not None:
            xsize = int((event.width - 1) / self.columns)
            ysize = int((event.height - 1) / self.rows)
            self.size = min(xsize, ysize)
            self.canvas.delete("square")
        
        board = self.othello_board.get_board()
            
        for row in range(self.rows):
            for col in range(self.columns):
                x1 = (col * self.size) + self.cell_border
                y1 = (row * self.size) + self.cell_border
                x2 = x1 + self.size - (2 * self.cell_border)
                y2 = y1 + self.size - (2 * self.cell_border)

                if board[row][col] is None:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=self.color, tags="square")
                elif board[row][col] == 'w':
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill='white', tags="square")
                elif board[row][col] == 'b':
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill='black', tags="square")

        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")


if __name__ == "__main__":
    root = tk.Tk()
    board = Game(root)
    # board.prepare_initial_board()
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    root.mainloop()
