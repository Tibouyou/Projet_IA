# dimensions de la grille de jeu
ROW_COUNT = 6
COLUMN_COUNT = 7

# dimensions des cercles de jetons
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE/2 - 5)

# couleurs
BLUE = "#0000FF"
BLACK = "#000000"
RED = "#FF0000"
YELLOW = "#FFFF00"

WIDTH = COLUMN_COUNT * SQUARE_SIZE
HEIGHT = ROW_COUNT * SQUARE_SIZE

EMPTY = 0
PLAYER1_PIECE = 1
PLAYER2_PIECE = 2
PLAYER1_COLOR = RED
PLAYER2_COLOR = YELLOW
PIECE_RADIUS = RADIUS



import math

class GameMeta:
    PLAYERS = {'none': 0, 'one': 1, 'two': 2}
    OUTCOMES = {'none': 0, 'one': 1, 'two': 2, 'draw': 3}
    INF = float('inf')
    ROWS = 6
    COLS = 7


class MCTSMeta:
    EXPLORATION = math.sqrt(2)