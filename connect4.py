#import numpy as np
from copy import deepcopy
from const import *
import tkinter as tk
from minimax import Minimax
from alphabeta import Alphabeta
from mcts import MCTS
from human import Human

class Connect4Game:

    def __init__(self, player1, player2, depth1, depth2):
        self.board = [[0 for j in range(COLUMN_COUNT)] for i in range(ROW_COUNT)]
        self.game_over = False
        self.current_player = PLAYER1_PIECE
        self.last_move = 0
        
        if(player1 == "minimax"):
            self._player1 = Minimax(depth1)
            self._player1_type = "minimax"
        elif(player1 == "alphabeta"):
            self._player1 = Alphabeta(depth1)
            self._player1_type = "alphabeta"
        elif(player1 == "mcts"):
            self._player1 = MCTS(1)                            #TODO : ajouter les paramètres d'initialisation de MCTS
            self._player1_type = "mcts"
        else:
            self._player1 = Human("Player 1")
            self._player1_type = "human"
        
        if(player2 == "minimax"):
            self._player2 = Minimax(depth2)
            self._player2_type = "minimax"
        elif(player2 == "alphabeta"):
            self._player2 = Alphabeta(depth2)
            self._player2_type = "alphabeta"
        elif(player2 == "mcts"):
            self._player2 = MCTS(1)                              #TODO : ajouter les paramètres d'initialisation de MCTS
            self._player2_type = "mcts"
        else:
            self._player2 = Human("Player 2")
            self._player2_type = "human"

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece
        self.last_move = col

    def is_valid_location(self, col):
        return self.board[ROW_COUNT-1][col] == EMPTY

    def get_next_open_row(self, col):
        for r in range(ROW_COUNT):
            if self.board[r][col] == EMPTY:
                return r

    def print_board(self):
        printboard(self.board[::-1])

    def winning_move(self, piece):
        # Check horizontal locations for win
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(3, ROW_COUNT):
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
                    return True
                
    def get_current_player(self):
        return self.current_player

    def get_legal_moves(self):
        legal_moves = []
        for col in range(COLUMN_COUNT):
            if self.is_valid_location(col):
                legal_moves.append(col)
        return legal_moves


    def get_winner(self):
        if self.winning_move(PLAYER1_PIECE):
            return PLAYER1_PIECE
        elif self.winning_move(PLAYER2_PIECE):
            return PLAYER2_PIECE
        else:
            return None
        
    def play_move(self, col):
        """
        Joue un coup pour le joueur courant dans la colonne spécifiée.
        Retourne True si le coup a été joué avec succès, False sinon.
        """
        if self.game_over:
            return False

        if self.current_player == PLAYER1_PIECE:
            if not isinstance(col, int) or col < 0 or col >= COLUMN_COUNT:
                return False
        elif self._player2 == "mcts":
            if col is None:
                return False
        else:
            if not isinstance(col, int) or col < 0 or col >= COLUMN_COUNT:
                return False

        if not self.is_valid_location(col):
            return False

        row = self.get_next_open_row(col)
        self.drop_piece(row, col, self.current_player)

        if self.winning_move(self.current_player):
            self.game_over = True

        self.current_player = PLAYER2_PIECE if self.current_player == PLAYER1_PIECE else PLAYER1_PIECE

        return True

    def is_terminal(self):
    # Check if the current node is a terminal state
        board = deepcopy(self.board)
        # Check for horizontal win
        for row in range(len(board)):
            for col in range(len(board[0]) - 3):
                if board[row][col] != 0 and board[row][col] == board[row][col+1] == board[row][col+2] == board[row][col+3]:
                    return True
        # Check for vertical win
        for row in range(len(board) - 3):
            for col in range(len(board[0])):
                if board[row][col] != 0 and board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col]:
                    return True
        # Check for diagonal win (top left to bottom right)
        for row in range(len(board) - 3):
            for col in range(len(board[0]) - 3):
                if board[row][col] != 0 and board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3]:
                    return True
        # Check for diagonal win (bottom left to top right)
        for row in range(3, len(board)):
            for col in range(len(board[0]) - 3):
                if board[row][col] != 0 and board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3]:
                    return True
        # If none of the above conditions are met, the game is not over yet
        return False

    
    def copy(self):
        """
        Retourne une copie de l'objet.
        """
        game = Connect4Game(self._player1, self._player2, 0, 0)
        game.board = [row[:] for row in self.board]
        game.game_over = self.game_over
        game.current_player = self.current_player
        game.last_move = self.last_move
        return game

                
