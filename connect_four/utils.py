import numpy as np
import random
import pygame
import sys
import itertools
import math
from game import PLAYER, AI,ConnectFourGame
ROW_COUNT = 6
COLUMN_COUNT = 6
PLAYER = 0
AI = 1
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 4

def evaluate_board(window, piece):

    score = 0
    opponent_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opponent_piece = AI_PIECE

    if np.count_nonzero(window == piece)== 4:
        score += 100
    elif np.count_nonzero(window == piece) == 3 and np.count_nonzero(window == EMPTY) == 1:
        score += 50
    elif np.count_nonzero(window == piece)== 2 and np.count_nonzero(window == EMPTY)== 2:
        score += 10


    if np.count_nonzero(window == opponent_piece)== 3 and np.count_nonzero(window == EMPTY) == 1:
        score -= 75
    elif np.count_nonzero(window == opponent_piece)== 2 and np.count_nonzero(window == EMPTY)== 2:
        score -= 25
    elif np.count_nonzero(window == opponent_piece)== 4  : 
         score -= 100  

    return score

def score_position(board, piece, directions=(1, 1, 1, 1)):

    score = 0
    centerArray = [int(i) for i in list(board[ : , COLUMN_COUNT//2])]
    centerCount = centerArray.count(piece)
    score += centerCount*10

    if directions[0]:
        for r in range(ROW_COUNT):
            rowArray = [int(i) for i in list(board[r , : ])]
            for c in range(COLUMN_COUNT - 3):
                window = rowArray[c : c + WINDOW_LENGTH]
                score += evaluate_board(window, piece)

    if directions[1]:
        for c in range(COLUMN_COUNT):
            colArray = [int(i) for i in list(board[ : , c])]
            for r in range(ROW_COUNT):
                window = colArray[r : r + WINDOW_LENGTH]
                score += evaluate_board(window, piece)

    if directions[2]:
        for r, c in itertools.product(range(ROW_COUNT - 3), range(COLUMN_COUNT - 3)):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_board(window, piece)

    if directions[3]:
        for r, c in itertools.product(range(ROW_COUNT - 3), range(COLUMN_COUNT - 3)):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_board(window, piece)

    return score

def pick_best_move(board, piece, directions=(1, 1, 1, 1)):
    valid_locations = get_valid_locations(board)

    best_score = -10000
    best_col = random.choice(valid_locations)

    for c in valid_locations:
        r = get_next_open_row(board, c)
        temp_board = board.copy()
        drop_piece(temp_board, r, c, piece)
        score = score_position(temp_board, piece, directions)

        if score > best_score:
            best_score = score
            best_col = c

    return best_col
