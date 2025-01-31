## Teammates:
Gavin Lebo 
Githika Annapureddy

## Modifications:
Our modifications to the modified MCTS was done by changing the rollout phase from completely random
to a heuristic function which prioritizes blocking winning moves from the opponent. This is implemented
through the blocks_opponent_win() function which checks if an action would block a players move, which then
would be played before any other action. 