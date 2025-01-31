from mcts_node import MCTSNode
from p2_t3 import Board
from random import choice
from math import sqrt, log
from timeit import default_timer as time

num_nodes = 1000
explore_faction = 2.0

def traverse_nodes(node: MCTSNode, board: Board, state, bot_identity: int):
    while not node.untried_actions and not board.is_ended(state):
        node = max(node.child_nodes.values(), key=lambda child: ucb(child, child.parent_action[1] != bot_identity, board, state))
        state = board.next_state(state, node.parent_action)
    return node, state

def expand_leaf(node: MCTSNode, board: Board, state):
    if not node.untried_actions:
        return node, state
    
    action = node.untried_actions.pop()
    next_state = board.next_state(state, action)
    child_node = MCTSNode(parent=node, parent_action=action, action_list=board.legal_actions(next_state))
    node.child_nodes[action] = child_node
    return child_node, next_state

def rollout(board: Board, state):
    while not board.is_ended(state):
        actions = board.legal_actions(state)
        # Prefer actions that block the opponent's winning moves
        blocking_actions = [action for action in actions if blocks_opponent_win(board, state, action)]
        action = choice(blocking_actions) if blocking_actions else choice(actions)
        state = board.next_state(state, action)
    return state

def backpropagate(node: MCTSNode, won: bool):
    while node is not None:
        node.visits += 1
        if won:
            node.wins += 1
        node = node.parent

def ucb(node: MCTSNode, is_opponent: bool, board, state):
    if node.visits == 0:
        return float('inf')
    exploitation = node.wins / node.visits
    if is_opponent:
        exploitation = 1 - exploitation
    # Adjust UCB for moves that block the opponent
    blocking_bonus = 1.0 if blocks_opponent_win(board, state, node.parent_action) else 0.0
    exploration = explore_faction * sqrt(log(node.parent.visits) / node.visits)
    return exploitation + exploration + blocking_bonus

def get_best_action(root_node: MCTSNode):
    return max(root_node.child_nodes.items(), key=lambda item: item[1].wins / item[1].visits)[0]

def is_win(board: Board, state, identity_of_bot: int):
    outcome = board.points_values(state)
    assert outcome is not None, "is_win was called on a non-terminal state"
    return outcome[identity_of_bot] == 1

def blocks_opponent_win(board: Board, state, action):
    """Checks if the action prevents the opponent from winning in the next move."""
    opponent = 3 - board.current_player(state)  # Assuming players are 1 and 2
    next_state = board.next_state(state, action)
    
    for opponent_action in board.legal_actions(next_state):
        future_state = board.next_state(next_state, opponent_action)
        if board.is_ended(future_state):  # Only check terminal states
            outcome = board.points_values(future_state)
            if outcome and outcome[opponent] == 1:
                return True
    return False

def think(board: Board, current_state):
    bot_identity = board.current_player(current_state) # 1 or 2
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(current_state))

    for _ in range(num_nodes):
    # Uncomment for Time Limit
    # num_nodes = 0
    # start = time() # Should return 0.0 and start the clock.
    # while (True):
        state = current_state
        node = root_node

        # Traverse Nodes
        node, state = traverse_nodes(node, board, state, bot_identity)

        # Expansion
        if node.untried_actions and not board.is_ended(state):
            node, state = expand_leaf(node, board, state)

        # Rollout
        final_state = rollout(board, state)

        # Backpropagation
        won = is_win(board, final_state, bot_identity)
        backpropagate(node, won)

        # Uncomment for Time Limit
        # num_nodes += 1
        # time_elapsed = time() - start # This is in seconds.
        # if time_elapsed > .5:
        #     break

    best_action = get_best_action(root_node)
    print(f"MODIFIED Action chosen: {best_action}")
    return best_action
