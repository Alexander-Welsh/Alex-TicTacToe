from ParseObject import *
from random      import randint

class TicTacToe( ParseObject ):

    cells = [
        [0,0], [0,1], [0,2], 
        [1,0], [1,1], [1,2], 
        [2,0], [2,1], [2,2], 
    ]

    lines = [
        [ [0,0], [0,1], [0,2] ], # Row 0
        [ [1,0], [1,1], [1,2] ], # Row 1
        [ [2,0], [2,1], [2,2] ], # Row 2
        [ [0,0], [1,0], [2,0] ], # Col 0
        [ [0,1], [1,1], [2,1] ], # Col 1
        [ [0,2], [1,2], [2,2] ], # Col 2
        [ [0,0], [1,1], [2,2] ], # Diagonal
        [ [2,0], [1,1], [0,2] ], # Diagonal
    ]

    def __init__( self ):                                                             #[0][0] is top left [2][2] is bottom right

        self.square= [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
    
    def print_small( self ):

        for i in range(3):            
            print ' '.join([ '_' if s == ' ' else s for s in self.square[i] ])
        print

    def print_large( self ):

        print ' ' + self.square[0][0] + ' | ' + self.square[0][1] + ' | ' + self.square[0][2]    
        print '---+---+---'
        print ' ' + self.square[1][0] + ' | ' + self.square[1][1] + ' | ' + self.square[1][2]
        print '---+---+---'
        print ' ' + self.square[2][0] + ' | ' + self.square[2][1] + ' | ' + self.square[2][2]
        print
                
    def set(self,d,e,f): 
        
        if self.square[d][e] != ' ':
            return False
        self.square[d][e] = f
        return True

    def random_blank_cell( self ):

        blank_cells = [ cell for cell in TicTacToe.cells if self.square[ cell[0] ][ cell[1] ] == ' ' ]
        assert len( blank_cells ) != 0, 'random_blank_cell() was called when board was full - cannot do that!!'
        i = randint( 0, len( blank_cells ) - 1 )
        return blank_cells[ i ]

    def is_win(self):
    
        for line in TicTacToe.lines:
            s = self.square[ line[0][0] ][ line[0][1] ]
            if all([ self.square[ line[i][0] ][ line[i][1] ] == s for i in range(3) ]) and s != ' ': return True
        return False

    @staticmethod
    def test_save_game(a):
        
        g0 = TicTacToe()
        g0.game_name = a
        g0.square = ttt.square
        g0.commit()

    @staticmethod
    def load_game():

        for game in TicTacToe.query():
            print game.game_name

    @staticmethod    
    def loader(z):
        for game in TicTacToe.query():
            return game.game_name
        print ttt.get(game_name = 'afsd')
