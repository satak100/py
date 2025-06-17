# Chain Reaction game engine with simple CLI and minimax AI

from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import List, Optional, Tuple

BOARD_ROWS = 9
BOARD_COLS = 6

Player = str  # 'R' or 'B'


def critical_mass(r: int, c: int) -> int:
    if (r == 0 or r == BOARD_ROWS - 1) and (c == 0 or c == BOARD_COLS - 1):
        return 2
    if r == 0 or r == BOARD_ROWS - 1 or c == 0 or c == BOARD_COLS - 1:
        return 3
    return 4


@dataclass
class Cell:
    owner: Optional[Player] = None
    count: int = 0

    def __str__(self) -> str:
        if self.owner is None or self.count == 0:
            return "0"
        return f"{self.count}{self.owner}"


@dataclass
class GameState:
    board: List[List[Cell]]
    player: Player  # player to move

    def clone(self) -> "GameState":
        return GameState(board=[[copy.copy(cell) for cell in row] for row in self.board], player=self.player)

    def switch_player(self):
        self.player = 'B' if self.player == 'R' else 'R'


def create_initial_state() -> GameState:
    board = [[Cell() for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return GameState(board=board, player='R')


def in_bounds(r: int, c: int) -> bool:
    return 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS


def neighbors(r: int, c: int) -> List[Tuple[int, int]]:
    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    return [(r + dr, c + dc) for dr, dc in deltas if in_bounds(r + dr, c + dc)]


def add_orb(state: GameState, r: int, c: int, player: Player):
    cell = state.board[r][c]
    if cell.owner not in (None, player):
        raise ValueError("Illegal move")
    cell.owner = player
    cell.count += 1
    if cell.count >= critical_mass(r, c):
        explode(state, r, c, player)


def explode(state: GameState, r: int, c: int, player: Player):
    cell = state.board[r][c]
    cell.count -= critical_mass(r, c)
    if cell.count <= 0:
        cell.count = 0
        cell.owner = None
    for nr, nc in neighbors(r, c):
        ncell = state.board[nr][nc]
        ncell.owner = player
        ncell.count += 1
        if ncell.count >= critical_mass(nr, nc):
            explode(state, nr, nc, player)


def legal_moves(state: GameState) -> List[Tuple[int, int]]:
    moves = []
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            cell = state.board[r][c]
            if cell.owner in (None, state.player):
                moves.append((r, c))
    return moves


def count_orbs(state: GameState, player: Player) -> int:
    return sum(cell.count for row in state.board for cell in row if cell.owner == player)


def evaluate(state: GameState, player: Player) -> int:
    # Simple heuristic: orb difference + corner control + mobility + center weight + stability
    opp = 'B' if player == 'R' else 'R'
    orb_diff = count_orbs(state, player) - count_orbs(state, opp)
    corner_score = sum(
        (1 if state.board[r][c].owner == player else 0) for r in [0, BOARD_ROWS - 1] for c in [0, BOARD_COLS - 1]
    )
    mobility = len([m for m in legal_moves(state) if state.board[m[0]][m[1]].owner in (None, player)])
    center = sum(
        (1 if state.board[r][c].owner == player else 0)
        for r in range(2, BOARD_ROWS - 2)
        for c in range(2, BOARD_COLS - 2)
    )
    stability = sum(
        (critical_mass(r, c) - state.board[r][c].count)
        for r in range(BOARD_ROWS)
        for c in range(BOARD_COLS)
        if state.board[r][c].owner == player
    )
    return orb_diff * 5 + corner_score * 3 + mobility + center * 2 + stability


def minimax(state: GameState, depth: int, alpha: int, beta: int, maximizing: bool, player: Player) -> Tuple[int, Tuple[int, int]]:
    if depth == 0 or not legal_moves(state):
        return evaluate(state, player), (-1, -1)

    best_move = (-1, -1)
    if maximizing:
        value = -float('inf')
        for move in legal_moves(state):
            next_state = state.clone()
            add_orb(next_state, move[0], move[1], state.player)
            next_state.switch_player()
            score, _ = minimax(next_state, depth - 1, alpha, beta, False, player)
            if score > value:
                value = score
                best_move = move
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return value, best_move
    else:
        value = float('inf')
        for move in legal_moves(state):
            next_state = state.clone()
            add_orb(next_state, move[0], move[1], state.player)
            next_state.switch_player()
            score, _ = minimax(next_state, depth - 1, alpha, beta, True, player)
            if score < value:
                value = score
                best_move = move
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value, best_move


def print_board(state: GameState):
    for r in range(BOARD_ROWS):
        row = " ".join(str(state.board[r][c]) for c in range(BOARD_COLS))
        print(row)


def human_move(state: GameState):
    while True:
        try:
            move = input(f"Player {state.player} move (row col): ")
            r, c = map(int, move.strip().split())
            if (r, c) in legal_moves(state):
                add_orb(state, r, c, state.player)
                state.switch_player()
                break
            else:
                print("Illegal move. Try again.")
        except Exception:
            print("Invalid input. Use: row col")


def ai_move(state: GameState, depth: int = 3):
    _, move = minimax(state, depth, -float('inf'), float('inf'), True, state.player)
    if move == (-1, -1):
        print("No moves available.")
        return
    print(f"AI plays {move}")
    add_orb(state, move[0], move[1], state.player)
    state.switch_player()


def main():
    state = create_initial_state()
    while True:
        print_board(state)
        if not legal_moves(state):
            state.switch_player()
            print(f"Player {state.player} wins!")
            break
        if state.player == 'R':
            human_move(state)
        else:
            ai_move(state)


if __name__ == "__main__":
    main()
