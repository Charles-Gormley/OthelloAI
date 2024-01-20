# OthelloAI
Othello AI agent which can play Othello through minimax trees or utilizing a Markov Decision Process I trained.
Video Demo: https://clipchamp.com/watch/hohux6Ai1Cp


# Minimax & Alpha Beta Pruning Example
https://www.youtube.com/watch?v=l-hh51ncgDI

# How to Run
1. Ensure you are working with python 3.7+
2. Change directory into the Othello_Code file
3. Run the python command: python main.py random random. This is two othello agents playing randomly. 
4. The other players you can play as are. Minimax, AlphaBeta, *human* and ab+ (alpha-beta plus).
5. When choosing minimax or alphabeta agents you can denote the level of depth they can go up to after the command. For example:
- python main.py minimax alphabeta 4.
- *This is a minimax and alphabeta agent playing against each other at depth 4 decision*
6. When playing as ab+ it accepts milliseconds as an integer. For example
* python main.py ab+ random 100
* - *This is a ab+ and random agent playing against each other with the ab+ agent having 100ms to make a decision.*
7. Player commands are {random, minimax, alphabeta, ab+}. Default depth is 3 for minimax and alphabeta. ab+ accepts the time in milliseconds to run.



## Agents
* Minimax - Implements minimax algorithm for 1 of the othello players.
* AlphaBeta - Implements alphabeta pruning algorithm from minimax for othello
* ab+ - Implements a alphabeta pruning alogithm with additional memoization and a more strategic evalution function and it runs based on time instead of depth.
* Random - Agent implements a move at random if there is a move avaiable, if not the agent passes its turn.

## Files
* game.py - This contains the game loop of othello
* othello.py - This contains the othello code.
* agent.py - This contains the code for all the agents.
* main.py - The main function which inits the game with the specified agents and depth level.
