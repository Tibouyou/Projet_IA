from connect4 import Connect4Game, Connect4Viewer, Connect4Console
from mcts import MonteCarlo
from const import *

def main():
    
    #choix si interface console ou graphique
    choix = int(input("Voulez-vous jouer en mode console ou graphique ? (1/2) : "))
    game = Connect4Game("humain","minimax")
    if choix == 2:
        viewer = Connect4Viewer(game)
    else:
        console = Connect4Console(game)
        console.play()
        

if __name__ == '__main__':
    main()

    """player1 = "human"
    player2 = "mcts"
    game = Connect4Game(player1, player2)
    console = Connect4Console(game)"""
