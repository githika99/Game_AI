from mcts_node import MCTSNode
from p2_t3 import Board
from random import choice
from math import sqrt, log

num_nodes = 400
explore_faction = 2.0

def traverse_nodes(node: MCTSNode, board: Board, state, bot_identity: int):
    """ Traverses the tree until a terminal node or a node with untried actions is found. """
    while not node.untried_actions and not board.is_ended(state):
        node = max(node.child_nodes.values(), key=lambda child: ucb(child, child.parent_action[1] != bot_identity))
        state = board.next_state(state, node.parent_action)
    return node, state

def expand_leaf(node: MCTSNode, board: Board, state):
    """ Expands the tree by adding a new child node for the given node. """
    if not node.untried_actions:
        return node, state

    action = node.untried_actions.pop()
    next_state = board.next_state(state, action)
    child_node = MCTSNode(parent=node, parent_action=action, action_list=board.legal_actions(next_state))
    node.child_nodes[action] = child_node
    return child_node, next_state

def evaluate_action(board: Board, state, action, bot_identity: int, opponent_identity: int):
    """ Evaluates an action based on whether it leads to a win or blocks the opponent's win.

    Args:
        board: The game setup.
        state: The current game state.
        action: The action to evaluate.
        bot_identity: The identity of the bot.
        opponent_identity: The identity of the opponent.

    Returns:
        A score representing the quality of the action.
    """
    resulting_state = board.next_state(state, action)

    # Check if the action results in an immediate win for the bot
    if board.is_ended(resulting_state):
        return 1.0  # Maximum score for a winning move

    # Check if the action blocks the opponent's winning move
    for opponent_action in board.legal_actions(resulting_state):
        opponent_state = board.next_state(resulting_state, opponent_action)
        opp_points = board.points_values(opponent_state)
        if opp_points and opp_points.get(opponent_identity, 0) == 1:
            return 0.9  # High score for blocking the opponent

    # Default score for a non-critical move
    return 0.1

def rollout(board: Board, state):
    """ Performs a rollout by prioritizing moves based on evaluate_action.

    Args:
        board:  The game setup.
        state:  The current game state.

    Returns:
        The terminal game state after simulating the game.
    """
    current_state = state
    bot_identity = board.current_player(state)
    opponent_identity = 3 - bot_identity

    while not board.is_ended(current_state):
        legal_actions = board.legal_actions(current_state)

        # Use evaluate_action to score actions and pick the best one
        scored_actions = [(action, evaluate_action(board, current_state, action, bot_identity, opponent_identity)) for action in legal_actions]
        best_action = max(scored_actions, key=lambda x: x[1])[0]

        current_state = board.next_state(current_state, best_action)

    return current_state

def backpropagate(node: MCTSNode | None, won: bool):
    """ Updates the win and visit counts from the leaf node to the root. """
    while node is not None:
        node.visits += 1
        if won:
            node.wins += 1
        node = node.parent

def ucb(node: MCTSNode, is_opponent: bool):
    """ Calculates the UCB value with a heuristic-based exploration factor. """
    if node.visits == 0:
        return float('inf')
    exploitation = node.wins / node.visits
    if is_opponent:
        exploitation = 1 - exploitation
    exploration = explore_faction * sqrt(log(node.parent.visits) / node.visits)
    return exploitation + exploration

def get_best_action(root_node: MCTSNode):
    """ Selects the best action based on the highest win rate. """
    return max(root_node.child_nodes.items(), key=lambda item: item[1].wins / item[1].visits)[0]

def is_win(board: Board, state, identity_of_bot: int):
    """ Checks if the state is a win state for the bot. """
    outcome = board.points_values(state)
    assert outcome is not None, "is_win was called on a non-terminal state"
    return outcome[identity_of_bot] == 1

def think(board: Board, current_state):
    """ Performs MCTS with heuristic rollouts. """
    bot_identity = board.current_player(current_state)  # 1 or 2
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(current_state))

    for _ in range(num_nodes):
        state = current_state
        node = root_node

        # Selection
        node, state = traverse_nodes(node, board, state, bot_identity)

        # Expansion
        if node.untried_actions and not board.is_ended(state):
            node, state = expand_leaf(node, board, state)

        # Rollout
        final_state = rollout(board, state)

        # Backpropagation
        won = is_win(board, final_state, bot_identity)
        backpropagate(node, won)

    # Return the best action based on the root node's statistics
    best_action = get_best_action(root_node)
    print(f"Action chosen: {best_action}")
    return best_action
