import time
import copy

BOARD_ROWS = 9
BOARD_COLS = 6
HUMAN = 'R'
AI = 'B'
CRIT_MASS = {(r,c): 4 - (r in (0,BOARD_ROWS-1)) - (c in (0,BOARD_COLS-1))
             for r in range(BOARD_ROWS) for c in range(BOARD_COLS)}

def parse_state(path='gamestate.txt'):
    with open(path) as f:
        header = f.readline().strip()
        board = []
        for _ in range(BOARD_ROWS):
            row = []
            for tok in f.readline().split():
                if tok=='0': row.append((0,None))
                else:
                    cnt=int(tok[:-1]); col=tok[-1]
                    row.append((cnt,col))
            board.append(row)
    return header, board


def write_state(header, board, path='gamestate.txt'):
    with open(path,'w') as f:
        f.write(f"{header}\n")
        for row in board:
            toks = [("0" if cnt==0 else f"{cnt}{col}") for cnt,col in row]
            f.write(" ".join(toks)+"\n")


def explode(board):
    changed=True
    while changed:
        changed=False
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                cnt,col=board[r][c]
                if cnt>=CRIT_MASS[(r,c)]:
                    changed=True
                    board[r][c]=(cnt-CRIT_MASS[(r,c)],col)
                    for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                        nr, nc = r+dr, c+dc
                        if 0<=nr<BOARD_ROWS and 0<=nc<BOARD_COLS:
                            ncnt,ncol=board[nr][nc]
                            board[nr][nc]=(ncnt+1, col)
        # conversion happens naturally by writing col
    return board


def get_legal_moves(board, player):
    moves=[]
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            cnt,col=board[r][c]
            if cnt==0 or col==player:
                moves.append((r,c))
    return moves


def apply_move(board, move, player):
    r,c = move
    cnt,col=board[r][c]
    board[r][c]=(cnt+1, player)
    return explode(board)


def game_over(board):
    seen = {col for _,col in sum(board,[])} - {None}
    return len(seen)<=1

# Heuristic 1: Orb difference
def h1(board, player):
    my = sum(cnt for cnt,col in sum(board,[]) if col==player)
    opp= sum(cnt for cnt,col in sum(board,[]) if col and col!=player)
    return my-opp

# Heuristic 2: Potential explosions
def h2(board, player):
    score=0
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            cnt,col=board[r][c]
            if col==player:
                score += (CRIT_MASS[(r,c)]-cnt)
    return -score

# Heuristic 3: Safe cells (not adjacent to opponent heavy cells)
def h3(board, player):
    safe=0
    opp = 'B' if player=='R' else 'R'
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            cnt,col=board[r][c]
            if col==player:
                adj = [(r+dr,c+dc) for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]]
                if all(not (0<=nr<BOARD_ROWS and 0<=nc<BOARD_COLS and board[nr][nc][1]==opp and board[nr][nc][0]>=CRIT_MASS[(nr,nc)])
                       for nr,nc in adj): safe+=1
    return safe

# Heuristic 4: Center control
def h4(board, player):
    center = (BOARD_ROWS//2, BOARD_COLS//2)
    cnt,col=board[center[0]][center[1]]
    return cnt if col==player else 0

# Heuristic 5: Frontier cells (cells at risk)
def h5(board, player):
    frontier=0
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            cnt,col=board[r][c]
            if col==player and cnt==CRIT_MASS[(r,c)]-1:
                frontier+=1
    return -frontier

# Combined heuristic
def evaluate(board, player):
    return (2*h1(board,player) + h2(board,player) + 0.5*h3(board,player)
            + h4(board,player) + h5(board,player))


def minimax(board, depth, alpha, beta, maximizing, player):
    if depth==0 or game_over(board):
        return evaluate(board, AI if maximizing else HUMAN), None
    best_action=None
    if maximizing:
        max_eval=-1e9
        for move in get_legal_moves(board, AI):
            newb=explode(copy.deepcopy(board))
            child=apply_move(newb, move, AI)
            val,_=minimax(child, depth-1, alpha, beta, False, player)
            if val>max_eval:
                max_eval=val; best_action=move
            alpha = max(alpha, val)
            if beta<=alpha: break
        return max_eval, best_action
    else:
        min_eval=1e9
        for move in get_legal_moves(board, HUMAN):
            newb=explode(copy.deepcopy(board))
            child=apply_move(newb, move, HUMAN)
            val,_=minimax(child, depth-1, alpha, beta, True, player)
            if val<min_eval:
                min_eval=val; best_action=move
            beta = min(beta, val)
            if beta<=alpha: break
        return min_eval, best_action


def run_engine():
    while True:
        header, board = parse_state()
        # only trigger AI after human has actually placed at least one orb
        if header.startswith('Human Move') and any(col == HUMAN for row in board for _,col in row):
            # compute AI move
            _, move = minimax(board, depth=3, alpha=-1e9, beta=1e9, maximizing=True, player=AI)
            if move is not None:
                newb = apply_move(board, move, AI)
                write_state('AI Move:', newb)
        time.sleep(1)

if __name__=='__main__':
    run_engine()