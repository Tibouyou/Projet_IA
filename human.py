class Human:
    def __init__(self, name):
        self.name = name

    def get_move(self, board, player):
        print(self.name, " , it's your turn !")
        col = -1
        while (col<0 or col>6) or (not type(col) == int) :
            col = int(input( "enter your column choice (0-6): "))
        return col
    
    def print_type(self):
        print("Human")