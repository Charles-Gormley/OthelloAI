from random import choice
from time import time

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

############################## Random Agent ##############################
class RandomAgent(game.Player):
    def __init__(self):
        super().__init__()

    def choose_move(self, state:State):
        moves = state.generateMoves()

        if moves:
            return choice(moves) # Randomly choose moves.
        else:
            return None

############################## Minimax Agent ##############################
class MinimaxAgent(game.Player):
    def __init__(self, depth):
        super().__init__()
        self.max_depth = depth

    def choose_move(self, state:State):
        moves = state.generateMoves()
        if not moves: # If there are no moves skip the move
            return None
        elif len(moves) == 1: # If there is just 1 move, choose that move.
            return moves[0]
        
        # Getting if the player is maximizing or not.
        maximizing_player = not state.nextPlayerToMove
        _, best_move = self.minimax_recursion(self.max_depth, 
                                              state, 
                                              maximizing_player)

        return best_move
    
    def minimax_recursion(self, depth:int, state:State, maximizing_player:bool) -> tuple:
        if state.game_over(): # Base case which will end recursion
            score = state.score()
            if score > 0:
                return (200, None)
            elif score < 0:
                return (-200, None)
            else:
                return(0, None)
        
        if depth <= 0: # Base case which will end recursion
            return (state.score(), None)
        
        moves = state.generateMoves()

        if maximizing_player:
            max_score = -1028
            max_move = None
            for move in moves:
                cur_score, _ = self.minimax_recursion(depth = depth-1, 
                                                      state = state.applyMoveCloning(move), 
                                                      maximizing_player=False)
                
                if max_score < cur_score:
                    max_score = cur_score
                    max_move = move
                
            return (max_score, max_move)
        
        elif not maximizing_player:
            min_score = 1028
            min_move = None
            for move in moves:
                cur_score, _ = self.minimax_recursion(depth = depth-1, 
                                                      state = state.applyMoveCloning(move), 
                                                      maximizing_player=True)
                
                if min_score > cur_score:
                    min_score = cur_score
                    min_move = move
            
            return (min_score, min_move)

############################## Alpha Beta Pruning ##############################
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
        _, best_move = self.alpha_beta_recursion(self.max_depth, 
                                                 state, 
                                                 maximizing_player, 
                                                 alpha = -1000, 
                                                 beta = 1000)

        return best_move
    
    def alpha_beta_recursion(self, 
                             depth:int, state:State, maximizing_player:bool, 
                             alpha:int, beta:int) -> tuple :
        if state.game_over():
            cur_score = state.score()
            if cur_score > 0:
                return (200, None)
            elif cur_score < 0:
                return (-200, None)
            
        if depth == 0:
            return (state.score(), None)
        
        moves = state.generateMoves()

        if maximizing_player:
            max_score = -1028
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
            min_score = 1028
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
        
##################### AlphaBeta+ ########################
def memoize(fn):
    cache = {}

    def hash_args(na, depth, state, maximizing_player, alpha, beta, *args, **kwargs):
        # Generate a hashable key based on selected function arguments
        hashed_state = hash(tuple(tuple(row) for row in state.board))
        key = (depth, hashed_state, maximizing_player, alpha, beta)
        return key

    def wrapper(na, depth, state, maximizing_player, alpha, beta, *args, **kwargs):
        key = hash_args(na, depth, state, maximizing_player, alpha, beta)

        if key in cache:
            # Return the result from the cache if it exists
            return cache[key]
        else:
            # Compute the result and store it in the cache
            result = fn(na, depth, state, maximizing_player, alpha, beta, *args, **kwargs)
            cache[key] = result
            return result

    return wrapper


class AlphaBetaPlus(game.Player):
    def __init__(self, timeout:int):
        super().__init__()
        self.timeout = timeout

        # Hyperparameters for Evaluation function
        self.edge_weight = 16
        self.danger_weight = 2
        self.base_weight = 1

    def choose_move(self, state:State):
        # 1. TIME PARAMETERS
        time_buffer = 5 # 5 Millisecond buffer to exit program, so we don't go over.
        self.end_time = round(time()*1000) + self.timeout - time_buffer

        # 2. Generating Moves & Checking Move Lengths
        moves = state.generateMoves()
        
        # If there are no moves which can be taken from given state we skip.
        if not moves:
            return None
        elif len(moves) == 1: # If there is only one move which can be taken we return that move.
            return moves[0]
        
        # 3. Current Player who this functions respective agent.
        # If the player is 1, they are X and they are minimizer. If player is 0, they are O and they are maximizer
        maximizing_player = not state.nextPlayerToMove

        best_move = None
        depth = 1
        max_depth = 20
        while True:
            _, depth_best_move, timeout = self.recursion(depth=depth, state=state, maximizing_player=maximizing_player, alpha=-1000, beta=1000)
            
            if not timeout: # Checking for time out. We can do this with our extensive timeout buffer.
                best_move = depth_best_move
                depth += 1
                if depth >= max_depth:
                    timeout = True
                
            
            if timeout or (round(time()*1000) >= self.end_time):
                if depth_best_move:
                    return depth_best_move
                elif best_move:
                    
                    return best_move
                else:
                    return choice(moves)

    
    
    @memoize 
    def recursion(self, depth:float, state:State, maximizing_player:bool, alpha:int, beta:int) -> tuple:
        if depth == 0:
            return (state.ceg98_extra_score(self.edge_weight, 
                                            self.danger_weight, 
                                            self.base_weight),
                                            None, False)
        
        if state.game_over():
            if state.score() > 0:
                return (1000, None, False)
            elif state.score() < 0:
                return (-1000, None, False)
        
        moves = state.generateMoves()

        if maximizing_player:
            max_score = -200
            max_move = None

            for move in moves:
                if round(time()*1000) >= self.end_time:
                    return (max_score, max_move, True)
                cur_score, _, _ = self.recursion(depth = depth-1, 
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

            return (max_score, max_move, False)
        
        elif not maximizing_player:
            min_score = 200
            min_move = None

            for move in moves:
                if round(time()*1000) >= self.end_time:
                    return (min_score, min_move, True)
                cur_score, _, _ = self.recursion(depth = depth-1, 
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

            return (min_score, min_move, False)