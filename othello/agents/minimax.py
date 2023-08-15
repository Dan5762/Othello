if __name__ == '__main__':
    import sys
    from os.path import dirname
    sys.path.append(dirname(dirname(__file__)))

import copy


def flip_color(color):
    return (set(['w', 'b']) - set([color])).pop()


def run_minimax(board_state, color, depth):
    pos_moves = board_state.get_possible_moves(color)

    move, best_move_idx = negamax(board_state, color, depth)

    return pos_moves[best_move_idx]


def negamax(board_state, color, depth):
    # print(f'Depth: {depth} Color: {color}')
    # for row in board_state.board:
    #     print([val if val is not None else ' ' for val in row ])

    if depth == 0 or terminal_test(board_state, color, depth):
        return board_state.get_score(color), 0

    value = -1e10
    best_move_idx = 0
    pos_moves = board_state.get_possible_moves(color)
    if len(pos_moves) > 0:
        for move_idx, pos_move in enumerate(pos_moves):
            board_state_copy = copy.deepcopy(board_state)
            color_copy = copy.deepcopy(color)
            board_state_copy.invoke_move(color, pos_move)
            new_value = -negamax(board_state_copy, flip_color(color_copy), depth - 1)[0]
            if new_value > value:
                best_move_idx = move_idx
                value = new_value
    else:
        board_state_copy = copy.deepcopy(board_state)
        color_copy = copy.deepcopy(color)
        new_value = -negamax(board_state_copy, flip_color(color_copy), depth - 1)[0]
        if new_value > value:
            value = new_value

    return value, best_move_idx


def terminal_test(board_state, color, depth):
    n_moves = board_state.get_possible_moves('w') + board_state.get_possible_moves('b')
    if n_moves == 0:
        return True
    else:
        return False


if __name__ == "__main__":
    from othello.state_tracker import OthelloBoard

    board = [[None] * 8 for _ in range(8)]
    board[3][3] = board[4][4] = 'w'
    board[3][4] = board[4][3] = 'b'

    othello_board = OthelloBoard()
    othello_board.board = board

    print('Running')
    move = run_minimax(othello_board, 'w', 4)
    print(f'Final Move: {move}')
