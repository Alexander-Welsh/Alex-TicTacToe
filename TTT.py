from ParseObject import *

class TicTacToe( ParseObject ):

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


    def is_win(self):
                    
        if self.square[0][0] == self.square[0][1] == self.square[0][2] != ' ': return True
        if self.square[1][0] == self.square[1][1] == self.square[1][2] != ' ': return True
        if self.square[2][0] == self.square[2][1] == self.square[2][2] != ' ': return True
        if self.square[0][0] == self.square[1][1] == self.square[2][2] != ' ': return True
        if self.square[2][0] == self.square[1][1] == self.square[0][2] != ' ': return True
        if self.square[0][0] == self.square[1][0] == self.square[2][0] != ' ': return True
        if self.square[0][1] == self.square[1][1] == self.square[2][1] != ' ': return True
        if self.square[0][2] == self.square[1][2] == self.square[2][2] != ' ': return True 
            
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
