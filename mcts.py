import random
import math

class MonteCarlo:
    
    def __init__(self, game, simulations_per_turn):
        self.game = game
        self.simulations_per_turn = simulations_per_turn

    def monte_carlo_tree_search(self, root_state, exploration_parameter):
        root_node = Node(state=root_state)
        for i in range(self.simulations_per_turn):
            node = root_node
            state = root_state.clone()

            # Selection
            while not node.is_terminal() and node.is_fully_expanded():
                node = self.select_child(node, exploration_parameter)
                action = node.parent_action
                state.do_move(action)

            # Expansion
            if not node.is_terminal():
                unexplored_actions = state.get_legal_moves()
                action = random.choice(unexplored_actions)
                state.do_move(action)
                node = node.add_child(action, state)

            # Simulation
            winner = self.simulate(state)

            # Backpropagation
            while node is not None:
                node.update(winner)
                node = node.parent

        # Choose the best action
        best_child = root_node.get_best_child()
        return best_child.parent_action

    def select_child(self, node, exploration_parameter):
        # Use the UCB1 formula to select a child node
        log_n = math.log(node.visit_count)
        child_scores = [
            (child.wins / child.visit_count) + exploration_parameter * math.sqrt(log_n / child.visit_count)
            for child in node.children
        ]
        return node.children[child_scores.index(max(child_scores))]

    def simulate(self, state):
        # Simulate a random game from the current state
        current_player = state.current_player
        while not state.is_terminal():
            legal_moves = state.get_legal_moves()
            move = random.choice(legal_moves)
            state.do_move(move)
        winner = state.get_winner()
        if winner is None:
            return 0
        elif winner == current_player:
            return 1
        else:
            return -1


class Node:

    def __init__(self, parent=None, parent_action=None, state=None):
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self.state = state
        self.wins = 0
        self.visit_count = 0

    def add_child(self, action, state):
        # Add a new child node
        child = Node(parent=self, parent_action=action, state=state)
        self.children.append(child)
        return child

    def is_fully_expanded(self):
        # Check if all possible child states are already explored
        return len(self.children) == len(self.state.get_legal_moves())

    def is_terminal(self):
        # Check if the current node is a terminal state
        return self.state.is_terminal()

    def get_best_child(self):
        # Get the child node with the highest win rate
        return max(self.children, key=lambda child: child.wins / child.visit_count)

    def update(self, result):
        # Update the node's win rate and visit count
        self.wins += result
        self.visit_count += 1
