# Board representation and game logic for Chain Reaction
# Each cell may contain a stack of orbs belonging to Red (R) or Blue (B)
# When the stack reaches the cell's critical mass, it explodes to neighbors
from copy import deepcopy

class Cell:
    def __init__(self, count=0, color=None):
        self.count = count
        self.color = color  # 'R' or 'B' or None

    def is_empty(self):
        return self.count == 0

class Board:
    def __init__(self, rows=9, cols=6):
        self.rows = rows
        self.cols = cols
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]

    def clone(self):
        return deepcopy(self)

    def critical_mass(self, r, c):
        # Number of orthogonal neighbors
        neighbors = 4
        if r == 0 or r == self.rows - 1:
            neighbors -= 1
        if c == 0 or c == self.cols - 1:
            neighbors -= 1
        return neighbors

    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def get(self, r, c):
        return self.grid[r][c]

    def set(self, r, c, cell):
        self.grid[r][c] = cell

    def legal_moves(self, color):
        moves = []
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if cell.is_empty() or cell.color == color:
                    moves.append((r, c))
        return moves

    def apply_move(self, color, r, c):
        # Add orb and resolve chain reactions
        target = self.grid[r][c]
        if target.is_empty():
            target.color = color
        target.count += 1
        self._resolve_explosions([(r, c)])

    def _resolve_explosions(self, queue):
        while queue:
            r, c = queue.pop(0)
            cell = self.grid[r][c]
            if cell.count >= self.critical_mass(r, c):
                # explosion
                color = cell.color
                cell.count -= self.critical_mass(r, c)
                if cell.count == 0:
                    cell.color = None
                for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr, nc = r+dr, c+dc
                    if self.in_bounds(nr, nc):
                        neighbor = self.grid[nr][nc]
                        if neighbor.is_empty():
                            neighbor.color = color
                        else:
                            neighbor.color = color
                        neighbor.count += 1
                        if neighbor.count >= self.critical_mass(nr, nc):
                            queue.append((nr, nc))

    def count_orbs(self, color):
        total = 0
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if cell.color == color:
                    total += cell.count
        return total

    def is_terminal(self):
        red = self.count_orbs('R')
        blue = self.count_orbs('B')
        if red == 0 and blue == 0:
            return False  # empty board at start
        return red == 0 or blue == 0

    def winner(self):
        red = self.count_orbs('R')
        blue = self.count_orbs('B')
        if red == 0 and blue == 0:
            return None
        if red == 0:
            return 'B'
        if blue == 0:
            return 'R'
        return None

    @classmethod
    def from_lines(cls, lines):
        rows = len(lines)
        cols = len(lines[0].split())
        board = cls(rows, cols)
        for r, line in enumerate(lines):
            parts = line.strip().split()
            for c, token in enumerate(parts):
                if token == '0':
                    continue
                count = int(token[:-1])
                color = token[-1]
                board.grid[r][c].count = count
                board.grid[r][c].color = color
        return board

    def to_lines(self):
        lines = []
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                cell = self.grid[r][c]
                if cell.is_empty():
                    row.append('0')
                else:
                    row.append(f"{cell.count}{cell.color}")
            lines.append(' '.join(row))
        return lines

    def display(self):
        for line in self.to_lines():
            print(line)


