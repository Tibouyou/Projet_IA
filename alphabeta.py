#import numpy as np
from copy import deepcopy
from const import *
from random import randint

class Alphabeta:
    def __init__(self, max_depth):
        self.max_depth = max_depth

    def get_move(self, game, player):        
        board = game.board
        valid_moves = self.get_valid_moves(board)
        best_move = None
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('+inf')

        for move in valid_moves:
            temp_board = deepcopy(board)
            self.make_move(temp_board, move, player)
            score = self.alphabeta(temp_board, self.max_depth, False, player, alpha, beta)
            #print(score,end="|")
            if score >= best_score:
                if score == best_score:
                    if randint(0,5) == 0:
                        best_move = move
                else:
                    best_score = score
                    alpha = score
                    best_move = move
        #print("")
        if best_move == None :
            if valid_moves == [] :
                game.game_over = True
                best_move = -1
            else :
                #print("best move is None, I lost. GG !")
                best_move = valid_moves[0]
        return best_move         

    def alphabeta(self, board, depth, tour_max, player, alpha, beta):
        if depth == 0 or self.is_terminal_node(board):
            return self.evaluate(board, player)

        valid_moves = self.get_valid_moves(board)
        
        if tour_max:
            
            best_score = float('-inf')
            
            for move in valid_moves:
                temp_board = deepcopy(board)
                self.make_move(temp_board, move, player)
                score = self.alphabeta(temp_board, depth-1, False, player, alpha, beta)
                best_score = max(score, best_score)
            
                if(score > beta):
                    return score
                
                if(score > best_score):
                    best_score = score
                    alpha = score
            
            return best_score
        
        else:

            best_score = float('+inf')

            for move in valid_moves:
                temp_board = deepcopy(board)
                self.make_move(temp_board, move, self.get_opponent(player))
                score = self.alphabeta(temp_board, depth-1, True, player, alpha, beta)

                if(score < alpha):
                    return score

                if(score < best_score):
                    best_score = score
                    beta = score

            return best_score

    def get_valid_moves(self, board):
        
        #return [col for col in range(COLUMN_COUNT) if board[ROW_COUNT-1][col] == 0]
        
        valid_moves = []
        if(board[ROW_COUNT-1][3] == 0):
            valid_moves.append(3)
        if(board[ROW_COUNT-1][2] == 0):
            valid_moves.append(2)
        if(board[ROW_COUNT-1][4] == 0):
            valid_moves.append(4)
        if(board[ROW_COUNT-1][1] == 0):
            valid_moves.append(1)
        if(board[ROW_COUNT-1][5] == 0):
            valid_moves.append(5)
        if(board[ROW_COUNT-1][0] == 0):
            valid_moves.append(0)
        if(board[ROW_COUNT-1][6] == 0):
            valid_moves.append(6)
        
        return valid_moves

        
        

    def make_move(self, board, move, player):
        row = self.get_next_open_row(board, move)
        board[row][move] = player

    def get_next_open_row(self, board, col):
        for row in range(0, ROW_COUNT-1, 1):
            if board[row][col] == 0:
                return row
        return -1

    def is_terminal_node(self, board):
        return self.check_win(board, 1) or self.check_win(board, 2) or len(self.get_valid_moves(board)) == 0

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


    def check_win(self, board, player):
        # Check horizontal
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

    def get_opponent(self, player):
        return 3 - player
    
    def evaluate_window(self, window, piece):
        """
        Evaluates the score of a portion of the board
        :param window: portion of the board with all the pieces that have been placed
        :param piece: 1 or -1 depending on whose turn it is
        :return: score of the window
        """
        opp_piece = self.get_opponent(piece)

        if window.count(EMPTY) > 2:
            return 0
        if window.count(piece) > 0 and window.count(opp_piece) > 0:
            return 0
        
        if window.count(EMPTY) == 2 :
            if window.count(piece) == 2:
                return 15
            else:
                return -15
        if window.count(EMPTY) == 1 :
            if window.count(piece) == 3:
                return 50
            else:
                return -50
            
        if window.count(piece) == 4:
            return float('inf')
        if window.count(opp_piece) == 4:
            return float('-inf')
        
        print("evaluate_window error")
        print(window)
        print(piece)
        return 0

    def print_type(self):
        print("alphabeta")



def printboard(board):
    print("printboard debug alphabeta : ")
    for i in range(6):
        for j in range(7):
            print(board[i][j], end="-")
        print("|")