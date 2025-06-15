"""Minimax AI with alpha-beta pruning for Chain Reaction."""
from typing import Tuple, Optional
from board import Board
from heuristics import HEURISTICS


def minimax(board: Board, depth: int, alpha: float, beta: float, maximizing: bool, color: str, heuristic_name: str) -> Tuple[int, Optional[Tuple[int,int]]]:
    opp = 'B' if color == 'R' else 'R'
    if depth == 0 or board.is_terminal():
        value = HEURISTICS[heuristic_name](board, color)
        return value, None
    if maximizing:
        max_val = float('-inf')
        best_move = None
        for move in board.legal_moves(color):
            new_board = board.clone()
            new_board.apply_move(color, *move)
            val, _ = minimax(new_board, depth-1, alpha, beta, False, color, heuristic_name)
            if val > max_val:
                max_val = val
                best_move = move
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        return max_val, best_move
    else:
        min_val = float('inf')
        for move in board.legal_moves(opp):
            new_board = board.clone()
            new_board.apply_move(opp, *move)
            val, _ = minimax(new_board, depth-1, alpha, beta, True, color, heuristic_name)
            if val < min_val:
                min_val = val
            beta = min(beta, val)
            if beta <= alpha:
                break
        return min_val, None


def best_move(board: Board, color: str, depth: int = 3, heuristic: str = 'weighted') -> Tuple[int,int]:
    _, move = minimax(board, depth, float('-inf'), float('inf'), True, color, heuristic)
    return move
