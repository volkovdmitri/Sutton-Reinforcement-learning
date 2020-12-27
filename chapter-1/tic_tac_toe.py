class Board:

    def __init__(self):
        
        self.field = ['-']*9
        self.game_is_going = True
        self.is_tie = False    

    def draw(self):
        
        print(self.field[0]+' | '+self.field[1]+' | '+self.field[2])
        print('---------')
        print(self.field[3]+' | '+self.field[4]+' | '+self.field[5])
        print('---------')
        print(self.field[6]+' | '+self.field[7]+' | '+self.field[8])
    

    def row_end(self):

        if self.field[0]==self.field[1]==self.field[2]!='-':
            self.game_is_going = False
        
        if self.field[3]==self.field[4]==self.field[5]!='-':
            self.game_is_going = False
            
        if self.field[6]==self.field[7]==self.field[8]!='-':
            self.game_is_going = False

    
    def col_end(self):

        if self.field[0]==self.field[3]==self.field[6]!='-':
            self.game_is_going = False
        
        if self.field[1]==self.field[4]==self.field[7]!='-':
            self.game_is_going = False
            
        if self.field[2]==self.field[5]==self.field[8]!='-':
            self.game_is_going = False

    
    def diag_end(self):

        if self.field[0]==self.field[4]==self.field[8]!='-':
            self.game_is_going = False
        
        if self.field[2]==self.field[4]==self.field[6]!='-':
            self.game_is_going = False

    
    def tie(self):
        
        if '-' not in self.field:
            self.game_is_going = False
            self.is_tie = True

    def is_end(self):
        self.row_end()
        self.col_end()
        self.diag_end()
        self.tie()


class Player:
    
    def __init__(self):
        self.score = 0


    def make_move(self):
        self.mv = input('Make a move:')
        try: 
            self.mv = int(self.mv) - 1
        except ValueError:
            print('Wrong move')
            self.make_move()
        if self.mv not in range(9):
            print('Wrong move!')
            self.make_move()


class Game:
    
    def __init__(self, board, player, turn):

        self.board = board
        self.player = player
        self.turn = turn


    def play(self):

        self.board.draw()
        self.player.make_move()

        if self.board.field[self.player.mv] == '-':
            self.board.field[self.player.mv] = self.turn
            self.board.is_end()
            if self.turn == 'X':
                self.turn = 'O'
            else:
                self.turn = 'X'
        else:
            print('The cell is already occupied!')
            self.play()




if __name__ == '__main__':
    board = Board()
    player = Player()
    game = Game(board, player, 'X')

    while board.game_is_going:
        game.play()
    board.draw()
    print('The game is over!')
    if board.is_tie:
        print('Tie')
    elif game.turn == 'X':
        print('Player O has won')
    else:
        print('Player X has won')






