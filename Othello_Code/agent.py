import math
import random

import game
from othello import State

class HumanPlayer(game.Player):

    def __init__(self):
        super().__init__()

    def choose_move(self, state):
        # generate the list of moves:
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

        try: 
            return random.choice(moves)
        except:
            return None


class MinimaxAgent(game.Player):
    def __init__(self, depth):
        super().__init__()
        self.max_depth = depth

    def choose_move(self, state):
        # generate the list of moves:

        # TODO: Get Player Type as boolean. 

        

        _, best_move = self.minimax_recursion(self.max_depth, state, maximizing_player)

        return best_move
    
    def minimax_recursion(self, depth:int, state:State, maximizing_player:bool):
        if depth == 0 or state.game_over():
            return state.score(), None
        
        moves = state.generateMoves()
        # TODO: Turn this into 1 if statement.

        # TODO: Code which catches if there is no available moves. 
        # Test if it runs properly.
        

        if maximizing_player:
            max_score = -100
            max_move = moves[0]
            for move in moves:
                cur_score, _ = self.minimax_recursion(depth = depth-1, 
                                                   state = state.applyMoveCloning(move), 
                                                   maximizing_player=False)
                if max_score < cur_score:
                    max_score = cur_score
                    max_move = move

            return max_score, max_move
        
        if maximizing_player:
            min_score = 100
            min_move = moves[0]
            for move in moves:
                cur_score, _ = self.minimax_recursion(depth = depth-1, 
                                                   state = state.applyMoveCloning(move), 
                                                   maximizing_player=True)
                if min_score < cur_score:
                    min_score = cur_score
                    min_move = move

            return min_score, min_move
        
                




class AlphaBeta(game.Player):
    pass