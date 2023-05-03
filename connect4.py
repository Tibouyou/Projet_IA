#import numpy as np
from const import *
import tkinter as tk
from minimax import Minimax
from mcts import MonteCarlo


class Connect4Game:

    def __init__(self,player1,player2):
        self.board = [[0 for j in range(COLUMN_COUNT)] for i in range(ROW_COUNT)]
        self.game_over = False
        self.current_player = PLAYER1_PIECE
        self.print_board()
        self.last_move = 0
        self._player1 = player1
        self._player2 = player2

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_location(self, col):
        return self.board[ROW_COUNT-1][col] == EMPTY

    def get_next_open_row(self, col):
        for r in range(ROW_COUNT):
            if self.board[r][col] == EMPTY:
                return r

    def print_board(self):
        print(self.board[::-1])

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
        return [col for col in range(COLUMN_COUNT) if self.is_valid_location(col)]

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
            if col < 0 or col >= COLUMN_COUNT:
                return False
        elif self._player2 == "mcts":
            if col is None:
                return False
        else:
            if col < 0 or col >= COLUMN_COUNT:
                return False

        if not self.is_valid_location(col):
            return False

        row = self.get_next_open_row(col)
        self.drop_piece(row, col, self.current_player)

        if self.winning_move(self.current_player):
            self.game_over = True

        self.current_player = PLAYER2_PIECE if self.current_player == PLAYER1_PIECE else PLAYER1_PIECE

        return True

                
class Connect4Console:
    
    def __init__(self,game):
        self.game = game
        self.minimax = Minimax(4)
        self.play()

    def play(self):
        while not self.game.game_over:
            if self.game.current_player == PLAYER1_PIECE:
                print("player 1")
                col = int(input("Player 1, enter your column choice (0-6): "))
            else:
                if (self.game._player2 == "mcts"):
                    monte_carlo = MonteCarlo(self.game, 1000)
                    exploration_parameter = 1.4
                    col = monte_carlo.monte_carlo_tree_search(self.game, exploration_parameter)
                elif (self.game._player2 == "minimax"):
                    col = self.minimax.get_best_move(self.game.board , self.game.current_player)
                else:
                    col = int(input("Player 2, enter your column choice (0-6): "))

            if self.game.is_valid_location(col):
                row = self.game.get_next_open_row(col)
                self.game.drop_piece(row, col, self.game.current_player)

                if self.game.winning_move(self.game.current_player):
                    self.game.game_over = True
                    self.game.print_board()
                    print("Player " + str(self.game.current_player) + " wins!")
                else:
                    self.game.current_player = PLAYER2_PIECE if self.game.current_player == PLAYER1_PIECE else PLAYER1_PIECE
                    self.game.print_board()

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
        
    def on_click(self, event):
        if not self.game.game_over:
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
            
    def draw_piece(self, row, col):
        x = col*SQUARE_SIZE + SQUARE_SIZE//2
        y = (ROW_COUNT - row - 1)*SQUARE_SIZE + SQUARE_SIZE//2
        color = PLAYER1_COLOR if self.game.current_player == PLAYER1_PIECE else PLAYER2_COLOR
        self.canvas.create_oval(x-PIECE_RADIUS, y-PIECE_RADIUS, x+PIECE_RADIUS, y+PIECE_RADIUS, fill=color)
        
    def toggle_player(self, player):
        return PLAYER2_PIECE if player == PLAYER1_PIECE else PLAYER1_PIECE
    
    def show_message(self, message):
        self.canvas.create_text(WIDTH//2, HEIGHT//2, text=message, fill="white", font=("Arial", 24))
