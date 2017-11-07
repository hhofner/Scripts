from socket import *
from random import randint as random

import sys
import time
import argparse

################################
# Create connection with Server
serverAddress = ('localhost', 707)

clientSocket = socket(AF_INET, SOCK_STREAM)
try:
    clientSocket.connect(serverAddress)
except:
    print('Err: Socket not socketing')
###################################
# Cached Bitboards
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

# Returns bitboard pairs with new move, or win/loss
def chooseMove(sBoard, cBoard):
    # Convert board to bitboard
    serverBoard = sBoard
    clientBoard = cBoard

    # Check for winning move
    for almostW in almostWins:
        isValidMove = False
        if almostW & clientBoard >= 1:  # This finds possible winning move
            isValidMove = True
            # Make sure server hasn't put his piece there already
            for winS in winSequence:
                if ((~almostW & winS) & serverBoard) >= 1:
                    isValidMove = False
                    break
        if isValidMove:
            return 'move' # TODO: return some valid string thing
            break

# Returns only client bitboard
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
                return (clientBoard|temp)
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


# Make first move to server
clientBoard = chooseRandomMove(serverBoard, clientBoard)
stringBoard = construct(serverBoard, clientBoard)

# print(stringBoard)
# clientSocket.send(stringBoard)

# serverResponse = clientSocket.recv(1024)
# print(serverResponse)
first = True
while(1):
    print(stringBoard)
    time.sleep(2)
    if first:
        clientSocket.send(stringBoard)
        first = False
    time.sleep(2)
    try:
        serverResponse = clientSocket.recv(2048)
    except:
        print('Socket already closed')
        clientSocket.close()
    print(serverResponse)
    if 'illegal' in (serverResponse.lower()):
        clientSocket.close()
    elif 'game over' in serverResponse.lower():
        clientSocket.close()
        break
    else:
        try:
            bitboards = deconstruct(serverResponse)
        except Exception:
            clientSocket.send('Illegal response: must be of form '
            '---|---|--- with newline appended.')
            clientSocket.close()
            break
        else:
            serverBoard = bitboards[0]
            clientBoard = bitboards[1]

            # make move here
            clientBoard = chooseRandomMove(serverBoard, clientBoard)
            if clientBoard == 'Game over' or clientBoard == 'Time out':
                clientSocket.send(clientBoard)
                print(clientBoard)
                clientSocket.close()
                break
            else:
                stringBoard = construct(serverBoard, clientBoard)
                clientSocket.send(stringBoard)
