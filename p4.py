# -*- coding: utf-8 -*-


#  _____                            _       
# |_   _|                          | |      
#   | |  _ __ ___  _ __   ___  _ __| |_ ___ 
#   | | | '_ ` _ \| '_ \ / _ \| '__| __/ __|
#  _| |_| | | | | | |_) | (_) | |  | |_\__ \
# |_____|_| |_| |_| .__/ \___/|_|   \__|___/
#                 | |                       
#                 |_|

import numpy as np


#     _____                _              _       
#    / ____|              | |            | |      
#   | |     ___  _ __  ___| |_ __ _ _ __ | |_ ___ 
#   | |    / _ \| '_ \/ __| __/ _` | '_ \| __/ __|
#   | |___| (_) | | | \__ \ || (_| | | | | |_\__ \
#    \_____\___/|_| |_|___/\__\__,_|_| |_|\__|___/

global D1, D2, Z #initiating global constants

#D1 and D2 are masks that will help extract diagonals
D1 = np.array([[False,False,False,True],
               [False,False,True,False],
               [False,True,False,False],
               [True,False,False,False]])

D2 = np.array([[True,False,False,False],
               [False,True,False,False],
               [False,False,True,False],
               [False,False,False,True]])

global res #total number of games
res = 0


#  ______                _   _                 
# |  ____|              | | (_)                
# | |__ _   _ _ __   ___| |_ _  ___  _ __  ___ 
# |  __| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
# | |  | |_| | | | | (__| |_| | (_) | | | \__ \
# |_|   \__,_|_| |_|\___|\__|_|\___/|_| |_|___/

def verif(M):
    '''
    checks if the game M has come to an end (either player won)

    Parameters
    ----------
    M : np.ndarray((n,n), dtype=int)
        The matrix representing a game. 
        0 has no token, 1 is a token from player 1, -1 is a token from player 2.

    Returns
    -------
    boolean
        Wether the game has ended. It is equivalent to saying that there is at
        least one alignement of four identical non-zero values.

    '''
    #going throught the matrix
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            if M[i,j]!=0 : #discarding cells where there are no tokens
                
                #checking the line
                if i<=M.shape[0]-4 :
                    if (M[i:i+4,j]==np.full(4, M[i,j])).all() :
                        return True
                
                #checking the column
                if j<=M.shape[1]-4 :
                    if (M[i,j:j+4]==np.full(4, M[i,j])).all() :
                        return True
                
                #checking the two diagonals using a numpy mask
                if i<=M.shape[0]-4 and j<=M.shape[1]-4 :
                    if (M[i:i+4,j:j+4][D1]==np.full(4, M[i,j])).all() :
                        return True
                    elif (M[i:i+4,j:j+4][D2]==np.full(4, M[i,j])).all() :
                        return True
    
    #if the program was never stopped, then there are no alignements found
    return False

def game(M, p=-1):
    '''
    simulation of every game of power4 possible. Backtracking when the programs achieves
    an end of the game.

    Parameters
    ----------
    M : np.ndarray((n,n), dtype=int)
        the matrix representing a game.
    p : int, optional
        This value is used to differentiate the players. It alternates between 1
        and -1. The default is -1 so that when the function is called for the first time,
        player 1 is starting.

    Returns
    -------
    None
        This "function" is actually a procedure that will increment the global variable
        "res" for each end reached, accounting for every possible game.

    '''
    if not verif(M) : #checking if the game has ended
        p*=-1 #swapping players
        for i in range(M.shape[0]): #a player selects a column
            if M[i,0]==0 : #if the column has at least one free slot then he can play it
                #searching the lowest position is the column
                a=0
                for j in range(M.shape[1]):
                    if M[i,j]==0 :
                        a+=1
                
                M[i, a-1] = p #playing the position
                game(M,p) #continuing the algorithm
                '''
                if we got out of the function, then it means we reached an end at some point,
                so we remove our token and try a different place.
                '''
                M[i, a-1] = 0 
        return
    
    else : #if one player won
        global res
        res+=1
        
        #only for monitoring
        if res%10000 == 0 :
            print(res)
            print(np.transpose(M))
            with open('result.txt', 'a') as f :
                    f.write(str(res))
        
        return


#  __  __       _ 
# |  \/  |     (_)
# | \  / | __ _ _ _ __
# | |\/| |/ _` | | '_ \ 
# | |  | | (_| | | | | |
# |_|  |_|\__,_|_|_| |_|
 
if __name__=='__main__':
    a,b = 7,6 #size of the board
    A = np.zeros((a,b), dtype=int)
    game(A)
    
    #saving the result at the end of the algorithm
    with open('result.txt', 'w') as f :
        f.write(str(res))
        

