"""Simple command-line UI for Chain Reaction using file protocol."""
import os
import time
from board import Board
from ai import best_move

STATE_FILE = 'gamestate.txt'


def write_state(header: str, board: Board):
    lines = [header]
    lines += board.to_lines()
    with open(STATE_FILE, 'w') as f:
        f.write('\n'.join(lines))


def read_state() -> (str, Board):
    with open(STATE_FILE, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    header = lines[0]
    board = Board.from_lines(lines[1:])
    return header, board


def wait_for_human_move(board: Board, color: str):
    while True:
        header, board_state = read_state()
        if header.startswith('Human Move'):
            return board_state
        time.sleep(0.5)


def main():
    board = Board()
    current = 'R'  # human is Red
    write_state('Human Move:', board)
    while not board.is_terminal():
        header, board = read_state()
        if header.startswith('Human Move'):
            # AI turn
            move = best_move(board, 'B', depth=2)
            if move is None:
                print('AI resigns')
                return
            board.apply_move('B', *move)
            write_state('AI Move:', board)
            board.display()
        else:
            # wait for human to update the file
            board = wait_for_human_move(board, 'R')
    winner = board.winner()
    print('Winner:', winner)

if __name__ == '__main__':
    main()
