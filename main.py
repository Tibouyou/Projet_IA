import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from connect4 import Connect4Game, Connect4Viewer, Connect4Console
from const import *
from tqdm import tqdm

def play_game(interface, p1, p2, hide_board, results):
    game = Connect4Game(p1, p2)
    if interface == "graphique":
        viewer = Connect4Viewer(game)
    else:
        console = Connect4Console(game, hide_board)
        winner = console.play()
        if winner == 1:
            results['player_1'] += 1
        elif winner == 2:
            results['player_2'] += 1

def play_games(args):
    # initialiser les résultats
    results = {'player_1': 0, 'player_2': 0}

    # créer une instance de ThreadPoolExecutor avec args.max_workers threads
    with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        # lancer plusieurs parties en parallèle
        futures = []
        for i in range(args.num_games):
            future = executor.submit(play_game, args.interface, args.p1, args.p2, args.hide_board, results)
            futures.append(future)
        
        # créer une barre de progression
        with tqdm(total=args.num_games) as pbar:
            # attendre que toutes les parties soient terminées
            for future in as_completed(futures):
                # mettre à jour la barre de progression
                pbar.update(1)
        
        # attendre la fin de toutes les tâches
        executor.shutdown()

    # afficher les résultats
    print(f"Nombre de victoires du joueur 1 ({args.p1}) : {results['player_1']} Win rate : {results['player_1']/args.num_games*100}%")
    print(f"Nombre de victoires du joueur 2 ({args.p2}) : {results['player_2']} Win rate : {results['player_2']/args.num_games*100}%")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--interface", help="Interface à utiliser : console ou graphique", default="console")
    parser.add_argument("--p1", help="player 1 : minimax / alphabeta / mcts / human", default="minimax")
    parser.add_argument("--p2", help="player 2 : minimax / alphabeta / mcts / human", default="alphabeta")
    parser.add_argument("--hide_board", help="Afficher le plateau de jeu", action="store_false")
    parser.add_argument("--num_games", help="Nombre de parties à jouer en même temps", type=int, default=1)
    parser.add_argument("--max_workers", help="Nombre de threads utilisé ", type=int, default=6)

    args = parser.parse_args()

    # lancer les parties en parallèle
    play_games(args)
