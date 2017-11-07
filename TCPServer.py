from socket import *
from random import randint as random

import sys
import time
import argparse

###########################################
serverPort = 707
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
###########################################

entireBoard = 0x1FF
singleSquare = [(0x100 >> i) for i in range(9)]

almostWinPairs = {0x180: singleSquare[0]+singleSquare[1]+singleSquare[2],
                  0x140: singleSquare[0]+singleSquare[1]+singleSquare[2],
                  0x0C0: singleSquare[0]+singleSquare[1]+singleSquare[2],
                  0x030: singleSquare[3]+singleSquare[4]+singleSquare[5],
                  0x028: singleSquare[3]+singleSquare[4]+singleSquare[5],
                  0x018: singleSquare[3]+singleSquare[4]+singleSquare[5],
                  0x006: singleSquare[6]+singleSquare[7]+singleSquare[8],
                  0x005: singleSquare[6]+singleSquare[7]+singleSquare[8],
                  0x003: singleSquare[6]+singleSquare[7]+singleSquare[8],
                  0x120: singleSquare[0]+singleSquare[3]+singleSquare[6],
                  0x104: singleSquare[0]+singleSquare[3]+singleSquare[6],
                  0x024: singleSquare[0]+singleSquare[3]+singleSquare[6],
                  0x090: singleSquare[1]+singleSquare[4]+singleSquare[7],
                  0x082: singleSquare[1]+singleSquare[4]+singleSquare[7],
                  0x012: singleSquare[1]+singleSquare[4]+singleSquare[7],
                  0x048: singleSquare[2]+singleSquare[5]+singleSquare[8],
                  0x041: singleSquare[2]+singleSquare[5]+singleSquare[8],
                  0x009: singleSquare[2]+singleSquare[5]+singleSquare[8]}
                  # There are more combo's (diagonals)

serverBoard = 0x000
clientBoard = 0x000

def chooseRandomMove(sBoard, cBoard):
    global entireBoard
    serverBoard = sBoard; clientBoard = cBoard

    # Check if game is over
    if ((serverBoard|clientBoard) & entireBoard) == entireBoard:
        return 'Game over'
    else:
        ttl = 50
        while(ttl > 0):
            temp = 0x100 >> random(0,8)
            if temp & (serverBoard|clientBoard) == 0:
                return (serverBoard|temp)
            ttt = ttl - 1
        return('Time out')

# Constructs a valid string from bitboards
def construct(serverBoard, clientBoard):
    board = [['-','-','-'],['-','-','-'],['-','-','-']]
    for row in range(3):
        if clientBoard & (0x100 >> (row*3)) > 0:
            board[row][0] = 'X'
        elif serverBoard & (0x100 >> (row*3)) > 0:
            board[row][0] = 'O'

        if clientBoard & (0x100 >> (row*3 + 1)) > 0:
            board[row][1] = 'X'
        elif serverBoard & (0x100 >> (row*3 + 1)) > 0:
            board[row][1] = 'O'

        if clientBoard & (0x100 >> (row*3 + 2)) > 0:
            board[row][2] = 'X'
        elif serverBoard & (0x100 >> (row*3 + 2)) > 0:
            board[row][2] = 'O'

    stringBoard = ''
    pipeCount = 2
    for row in board:
        for elem in row:
            stringBoard += elem
        if pipeCount > 0:
            stringBoard += '|'
            pipeCount -= 1

    stringBoard += '\n'
    return stringBoard

# This parses the response from server
# from string to bitboards
def deconstruct(board):
    serverBoard = 0x000
    clientBoard = 0x000
    if board.lower() == 'illegal':
        # Do something
        pass
    else:
        dec = board.split('|')
        if len(dec) > 3:
            raise Exception('Illegal')  # TODO: Do something else
        else:
            for i in range(3):
                if dec[i][0] == 'X':
                    clientBoard = clientBoard | (0x100 >> (i*3))
                if dec[i][1] == 'X':
                    clientBoard = clientBoard | (0x100 >> (i*3 + 1))
                if dec[i][2] == 'X':
                    clientBoard = clientBoard | (0x100 >> (i*3 + 2))

                if dec[i][0] == 'O':
                    serverBoard = serverBoard | (0x100 >> (i*3))
                if dec[i][1] == 'O':
                    serverBoard = serverBoard | (0x100 >> (i*3 + 1))
                if dec[i][2] == 'O':
                    serverBoard = serverBoard | (0x100 >> (i*3 + 2))
        return (serverBoard, clientBoard)

print 'The server is ready to receive'
connectionSocket, addr = serverSocket.accept()
while 1:
    time.sleep(2)
    clientResponse = connectionSocket.recv(2048)
    print(clientResponse)
    if 'illegal' in (clientResponse.lower()):
        connectionSocket.close()
    elif 'game over' in clientResponse.lower():
        print('Game over')
        connectionSocket.send('Game over')
        connectionSocket.close()
        break
    else:
        try:
            bitboards = deconstruct(clientResponse)
        except Exception:
            print('Illegal response')
            connectionSocket.send('Illegal response')
            connectionSocket.close()
            break
        else:
            serverBoard = bitboards[0]
            clientBoard = bitboards[1]

            # make move here
            serverBoard = chooseRandomMove(serverBoard, clientBoard)
            if serverBoard == 'Game over' or serverBoard == 'Time out':
                print(serverBoard)
                connectionSocket.send(serverBoard)
                connectionSocket.close()
                break
            else:
                stringBoard = construct(serverBoard, clientBoard)
                print(stringBoard)
                connectionSocket.send(stringBoard)

# connectionSocket.close()
