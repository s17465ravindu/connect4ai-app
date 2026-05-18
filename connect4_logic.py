import math
import time
import random

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 1
AI = 2
EMPTY = 0

TIME_LIMIT = 3


# ---------------- BOARD ----------------
def create_board():
    return [[0 for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]


def is_valid(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_valid_locations(board):
    return [c for c in range(COLUMN_COUNT) if is_valid(board, c)]


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def drop_piece(board, row, col, piece):
    board[row][col] = piece


# ---------------- WIN CHECK ----------------
def winning_move(board, piece):

    # Horizontal
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True

    # Vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True

    # Positive diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True

    # Negative diagonal
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True

    return False


def is_draw(board):
    return len(get_valid_locations(board)) == 0


# ---------------- HEURISTIC ----------------
def evaluate_window(window, piece):

    score = 0
    opp = PLAYER if piece == AI else AI

    if window.count(piece) == 4:
        score += 100

    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 8

    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 3

    if window.count(opp) == 3 and window.count(EMPTY) == 1:
        score -= 6

    return score


def score_position(board, piece):

    score = 0

    # Horizontal
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            window = [board[r+i][c] for i in range(4)]
            score += evaluate_window(window, piece)

    return score


# ---------------- MINIMAX ----------------
def minimax(board, depth, alpha, beta, maximizing):

    valid_locations = get_valid_locations(board)

    terminal = (
        winning_move(board, PLAYER)
        or winning_move(board, AI)
        or len(valid_locations) == 0
    )

    if depth == 0 or terminal:

        if winning_move(board, AI):
            return None, 100000

        elif winning_move(board, PLAYER):
            return None, -100000

        elif len(valid_locations) == 0:
            return None, 0

        return None, score_position(board, AI)

    # MAXIMIZING
    if maximizing:

        value = -math.inf
        best_col = random.choice(valid_locations)

        for col in valid_locations:

            row = get_next_open_row(board, col)
            temp = [r[:] for r in board]

            drop_piece(temp, row, col, AI)

            new_score = minimax(
                temp,
                depth - 1,
                alpha,
                beta,
                False
            )[1]

            if new_score > value:
                value = new_score
                best_col = col

            alpha = max(alpha, value)

            if alpha >= beta:
                break

        return best_col, value

    # MINIMIZING
    else:

        value = math.inf
        best_col = random.choice(valid_locations)

        for col in valid_locations:

            row = get_next_open_row(board, col)
            temp = [r[:] for r in board]

            drop_piece(temp, row, col, PLAYER)

            new_score = minimax(
                temp,
                depth - 1,
                alpha,
                beta,
                True
            )[1]

            if new_score < value:
                value = new_score
                best_col = col

            beta = min(beta, value)

            if alpha >= beta:
                break

        return best_col, value


# ---------------- AI DIFFICULTY ----------------
def get_ai_move(board, difficulty):

    valid_locations = get_valid_locations(board)

    # EASY
    if difficulty == "Easy":

        # 70% random
        if random.random() < 0.7:
            return random.choice(valid_locations)

        return minimax(board, 2, -math.inf, math.inf, True)[0]

    # MEDIUM
    elif difficulty == "Medium":

        # Some mistakes
        if random.random() < 0.25:
            return random.choice(valid_locations)

        return minimax(board, 4, -math.inf, math.inf, True)[0]

    # HARD
    else:

        start_time = time.time()
        best_col = random.choice(valid_locations)
        depth = 1

        while True:

            col, _ = minimax(
                board,
                depth,
                -math.inf,
                math.inf,
                True
            )

            if col is not None:
                best_col = col

            depth += 1

            if time.time() - start_time > TIME_LIMIT:
                break

        return best_col