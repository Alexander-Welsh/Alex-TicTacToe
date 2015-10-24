

# from __future__  import unicode_literals
from ParseObject import *

#import json



class TicTacToe( ParseObject ):

    ParseObject.push_environment( 'development' )

    def __init__( self ):                                                             #[0][0] is top left [2][2] is bottom right
        self.square= [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
    
    #def save_game( self, filename):
     #    with open( filename, 'w' ) as outfile: json.dump( self.square, outfile )

    #def load_game( self, filename ):
    #    self.square = json.load( open( filename, 'r' ) )
        
        



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



    
        
        


        


           
        




            

        

    ''' Where do i want this to be inputted?  How?  Do I want it to be defined as integers, unique strings, objectID?'''


    # Staticmethod(noself), normal(self), Class method









        

       
        
              


        










ttt = TicTacToe()     #instantiating makes TicTacToe an object.         
#ttt.print_small()      #calling object on method.
#ttt.set(0,2, 'X')
#ttt.print_small()
# b = ttt.set()
"""ttt.print_small()
ttt.set(0,2,'L')
ttt.set(0,2, 'O')
a = ttt.set(0,2, 'L')
if a == False: print "Err Or?"

b = ttt.set(1,2, 'X')
ttt.set(1,2, 'N')

if b == False: print "Something"
ttt.print_small()

#ttt.print_large()
#ttt.set(1,2, 'x')
#ttt.print_large()
#ttt.print_large()
#ttt.set(0,0, 'X') 
#ttt.player2(0,1, "R")
#ttt.print_large()"""
'''

ttt.print_small()
ttt.set(0,2, 'X')
ttt.set(0,1, 'X')
ttt.set(0,0, 'X')

r = ttt.is_win()
if r == True: print "Wins"
if r == False: print "Fail"
#ttt.print_small()

#ttt.load_game('blahblah.ttt')
'''

while True:
    for XO in ['X', 'O']:

        
    
        a = raw_input("Player " + str(XO) + ", please give two integers in range 0-2, save or load: ")

        if a.strip() == ('save'):
            x = raw_input("What would you like to save your game as? ")
            n =  x.strip()
            ttt.test_save_game(n)
            break

            
        elif a.strip() == ('load'):
            ttt.load_game() 

            y = raw_input("Which game would you like to load? ")
            z = y.strip()
            ttt.loader(z)

            break

        

            break


        else:
            b = a.split(",")

        c = int(b[0])
        d = int(b[1])
        


        ttt.set(c,d, XO)
    

        r = ttt.is_win()

        if r == True: 
            ttt.print_small()
            print "Winner" 
            
            break
    
        if r == False: print "No Winner"
        
        ttt.print_small()

        
        
'''
        XO = "O" 
    
   
        a = raw_input("Player " + str(XO) + ", please give two integere in range 0-2: " )

        b = a.split(",")

        c = int(b[0])
        d = int(b[1])

        if a == a.strip('save'):
            ttt.save_game('blahblah.ttt')
        if a == a.strip('load'):
            ttt.load_game('blahblah.ttt')

        ttt.set(c,d, XO)
    

        r = ttt.is_win()

        if r == True:
            ttt.print_small() 
            print "Winner"
            break
    
        if r == False: print "No Winner"

        ttt.print_small() 
'''



    
