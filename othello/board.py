import time
import tkinter as tk
import sys
import os
sys.path.insert(0, os.getcwd())

from othello.state_tracker import OthelloBoard


class GameBoard(tk.Frame):
    def __init__(self, parent, rows=8, columns=8, size=64, cell_border=1, color="green", border_color='black'):
        '''size is the size of a square, in pixels'''

        self.rows = rows
        self.columns = columns
        self.size = size
        self.cell_border = cell_border
        self.color = color
        self.border_color = border_color
        self.tiles = [[None] * self.columns for _ in range(self.rows)]
        self.tiles[int(self.rows / 2) - 1][int(self.columns / 2) - 1] = self.tiles[int(self.rows / 2)][int(self.columns / 2)] = 'w'
        self.tiles[int(self.rows / 2) - 1][int(self.columns / 2)] = self.tiles[int(self.rows / 2)][int(self.columns / 2) - 1] = 'b'

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

        othello_board = OthelloBoard(self.tiles)

        if othello_board.check_valid_position((row, col)):
            othello_board.invoke_move('w', (row, col))
            self.tiles = othello_board.get_board()

            self.refresh(event=None)

            cpu_move = othello_board.choose_cpu_move()
            othello_board.invoke_move('b', cpu_move)
            self.tiles = othello_board.get_board()

            self.refresh(event=None)

    def refresh(self, event):
        '''Redraw the board, possibly in response to window being resized'''
        if event is not None:
            xsize = int((event.width - 1) / self.columns)
            ysize = int((event.height - 1) / self.rows)
            self.size = min(xsize, ysize)
            self.canvas.delete("square")

        for row in range(self.rows):
            for col in range(self.columns):
                x1 = (col * self.size) + self.cell_border
                y1 = (row * self.size) + self.cell_border
                x2 = x1 + self.size - (2 * self.cell_border)
                y2 = y1 + self.size - (2 * self.cell_border)

                if self.tiles[row][col] is None:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=self.color, tags="square")
                elif self.tiles[row][col] == 'w':
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill='white', tags="square")
                elif self.tiles[row][col] == 'b':
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill='black', tags="square")

        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")


if __name__ == "__main__":
    root = tk.Tk()
    board = GameBoard(root)
    # board.prepare_initial_board()
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    root.mainloop()
