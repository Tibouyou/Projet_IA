from connect4 import Connect4Game, Connect4Viewer, Connect4Console
from mcts import MonteCarlo
from const import *

def main():
    
    #choix si interface console ou graphique
    choix1 = int(input("Voulez-vous jouer en mode console ou graphique ? (1/2) : "))
    
    game = Connect4Game("humain","humain")

    if choix1 == 1 :
        console = Connect4Console(game)
    elif choix1 == 2 :
        viewer = Connect4Viewer(game)
    else :
        print("Erreur de saisie !")
        print("t'es bloated !")
        main()

if __name__ == '__main__':
    print("Bienvenue dans le jeu du puissance 4 !")
    main()

    """
    player1 = "human"
    player2 = "mcts"
    game = Connect4Game(player1, player2)
    console = Connect4Console(game)
    """
