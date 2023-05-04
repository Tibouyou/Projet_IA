import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from connect4 import Connect4Game, Connect4Viewer, Connect4Console
from const import *
from tqdm import tqdm
import tkinter as tk

var = None
var2 = None
e1 = None
e2 = None


def show_entry_fields():
    global var, var2, e1, e2
    p1_algo = var.get()
    p2_algo = var2.get()
    p1_depth = int(e1.get())
    p2_depth = int(e2.get())
    print("Player 1 algorithm: ", p1_algo)
    print("Player 2 algorithm: ", p2_algo)
    print("Player 1 depth: ", p1_depth)
    print("Player 2 depth: ", p2_depth)
    play_game(p1_algo, p2_algo, p1_depth, p2_depth)

def play_game(p1, p2, depth1, depth2):
    game = Connect4Game(p1, p2, depth1, depth2)
    viewer = Connect4Viewer(game)
    

def main():
    global var, var2, e1, e2
    root = tk.Tk()
    root.title("Connect 4")

    tk.Label(root, 
            text="Player 1 : ").grid(row=0, column=0)

    
    var = tk.StringVar()
    var.set("minimax")
    R1 = tk.Radiobutton(root, text="Minimax", variable=var, value="minimax")
    
    R2 = tk.Radiobutton(root, text="Alphabeta", variable=var, value="alphabeta")
    

    R3 = tk.Radiobutton(root, text="MCTS", variable=var, value="mcts")
    
    R4 = tk.Radiobutton(root, text="Humain", variable=var, value="human")


    R1.grid(row=1, column=0)
    R2.grid(row=2, column=0)
    R3.grid(row=3, column=0)
    R4.grid(row=4, column=0)


    tk.Label(root, 
            text="Player 2 :").grid(row=0, column=1)
    
    var2 = tk.StringVar()
    var2.set("minimax")
    R5 = tk.Radiobutton(root, text="Minimax", variable=var2, value="minimax")
    
    R6 = tk.Radiobutton(root, text="Alphabeta", variable=var2, value="alphabeta")
    
    R7 = tk.Radiobutton(root, text="MCTS", variable=var2, value="mcts")
    
    R5.grid(row=1, column=1)
    R6.grid(row=2, column=1)
    R7.grid(row=3, column=1)

    
    tk.Label(root, 
            text="Profondeur player 1").grid(row=6, column=0)
    tk.Label(root, 
            text="Profondeur player 2").grid(row=7, column=0)

    e1 = tk.Entry(root)
    e2 = tk.Entry(root)

    e1.grid(row=6, column=1)
    e2.grid(row=7, column=1)

    tk.Button(root, 
            text='Quit', 
            command=root.quit).grid(row=8, 
                                        column=0, 
                                        sticky=tk.W, 
                                        pady=4)
    tk.Button(root, 
            text='Play', command=show_entry_fields).grid(row=8, 
                                                        column=1, 
                                                        sticky=tk.W, 
                                                        pady=4)
    
    tk.mainloop()

if __name__ == '__main__':
    main()