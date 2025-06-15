"""Heuristic evaluation functions for Chain Reaction."""
from board import Board


def orb_difference(board: Board, color: str) -> int:
    """Difference in total orb count."""
    opp = 'B' if color == 'R' else 'R'
    return board.count_orbs(color) - board.count_orbs(opp)


def mobility(board: Board, color: str) -> int:
    """Number of legal moves available."""
    return len(board.legal_moves(color))


def corner_control(board: Board, color: str) -> int:
    """Control of corner cells gives bonus."""
    corners = [(0,0), (0, board.cols-1), (board.rows-1,0), (board.rows-1, board.cols-1)]
    score = 0
    for r, c in corners:
        cell = board.get(r, c)
        if cell.color == color:
            score += 3
    return score


def critical_mass_distance(board: Board, color: str) -> int:
    """Preference for cells close to exploding."""
    total = 0
    for r in range(board.rows):
        for c in range(board.cols):
            cell = board.get(r, c)
            if cell.color == color:
                needed = board.critical_mass(r, c) - cell.count
                total -= needed  # fewer needed is better
    return total


def weighted_heuristic(board: Board, color: str) -> int:
    """Combine several heuristics."""
    return (
        3 * orb_difference(board, color)
        + mobility(board, color)
        + corner_control(board, color)
        + critical_mass_distance(board, color)
    )

HEURISTICS = {
    'orb_diff': orb_difference,
    'mobility': mobility,
    'corner': corner_control,
    'critical': critical_mass_distance,
    'weighted': weighted_heuristic,
}
