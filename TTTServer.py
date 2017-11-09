#!/usr/bin/env python
"""
TCPServer.py:
Opens a "Tic Tac Toe Server" and plays through sending and
receiving strings of the form "---|---|---" with a connecting
"Tic Tac Toe Client".

Alpha-Beta Pruning implementation and Tic class design adapted from
Cecil Woebker's @ https://cwoebker.com/posts/tic-tac-toe

UNM Fall 2017
ECE 440: Computer Networks
Hans Hofner
"""

__author__ = "Hans Hofner, Cecil Woebker"

from socket import *


import sys
import time
import random
import signal
import argparse

###########################################
serverPort = 10000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
###########################################

class Tic(object):
    winning_combos = (
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6])

    winners = ('X-win', 'Draw', 'O-win')

    def __init__(self, squares=[]):
        if len(squares) == 0:
            self.squares = [None for i in range(9)]
        else:
            self.squares = squares

    def show(self):
        stringBoard = ''
        counter = 1
        for element in self.squares:
            if counter == 4 or counter == 8:
                stringBoard += '|'
                counter += 1
            if element == None:
                stringBoard += '-'
                counter += 1
            elif element == 'X':
                stringBoard += 'X'
                counter += 1
            elif element == 'O':
                stringBoard += 'O'
                counter += 1
        stringBoard += '\n'
        return stringBoard

    def available_moves(self):
        """what spots are left empty?"""
        return [k for k, v in enumerate(self.squares) if v is None]

    def available_combos(self, player):
        """what combos are available?"""
        return self.available_moves() + self.get_squares(player)

    def complete(self):
        """is the game over?"""
        if None not in [v for v in self.squares]:
            return True
        if self.winner() != None:
            return True
        return False

    def X_won(self):
        return self.winner() == 'X'

    def O_won(self):
        return self.winner() == 'O'

    def tied(self):
        return self.complete() == True and self.winner() is None

    def winner(self):
        for player in ('X', 'O'):
            positions = self.get_squares(player)
            for combo in self.winning_combos:
                win = True
                for pos in combo:
                    if pos not in positions:
                        win = False
                if win:
                    return player
        return None

    def get_squares(self, player):
        """squares that belong to a player"""
        return [k for k, v in enumerate(self.squares) if v == player]

    def make_move(self, position, player):
        """place on square on the board"""
        self.squares[position] = player

    def alphabeta(self, node, player, alpha, beta):
        if node.complete():
            if node.X_won():
                return -1
            elif node.tied():
                return 0
            elif node.O_won():
                return 1
        for move in node.available_moves():
            node.make_move(move, player)
            val = self.alphabeta(node, get_enemy(player), alpha, beta)
            node.make_move(move, None)
            if player == 'O':
                if val > alpha:
                    alpha = val
                if alpha >= beta:
                    return beta
            else:
                if val < beta:
                    beta = val
                if beta <= alpha:
                    return alpha
        if player == 'O':
            return alpha
        else:
            return beta


def determine(board, player):
    a = -2
    choices = []
    if len(board.available_moves()) == 9:
        return 4
    for move in board.available_moves():
        board.make_move(move, player)
        val = board.alphabeta(board, get_enemy(player), -2, 2)
        board.make_move(move, None)
        # print "move:", move + 1, "causes:", board.winners[val + 1]
        if val > a:
            a = val
            choices = [move]
        elif val == a:
            choices.append(move)
    return random.choice(choices)


def get_enemy(player):
    if player == 'X':
        return 'O'
    return 'X'

# Returns an integer
def deconstruct(board, previousBoard):
    sq = board.split('|')
    if previousBoard == '':
        for i in range(3):
            if not sq[i][0] == '-': return (i*3)
            if not sq[i][1] == '-': return (i*3+1)
            if not sq[i][2] == '-': return (i*3+2)
    sq2 = previousBoard.split('|')            
    for i in range(3):
        if not sq[i][0] == sq2[i][0]: return (i*3)
        elif not sq[i][1] == sq2[i][1]: return (i*3+1)
        elif not sq[i][2] == sq2[i][2]: return (i*3+2)

allowed = set('XO|-\n')
def allow(tst):
    str = tst[:11]
    if str=='' or len(str) < 11:
        return False
    for c in str.upper():
        if c not in allowed:
            return False
    return True
while(1):
    print('Server ready:')
    connectionSocket, addr = serverSocket.accept()
    print('Connected.')
    board = Tic()

    previousBoard = ''
    while not board.complete():
        player = 'X'
        clientResponse = connectionSocket.recv(2048)
        print('Received: ' + clientResponse)

        if 'illegal' in (clientResponse.lower()):
            print('illegal move, conn. closed')
            connectionSocket.close()
            break
        elif not allow(clientResponse):
            print('illegal response, conn. closed')
            try:
                connectionSocket.send('illegal response, conn. closed')
            except:
                print('Couldnt send error message. Conn. closed')
            connectionSocket.close()
            break
        
        client_move = deconstruct(clientResponse, previousBoard)
        if not client_move in board.available_moves():
            continue
        board.make_move(client_move, player)
    
        if board.complete():
            break  # TODO: HERE!!!
        player = get_enemy(player)
        server_move = determine(board, player)
        board.make_move(server_move, player)
        previousBoard = board.show()
        print('Sent: ' + board.show())
        connectionSocket.send(board.show())

    try:
        connectionSocket.send(board.winner().lower() + ' win')
        print(board.winner().lower() + ' win')
    except:
        if board.winner() == None:
            connectionSocket.send('tie')
            print('tie')
    connectionSocket.close()
    print('Closing connection')
