import numpy as np

class Board:

    def __init__(self):
        self.cells = np.zeros((3, 3)) 
    

    def num_to_pic(self, x):
        if x == 1:
            return 'x'
        elif x == -1:
            return 'o'
        else: 
            return ' '

    def draw(self):
        print('- - -')
        print(self.num_to_pic(self.cells[0, 0]), self.num_to_pic(self.cells[0, 1]), \
                                                self.num_to_pic(self.cells[0, 2]))
        
        print('- - -')

        print(self.num_to_pic(self.cells[1, 0]), self.num_to_pic(self.cells[1, 1]), \
                                                self.num_to_pic(self.cells[1, 2]))
        print('- - -')

        print(self.num_to_pic(self.cells[2, 0]), self.num_to_pic(self.cells[2, 1]), \
                                                self.num_to_pic(self.cells[2, 2]))
        print('- - -')


class Move():
    
    def __init__(self, board):
        self.board = board

    def get_move(self):
        print('Enter row:')
        self.row_num = input()
        print('Enter column:')
        self.col_num = input()
   
    def make_move(self):
        self.board.cells[int(self.row_num), int(self.col_num)] = 1

def main():
    board = Board()
    move = Move(board)
    move.get_move()
    move.make_move()
    board.draw()


if __name__ == '__main__':
    main()

