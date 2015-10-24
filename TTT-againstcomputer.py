from TTT import *

ParseObject.push_environment( 'development' )
ttt = TicTacToe()     #instantiating makes TicTacToe an object.         

while True:

    ###############################
	# Human moves as X
    ###############################

    XO = 'X'

    a = raw_input("Player " + str(XO) + ", please give two integers in range 0-2, save or load: ")

    if a.strip() == ('save'):
        x = raw_input("What would you like to save your game as? ")
        n =  x.strip()
        ttt.test_save_game(n)
        
    elif a.strip() == ('load'):
        ttt.load_game() 
        y = raw_input("Which game would you like to load? ")
        z = y.strip()
        ttt.loader(z)

    else:
        b = a.split(",")
        c = int(b[0])
        d = int(b[1])
        ttt.set(c,d, XO)

    ttt.print_small()

    r = ttt.is_win()
    if r == True: 
        print "Winner" 
        break

    ###############################
    # Computer moves as O
    ###############################

    cell = ttt.random_blank_cell()

    # Implement the move
    ttt.set( cell[0], cell[1], 'O' )
    print "I move", cell[0], cell[1]
    ttt.print_small()

    # Test for a 
    r = ttt.is_win()
    if r == True: 
        print "Winner" 
        break