class Connect4Console:
    
    def __init__(self,game,show_board=True):
        self.game = game
        self._show_board = show_board
        self.play()

    def play(self):
        while not self.game.game_over:
            if self.game.current_player == PLAYER1_PIECE:
                col = self.game._player1.get_move(self.game, self.game.current_player) 
            else:
                col = self.game._player2.get_move(self.game, self.game.current_player)
            if self.game.is_valid_location(col):
                row = self.game.get_next_open_row(col)
                self.game.drop_piece(row, col, self.game.current_player)
                if self.game.winning_move(self.game.current_player):
                    self.game.game_over = True
                    if self._show_board:
                        self.game.print_board()
                        print("Player " + str(self.game.current_player) + " wins!")
                else:
                    self.game.current_player = PLAYER2_PIECE if self.game.current_player == PLAYER1_PIECE else PLAYER1_PIECE
                    if self._show_board:
                        self.game.print_board()
        return self.game.current_player

class Connect4Viewer:
    
    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("Connect 4")
        self.root.geometry("{}x{}".format(WIDTH, HEIGHT))
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        
        self.draw_board()
        
        self.root.mainloop()
        
    def draw_board(self):
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                x1 = c*SQUARE_SIZE
                y1 = r*SQUARE_SIZE
                x2 = x1 + SQUARE_SIZE
                y2 = y1 + SQUARE_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue")
                self.canvas.create_oval(x1, y1, x2, y2, fill="white")
                
        self.canvas.bind("<Button-1>", self.on_click)
        self.update()
        
    def update(self):
        liste_IA = ["minimax", "alphabeta", "mcts"]
        if self.game.current_player == 1:
            type_player = self.game._player1_type
        else:
            type_player = self.game._player2_type
        
        if not self.game.game_over:
            if type_player in liste_IA:
                # Current player is a bot, use AI to determine next move
                col = self.get_ai_move(type_player, self.game.current_player)
                self.root.after(500, lambda: self.play_ai_move(col))
        
        self.root.after(50, self.update)


    def on_click(self, event):
        liste_IA = ["minimax", "alphabeta", "mcts"]
        if self.game.current_player == 1:
            type_player = self.game._player1_type
        else:
            type_player = self.game._player2_type

        if not self.game.game_over:
            if type_player not in liste_IA:
                # Current player is human, get column from mouse click event
                col = event.x // SQUARE_SIZE
                
                if self.game.is_valid_location(col):
                    row = self.game.get_next_open_row(col)
                    self.game.drop_piece(row, col, self.game.current_player)
                    self.draw_piece(row, col)
                    
                    if self.game.winning_move(self.game.current_player):
                        self.game.game_over = True
                        self.show_message("Player {} wins!".format(self.game.current_player))
                    else:
                        self.game.current_player = self.toggle_player(self.game.current_player)
                        
    def get_ai_move(self, player, current_player):
        if player == "minimax":
            if current_player == 1:
                col = self.game._player1.get_move(self.game, self.game.current_player)
            else:
                col = self.game._player2.get_move(self.game, self.game.current_player)
        elif player == "alphabeta":
            if current_player == 1:
                col = self.game._player1.get_move(self.game, self.game.current_player)
            else:
                col = self.game._player2.get_move(self.game, self.game.current_player)
        elif player == "mcts":
            if current_player == 1:
                col = self.game._player1.get_move(self.game, self.game.current_player)
            else:
                col = self.game._player2.get_move(self.game, self.game.current_player)
              
        return col

    def play_ai_move(self, col):
        if self.game.is_valid_location(col):
            row = self.game.get_next_open_row(col)
            self.game.drop_piece(row, col, self.game.current_player)
            self.draw_piece(row, col)
            
            if self.game.winning_move(self.game.current_player):
                self.game.game_over = True
                self.show_message("Player {} wins!".format(self.game.current_player))
            else:
                self.game.current_player = self.toggle_player(self.game.current_player)
                
                if self.game.current_player == 2:
                    self.on_click(None)
            
    def draw_piece(self, row, col):
        x = col*SQUARE_SIZE + SQUARE_SIZE//2
        y = (ROW_COUNT - row - 1)*SQUARE_SIZE + SQUARE_SIZE//2
        color = PLAYER1_COLOR if self.game.current_player == PLAYER1_PIECE else PLAYER2_COLOR
        self.canvas.create_oval(x-PIECE_RADIUS, y-PIECE_RADIUS, x+PIECE_RADIUS, y+PIECE_RADIUS, fill=color)
        
    def toggle_player(self, player):
        return PLAYER2_PIECE if player == PLAYER1_PIECE else PLAYER1_PIECE
    
    def show_message(self, message):
        self.canvas.create_text(WIDTH//2, HEIGHT//2, text=message, fill="white", font=("Arial", 24))


def printboard(board):
    print("board : ")
    for i in range(6):
        for j in range(7):
            print(board[i][j], end="  ")
        print("")



