#EARIN Exercise 3 Andreas Kalavas, Kotopoulaki

import random
import numpy as np

h = [3, 2, 3, 2, 4, 2, 3, 2, 3]

def check(b):
    ans=2
    for i in b:
        if(i==-1):ans=-1

    if b[0]==b[1] and b[1]==b[2] and b[1]!=-1:
        ans=b[0]
    elif b[3]==b[4] and b[4]==b[5] and b[4]!=-1:
        ans=b[4]
    elif b[6]==b[7] and b[7]==b[8] and b[7]!=-1:
        ans=b[7]
    elif b[0]==b[3] and b[3]==b[6] and b[6]!=-1:
        ans=b[6]
    elif b[1] == b[4] and b[7] == b[4] and b[7] != -1:
        ans = b[7]
    elif b[2]==b[5] and b[5]==b[8] and b[5]!=-1:
        ans=b[5]
    elif b[0]==b[4] and b[4]==b[8] and b[8]!=-1:
        ans=b[4]
    elif b[2]==b[4] and b[4]==b[6] and b[6]!=-1:
        ans=b[6]
    return ans


def printboard(board):
    re = []
    for i in board:
        if (i == 1):
            re.append('O')
        elif (i == 0):
            re.append('X')
        else:
            re.append(' ')
    print(' ', re[0], '|', re[1], '|', re[2])
    print(' --- --- ---')
    print(' ', re[3], '|', re[4], '|', re[5])
    print(' --- --- ---')
    print(' ', re[6], '|', re[7], '|', re[8])


def minimax(b,d,xoro,maxmove,cutvalue):
    curr = 0
    winner=check(b)
    if(winner==2):d=0
    if(winner==(xoro+1)%2):
        return 25                                       #found winning state (for the computer)
    elif(winner==(xoro)%2):
        return -25                                      #found losing state (for the computer)
    for i in range(9):
        if (b[i] == xoro):
            curr -= h[i]
        elif (b[i] == (xoro + 1) % 2):
            curr += h[i]
    if (d == 0):
        return curr
    succ = []
    tempvalue=100
    if maxmove==1:
        tempvalue=-100
    for i in range(9):
        if (b[i] == -1):
            temp = b.copy()
            temp[i] = (maxmove + xoro) % 2
            newvalue=(minimax(temp, d - 1, xoro, (maxmove + 1) % 2,tempvalue))
            succ.append(newvalue)

            if(maxmove==0):                             #a-b pruning for min
                tempvalue=min(tempvalue,newvalue)
                if(tempvalue<cutvalue):
                    break
            else:                                       #a-b pruning for max
                tempvalue=max(tempvalue,newvalue)
                if(tempvalue>cutvalue):
                    break

    #print(succ)
    if (maxmove == 1): return np.max(succ)
    return np.min(succ)

def makemoveminimax(b,d,xoro,maxmove):
    curr=0
    for i in range(9):
        if(b[i]==xoro):curr-=h[i]
        elif(b[i]==(xoro+1)%2):curr+=h[i]
    succ=[]
    tempval=-100                                    #for a-b pruning
    for i in range(9):
        if(b[i]==-1):
            temp=b.copy()
            temp[i]=(maxmove+xoro)%2
            newvalue=minimax(temp,d-1,xoro,0,tempval)
            tempval=max(tempval,newvalue)
            succ.append([newvalue,i])
    #print(succ)
    return max(succ,key=lambda item: (item[0], -item[1]))


def game(start,d):
    finish=0
    board=[-1,-1,-1,-1,-1,-1,-1,-1,-1]
    st=start

    while finish==0:

        if(st==1):                                  #player's move
            r,c=input('Your move: ').split()
            r=int(r)
            c=int(c)
            pos=(r-1)*3+c-1
            while(board[pos]!=-1):
                r,c=input('This square is already marked, select a different one: ').split()
                r = int(r)
                c = int(c)
                pos=(r-1)*3+c-1
            board[pos]=start

        else:                                       #computer's move
            if d==0:
                pos=random.randint(0,8)
                while board[pos]!=-1:
                    pos = random.randint(0, 8)
            else:
                pos=makemoveminimax(board,d,start,1)[1]
            r=pos//3+1
            c=pos%3+1
            print('Computers move:',r,c)
            board[pos]=(start+1)%2

        st=(st+1)%2                                 #change player

        printboard(board)                           #print the board
        winner=check(board)                         #check if the game is over
        if winner!=-1:
            finish=1
            if(winner==2):print('WE HAVE A DRAW!!!')
            elif(winner==start):print('CONGRATULATIONS YOU WIN!!!')
            else:print('YOU LOST!!!')



##MAIN##
print('LET THE TIC TAC TOE GAME BEGIN...')
print('To make your move, write the row and the column of the square you wanna mark.')
print('The rows and columns are shown below:')
print('  1   2   3')
print('1   |   |')
print(' --- --- ---')
print('2   |   |')
print(' --- --- ---')
print('3   |   |')
cont=1
while cont==1:
    start=int(input('Do you want to play first? (1 for yes, 0 for no) '))
    d=int(input('Give the searching depth of the algorithm (>=0): '))
    print('LETS GOOOO')
    game(start,d)
    cont=int(input('Do you want to play again? (1 for yes, 0 for no) '))
print('THANK YOU FOR PLAYING!!! GOODBYE:)')