"""Run AI vs AI matches for experimentation."""
from board import Board
from ai import best_move


def play_game(depth_a=2, depth_b=2, heuristic_a='weighted', heuristic_b='weighted'):
    board = Board()
    current = 'R'
    while not board.is_terminal():
        if current == 'R':
            move = best_move(board, 'R', depth=depth_a, heuristic=heuristic_a)
            if move is None:
                break
            board.apply_move('R', *move)
            current = 'B'
        else:
            move = best_move(board, 'B', depth=depth_b, heuristic=heuristic_b)
            if move is None:
                break
            board.apply_move('B', *move)
            current = 'R'
    return board.winner()

if __name__ == '__main__':
    winner = play_game()
    print('Winner:', winner)
