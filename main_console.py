import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from connect4 import Connect4Game, Connect4Viewer, Connect4Console
from const import *
from tqdm import tqdm

def play_game( p1, p2, hide_board, depth1, depth2, results):
    game = Connect4Game(p1, p2, depth1, depth2)
    console = Connect4Console(game, hide_board)
    winner = console.play()
    if winner == 1:
        results['player_1'] += 1
    elif winner == 2:
        results['player_2'] += 1

def play_games(args):
    
    # initialiser les résultats
    results = {'player_1': 0, 'player_2': 0}

    if(args.num_games == 1 or args.player_1 == "human" or args.player_2 == "human" or args.max_workers == 1 ):
        print ("Mode séquentiel")
        for i in range(args.num_games):
            play_game(args.player_1, args.player_2, args.hide_board, args.depth_player_1, args.depth_player_2, results)
    else:
        print ("Mode parallèle")
        # créer une instance de ThreadPoolExecutor avec args.max_workers threads
        with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
            # lancer plusieurs parties en parallèle
            futures = []
            for i in range(args.num_games):
                future = executor.submit(play_game, args.player_1, args.player_2, args.hide_board, args.depth_player_1, args.depth_player_2, results)
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
    print(f"Résultats (nb game = {args.num_games}) :")
    print(f"Nombre de victoires du joueur 1 ({args.player_1} = {args.depth_player_1}) : {results['player_1']} Win rate : {results['player_1']/args.num_games*100}%")
    print(f"Nombre de victoires du joueur 2 ({args.player_2} = {args.depth_player_2}) : {results['player_2']} Win rate : {results['player_2']/args.num_games*100}%")
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p1","--player_1", help="player 1 : minimax / alphabeta / mcts / human", default="minimax")
    parser.add_argument("-p2","--player_2", help="player 2 : minimax / alphabeta / mcts / human", default="alphabeta")
    parser.add_argument("-c" ,"--hide_board", help="Afficher le plateau de jeu", action="store_false")
    parser.add_argument("-n" ,"--num_games", help="Nombre de parties à jouer en même temps", type=int, default=1)
    parser.add_argument("-w" ,"--max_workers", help="Nombre de threads utilisé ", type=int, default=6)
    parser.add_argument("-d1","--depth_player_1", help="Profondeur de recherche du joueur 1", type=int, default=3)
    parser.add_argument("-d2","--depth_player_2", help="Profondeur de recherche du joueur 2", type=int, default=5)
    args = parser.parse_args()

    # lancer les parties en parallèle (ou pas selon les arguments)
    play_games(args)
