import math
import random

import game
from othello import State


class ceg98(game.Player):
    def __init__(self, max_time):
        super().__init__()
        self.max_time = max_time

    def choose_move(self, state:State):
        moves = state.generateMoves()
        
        # If there are no moves which can be taken from given state we skip.
        if not moves:
            return None
        elif len(moves) == 1: # If there is only one move which can be taken we return that move.
            return moves[0]
        
        # If the player is 1, they are X and they are minimizer. If player is 0, they are O and they are maximizer
        maximizing_player = not state.nextPlayerToMove 

        _, best_move = self.recursion(self.max_depth, state, maximizing_player, alpha = -1000, beta = 1000)

        if best_move == None:
            return random.choice(moves)

        return best_move
    
    def recursion(self, depth:int, state:State, maximizing_player:bool, alpha:int, beta:int):
        if depth == 0:
            return (state.score(), None)
        
        if state.game_over():
            if state.score() > 0:
                return (1000, None)
            elif state.score() < 0:
                return (-1000, None)
                
        moves = state.generateMoves()

        if maximizing_player:
            max_score = -200
            max_move = None

            for move in moves:
                cur_score, _ = self.recursion(depth = depth-1, 
                                                         state = state.applyMoveCloning(move), 
                                                         maximizing_player=False,
                                                         alpha = alpha,
                                                         beta = beta)

                if max_score < cur_score:
                    max_score = cur_score
                    max_move = move

                alpha = max(alpha, cur_score)
                if beta <= alpha:
                    break

            return (max_score, max_move)
        
        elif not maximizing_player:
            min_score = 200
            min_move = None

            for move in moves:
                cur_score, _ = self.recursion(depth = depth-1, 
                                                         state = state.applyMoveCloning(move), 
                                                         maximizing_player=True,
                                                         alpha = alpha,
                                                         beta = beta)
                
                if min_score > cur_score:
                    min_score = cur_score
                    min_move = move

                beta = min(beta, cur_score)
                if beta <= alpha:
                    break

            return (min_score, min_move)