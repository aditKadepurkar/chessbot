import math
from Board import Board
from ChessPiece import *
from functools import wraps
import random

def minimax(board, depth, alpha, beta, max_player, save_move, data, side): ## Getting expected value for each possible move

    if depth == 0 or board.is_terminal():
        data[1] = board.evaluate(side) ## exit
        return data

    if max_player: ## Test own move Max function
        max_eval = -math.inf
        for i in range(8):
            for j in range(8):
                if isinstance(board[i][j], ChessPiece) and board[i][j].color == side: ## For all peices that are of our color
                    piece = board[i][j]
                    moves = piece.filter_moves(piece.get_moves(board), board)
                    for move in moves:
                        board.make_move(piece, move[0], move[1], keep_history=True)
                        evaluation = minimax(board, depth - 1, alpha, beta, False, False, data,side)[1] ## Recersivley check all moves possible in this state
                        if save_move:
                            if evaluation >= max_eval:
                                if evaluation > data[1]:
                                    data.clear()
                                    data[1] = evaluation
                                    data[0] = [piece, move, evaluation]
                                elif evaluation == data[1]:
                                    data[0].append([piece, move, evaluation])
                        board.unmake_move(piece)
                        max_eval = max(max_eval, evaluation)
                        alpha = max(alpha, evaluation)
                        if beta <= alpha:
                            break
        return data
    else: ## Test other players move Mini function
        min_eval = math.inf
        for i in range(8):
            for j in range(8):
                if isinstance(board[i][j], ChessPiece) and board[i][j].color != side: ## For all peices that are of other color
                    piece = board[i][j]
                    moves = piece.get_moves(board)
                    for move in moves:
                        board.make_move(piece, move[0], move[1], keep_history=True)
                        evaluation = minimax(board, depth - 1, alpha, beta, True, False, data,side)[1] ## Recersivley check all moves possible in this state
                        board.unmake_move(piece)
                        min_eval = min(min_eval, evaluation)
                        beta = min(beta, evaluation)
                        if beta <= alpha:
                            break
        return data


def get_ai_move(board,side): ## MODIFY
    moves = minimax(board, board.depth, -math.inf, math.inf, True, True, [[], 0],side) ## Returns expected value of all moves
    # moves = [[pawn, move, move_score], [..], [..],[..], total_score]
    if len(moves[0]) == 0: ## Uh oh no possible moves
        return False
    best_score = max(moves[0], key=lambda x: x[2])[2] ## Get best score
    piece_and_move = random.choice([move for move in moves[0] if move[2] == best_score]) ## If two are equal then pick one randomly
    piece = piece_and_move[0]
    move = piece_and_move[1]
    if isinstance(piece, ChessPiece) and len(move) > 0 and isinstance(move, tuple):
        board.make_move(piece, move[0], move[1]) ## Make Move
    return True


def get_random_move(board):
    pieces = []
    moves = []
    for i in range(8):
        for j in range(8):
            if isinstance(board[i][j], ChessPiece) and board[i][j].color != board.get_player_color():
                pieces.append(board[i][j])
    for piece in pieces[:]:
        piece_moves = piece.filter_moves(piece.get_moves(board), board)
        if len(piece_moves) == 0:
            pieces.remove(piece)
        else:
            moves.append(piece_moves)
    if len(pieces) == 0:
        return
    piece = random.choice(pieces)
    move = random.choice(moves[pieces.index(piece)])
    if isinstance(piece, ChessPiece) and len(move) > 0:
        board.make_move(piece, move[0], move[1])
