import argparse
from connect4 import Connect4Game, Connect4Viewer, Connect4Console
from mcts import MonteCarlo
from const import *

def main(interface, p1, p2, hide_board):
    game = Connect4Game(p1,p2)
    if interface == "graphique":
        viewer = Connect4Viewer(game)
    else:
        console = Connect4Console(game , hide_board)
        console.play()
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--interface", help="Interface à utiliser : console ou graphique", default="console")
    parser.add_argument("--p1", help="player 1 : minimax / alphabeta / mcts / human", default="minimax")
    parser.add_argument("--p2", help="player 2 : minimax / alphabeta / mcts / human", default="alphabeta")
    parser.add_argument("--hide_board", help="Afficher le plateau de jeu", action="store_false")

    args = parser.parse_args()
    
    main(args.interface, args.p1, args.p2, args.hide_board)

