import math
import random

import game
from othello import State

class HumanPlayer(game.Player):

    def __init__(self):
        super().__init__()

    def choose_move(self, state):
        # generate the list of
        # moves:
        moves = state.generateMoves()

        for i, action in enumerate(moves):
            print('{}: {}'.format(i, action))
        response = input('Please choose a move: ')
        return moves[int(response)]

class RandomAgent(game.Player):
    def __init__(self):
        super().__init__()

    def choose_move(self, state):
        moves = state.generateMoves()

        if moves:
            return random.choice(moves)
        else:
            return None


class MinimaxAgent(game.Player):
    def __init__(self, depth):
        super().__init__()
        self.max_depth = depth

    def choose_move(self, state:State):

        moves = state.generateMoves()
        if not moves:
            return None
        elif len(moves) == 1:
            return moves[0]
        
        # Getting if the player is maximizing or not.
        maximizing_player = not state.nextPlayerToMove
        
        _, best_move = self.minimax_recursion(self.max_depth, state, maximizing_player, moves)


        if best_move == None:
            _, best_move = self.minimax_recursion(1, state, maximizing_player, moves)
            if best_move == None:
                return random.choice(moves)

        return best_move
    
    def minimax_recursion(self, depth:int, state:State, maximizing_player:bool, moves:list):
        if state.game_over():
            score = state.score()

            if score > 0:
                return (200, None)
            elif score < 0:
                return (-200, None)
            else:
                return(0, None)
        
        if depth == 0:
            return (state.score(), None)
        
        
        

        if maximizing_player:
            max_score = float("-inf")
            max_move = None
            for move in moves:
                next_state = state.applyMoveCloning(move)
                next_state_moves = next_state.generateMoves()
                if not next_state_moves:
                    continue

                cur_score, _ = self.minimax_recursion(depth = depth-1, 
                                                      state = next_state, 
                                                      maximizing_player=False,
                                                      moves = next_state_moves)
                
                if max_score < cur_score:
                    max_score = cur_score
                    max_move = move
                
            return (max_score, max_move)
        
        if not maximizing_player:
            min_score = float("inf")
            min_move = None
            for move in moves:
                next_state = state.applyMoveCloning(move)
                next_state_moves = next_state.generateMoves()
                if not next_state_moves:
                    continue

                cur_score, _ = self.minimax_recursion(depth = depth-1, 
                                                      state = next_state, 
                                                      maximizing_player=True, 
                                                      moves = next_state_moves)
                
                if min_score > cur_score:
                    min_score = cur_score
                    min_move = move
            
            return (min_score, min_move)


class AlphaBeta(game.Player):
    def __init__(self, depth):
        super().__init__()
        self.max_depth = depth

    def choose_move(self, state:State):
        moves = state.generateMoves()
        
        if not moves:
            return None
        elif len(moves) == 1:
            return moves[0]
        
        # Getting if the player is maximizing or not.
        maximizing_player = not state.nextPlayerToMove

        _, best_move = self.alpha_beta_recursion(self.max_depth, state, maximizing_player, alpha = -1000, beta = 1000)

        if best_move == None:
            _, best_move = self.alpha_beta_recursion(1, state, maximizing_player, alpha=-1000, beta = 1000)
            if best_move == None:
                return random.choice(moves)

        return best_move
    
    def alpha_beta_recursion(self, depth:int, state:State, maximizing_player:bool, alpha:int, beta:int):
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
                cur_score, _ = self.alpha_beta_recursion(depth = depth-1, 
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
                cur_score, _ = self.alpha_beta_recursion(depth = depth-1, 
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