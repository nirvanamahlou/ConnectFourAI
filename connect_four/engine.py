import math
from game import ConnectFourGame, PLAYER, AI
from utils import evaluate_board
def get_valid_locations(game):
    return game.get_valid_locations()

def is_terminal_node(game):
    return game.is_draw() or game.winning_move(PLAYER) or game.winning_move(AI)

def minimax(game, depth, is_maximizing):
    valid_locations = get_valid_locations(game)
    if isTerminal := is_terminal_node(game):
        if game.winning_move(AI):
            return (None, math.inf)
        elif game.winning_move(PLAYER):
            return (None, -math.inf)
        else:
            return (None, 0)
    elif depth == 0:
        return (None, evaluate_board(game.board, AI if is_maximizing else PLAYER))

    if is_maximizing:
        value = -math.inf
        column = valid_locations[0]
        for c in valid_locations:
            r = game.get_next_open_row(c)
            game.drop_piece(r, c, AI)
            best_score = minimax(game, depth - 1, False)[1]
            game.board[r][c] = 0 
            if best_score > value:
                value = best_score
                column = c
    else:
        value = math.inf
        column = valid_locations[0]
        for c in valid_locations:
            r = game.get_next_open_row(c)
            game.drop_piece(r, c, PLAYER)
            best_score = minimax(game, depth - 1, True)[1]
            game.board[r][c] = 0  
            if best_score < value:
                value = best_score
                column = c

    return column, value

def alpha_beta_pruning(game, depth, alpha, beta, is_maximizing):
    valid_locations = get_valid_locations(game)
    if isTerminal := is_terminal_node(game):
        if game.winning_move(AI):
            return (None, math.inf)
        elif game.winning_move(PLAYER):
            return (None, -math.inf)
        else:
            return (None, 0)
    elif depth == 0:
        return (None, evaluate_board(game.board, AI if is_maximizing else PLAYER))
    if is_maximizing:
        value = -math.inf
        column = valid_locations[0]
        for c in valid_locations:
            r = game.get_next_open_row(c)
            game.drop_piece(r, c, AI)
            best_score = alpha_beta_pruning(game, depth - 1, alpha, beta, False)[1]
            game.board[r][c] = 0  

            if best_score > value:
                value = best_score
                column = c

            alpha = max(alpha, value)

            if alpha >= beta:
                break


    else:
        value = math.inf
        column = valid_locations[0]
        for c in valid_locations:
            r = game.get_next_open_row(c)
            game.drop_piece(r, c, PLAYER)
            best_score = alpha_beta_pruning(game, depth - 1, alpha, beta, True)[1]
            game.board[r][c] = 0  
            if best_score < value:
                value = best_score
                column = c

            beta = min(beta, value)
            if alpha >= beta:
                break

    return column, value


def expectimax(game, depth, is_maximizing):
    valid_locations = get_valid_locations(game)

    if isTerminal := is_terminal_node(game):
        if game.winning_move(AI):
            return (None, math.inf)
        elif game.winning_move(PLAYER):
            return (None, -math.inf)
        else:
            return (None, 0)
    elif depth == 0:
        return (None, evaluate_board(game.board, AI if is_maximizing else PLAYER))

    if is_maximizing:
        value = -math.inf
        column = valid_locations[0]

        for c in valid_locations:
            r = game.get_next_open_row(c)
            game.drop_piece(r, c, AI)
            best_score = expectimax(game, depth - 1, False)[1]
            game.board[r][c] = 0  

            if best_score > value:
                value = best_score
                column = c


    else:
        value = 0
        column = valid_locations[0]

        for c in valid_locations:
            r = game.get_next_open_row(c)
            game.drop_piece(r, c, PLAYER)
            best_score = expectimax(game, depth - 1, True)[1]
            game.board[r][c] = 0  

            value += best_score

        value /= len(valid_locations)  

    return column, value


