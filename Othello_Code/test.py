import agent
import othello
import game
import sys

initial_state = othello.State()

      
depth_or_time = 2

player1 = agent.extra(depth_or_time) # O
player2 = agent.AlphaBeta(depth_or_time) # X

# player1 = agent.HumanPlayer()
# player2 = agent.RandomAgent()

results = list()
for i in range(1, 4):
    control = 0
    for _ in range(100): # Play 100 games at each depth level.
        depth_or_time = i
        player1 = agent.extra(depth_or_time) # O
        player2 = agent.RandomAgent() # X

        session = game.Game(initial_state, player1, player2)
        session.play()

        if session.state.winner() == "O":
            control += 1
    
    results.append("* Depth " + str(i) + ": " + str(control) + "% Win Rate")

for result in results:
    print(result)
        

    
    