import random
import time
import math
from copy import deepcopy
from const import *


class Node:
    def __init__(self, move, parent):
        self.move = move
        self.parent = parent
        self.N = float(0)
        self.Q = float(0)
        self.children = {}
        self.outcome = float(0)

    def add_children(self, children: dict) -> None:
        for child in children:
            self.children[child.move] = child

    def value(self, explore: float = EXPLORATION):
        if self.N == 0:
            return 0 if explore == 0 else float('inf')
        else:
            return float(self.Q) / float(self.N) + float(explore) * math.sqrt(math.log(float(self.parent.N)) / float(self.N))


class MCTS:
    def __init__(self, game, time_limit: float = 5):
        self.root_state = deepcopy(game)
        self.root = Node(None, None)
        self.run_time = time_limit
        self.node_count = 0
        self.num_rollouts = 0

    def select_node(self) -> tuple:
        node = self.root
        state = deepcopy(self.root_state)

        while len(node.children) != 0:
            children = node.children.values()
            max_value = max(children, key=lambda n: n.value()).value()
            max_nodes = [n for n in children if n.value() == max_value]

            node = random.choice(max_nodes)
            state.move(node.move)

            if node.N == 0:
                return node, state

        if self.expand(node, state):
            node = random.choice(list(node.children.values()))
            state.move(node.move)

        return node, state

    def expand(self, parent: Node, game) -> bool:
        if game.game_over_check():
            return False

        children = [Node(move, parent) for move in game.get_legal_moves()]
        parent.add_children(children)

        return True

        
    def roll_out(self, game) -> int:
        while not game.game_over_check():
            game.move(random.choice(game.get_legal_moves()))

        return self.get_outcome(game)

    def get_outcome(self, game) -> int:
        if len(game.get_legal_moves()) == 0 and self.check_win(game) == 0:
            return 3
        return 1 if self.check_win(game) == 1 else 2
    
    def check_win(self, game):
        # Check horizontal
        board = game.board
        player = game.current_player
        for row in range(ROW_COUNT):
            for col in range(COLUMN_COUNT-3):
                if board[row][col] == player and board[row][col+1] == player and board[row][col+2] == player and board[row][col+3] == player:
                    return True
        
        # Check vertical
        for row in range(ROW_COUNT-3):
            for col in range(COLUMN_COUNT):
                if board[row][col] == player and board[row+1][col] == player and board[row+2][col] == player and board[row+3][col] == player:
                    return True
        
        # Check diagonal (positive slope)
        for row in range(ROW_COUNT-3):
            for col in range(COLUMN_COUNT-3):
                if board[row][col] == player and board[row+1][col+1] == player and board[row+2][col+2] == player and board[row+3][col+3] == player:
                    return True
        
        # Check diagonal (negative slope)
        for row in range(3, ROW_COUNT):
            for col in range(COLUMN_COUNT-3):
                if board[row][col] == player and board[row-1][col+1] == player and board[row-2][col+2] == player and board[row-3][col+3] == player:
                    return True
        return False
    
    def back_propagate(self, node: Node, turn: int, outcome: int) -> None:

        # For the current player, not the next player
        reward = 0 if outcome == turn else 1

        while node is not None:
            node.N += 1
            node.Q += reward
            node = node.parent
            if outcome == 3:
                reward = 0
            else:
                reward = 1 - reward

    def search(self, time_limit: int):
        start_time = time.process_time()

        num_rollouts = 0
        while time.process_time() - start_time < time_limit:
            print("time: ",time.process_time()-start_time,"\tRollouts: ", num_rollouts)
            node, state = self.select_node()
            outcome = self.roll_out(state)
            self.back_propagate(node, state.current_player, outcome)
            num_rollouts += 1

        run_time = time.process_time() - start_time
        self.run_time = run_time
        self.num_rollouts = num_rollouts

    def best_move(self):
        if self.root_state.game_over_check():
            return -1

        max_value = max(self.root.children.values(), key=lambda n: n.N).N
        max_nodes = [n for n in self.root.children.values() if n.N == max_value]
        best_child = random.choice(max_nodes)

        return best_child.move

    def move(self, move):
        if move in self.root.children:
            self.root_state.move(move)
            self.root = self.root.children[move]
            return

        self.root_state.move(move)
        self.root = Node(None, None)

    def statistics(self) -> tuple:
        return self.num_rollouts, self.run_time

    def get_move(self, state, player):
        mcts = MCTS(state)
        mcts.search(0.1)
        return mcts.best_move()