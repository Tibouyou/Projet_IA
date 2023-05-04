import math
import random
#import numpy as np
from const import *


class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.score = 0

    def add_child(self, child_state):
        child = Node(child_state, self)
        self.children.append(child)
        return child

    def update(self, score):
        self.score += score
        self.visits += 1

    def fully_expanded(self):
        return len(self.children) == len(self.state.get_legal_moves())

    def __repr__(self):
        return f"{self.score / self.visits if self.visits != 0 else math.inf}, {self.score}, {self.visits}"


class MonteCarlo:
    def __init__(self, state):
        self.root = Node(state)

    def evaluate(self, board, player):
        score = 0
        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(board[r])]
            for c in range(COLUMN_COUNT - 3):
                window = row_array[c : c + 4]
                score += self.evaluate_window(window, player)

        for c in range(COLUMN_COUNT):
            col_array = [board[i][c] for i in range(ROW_COUNT)]
            for r in range(ROW_COUNT - 3):
                window = col_array[r : r + 4]
                score += self.evaluate_window(window, player)        

        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                window = [board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window, player)

        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                window = [board[r + 3 - i][c + i] for i in range(4)]
                score += self.evaluate_window(window, player)        
      
        return score
    
    def evaluate_window(self, window, piece):
        """
        Evaluates the score of a portion of the board
        :param window: portion of the board with all the pieces that have been placed
        :param piece: 1 or -1 depending on whose turn it is
        :return: score of the window
        """
        score = 0
        opp_piece = self.get_opponent(piece)
        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score -= 4

        return score
    
    def get_opponent(self, player):
        return 3 - player

    def search(self, num_iterations):
        for i in range(num_iterations):
            node = self.root
            state = self.root.state.copy()

            # selection
            while node.fully_expanded() and node.children:
                node = self.select_child(node)
                state.play_move(node.state.last_move)
                
            # expansion
            if not node.fully_expanded():
                move = random.choice(list(set(state.get_legal_moves()) - set([child.state.last_move for child in node.children])))
                if isinstance(move, tuple):
                    col = move[0]
                else:
                    col = move
                state.play_move(col)


                node = node.add_child(state)

            # simulation
            while not state.is_terminal() and state.get_legal_moves() != []:
                state.play_move(random.choice(state.get_legal_moves()))

            # backpropagation
            while node is not None:
                node.update(self.evaluate(state.board, self.root.state.current_player))
                node = node.parent

    def select_child(self, node):
        total_visits = sum(child.visits for child in node.children)
        ucb_scores = [self.ucb_score(child, total_visits) for child in node.children]
        return node.children[ucb_scores.index(max(ucb_scores))]

    def ucb_score(self, node, parent_visits):
        exploitation = node.score / node.visits if node.visits != 0 else math.inf
        exploration = math.sqrt(math.log(parent_visits) / node.visits) if node.visits != 0 else math.inf
        return exploitation + 2 * exploration

    def best_child(self):
        children = sorted(self.root.children, key=lambda child: child.visits, reverse=True)
        return self.select_child(self.root)


class MCTS:
    def __init__(self, player, profondeur):
        self.player = player
        self._profondeur = profondeur

    def get_move(self, state, player):
        mcts = MonteCarlo(state)
        mcts.search(self._profondeur)

        if self.player == 1:
            return mcts.best_child().state.last_move
        else:
            return mcts.best_child().state.last_move - 1
