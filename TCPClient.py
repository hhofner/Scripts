from socket import *

import sys
import time
import random
import argparse

################################
# Create connection with Server
serverAddress = ('localhost', 10000)

clientSocket = socket(AF_INET, SOCK_STREAM)
try:
    clientSocket.connect(serverAddress)
except:
    print('Err: Socket not socketing')
    sys.exit()
###################################

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
        # stringBoard += '\n'
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
        print "move:", move + 1, "causes:", board.winners[val + 1]
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

# Returns an int
def deconstruct(board, previousBoard):
    sq = board.split('|')
    sq2 = previousBoard.split('|')
    for i in range(3):
        if not sq[i][0] == sq2[i][0]: return (i*3)
        elif not sq[i][1] == sq2[i][1]: return (i*3+1)
        elif not sq[i][2] == sq2[i][2]: return (i*3+2)

first = True

board = Tic()
previousBoard = ''

while not board.complete():
    player = 'O'
    if first:
        player = 'X'
        client_move = random.randint(0,8)
        board.make_move(client_move, player)
        print('Sent: ' + board.show())
        clientSocket.send(board.show())
        player = 'O'
        first = False
        previousBoard = board.show()

    serverResponse = clientSocket.recv(2048)
    print('Received: ' + serverResponse)
    server_move = deconstruct(serverResponse, previousBoard)

    if 'illegal' in (serverResponse.lower()):
        print('Illegal move, conn. closed')
        clientSocket.send('Illegal move, connection closed')
        clientSocket.close()
        break
    elif 'game over' in serverResponse.lower():
        print('Game over, conn. closed')
        connectionSocket.send('Game over')
        connectionSocket.close()
        break

    if not server_move in board.available_moves():
        continue
    board.make_move(server_move, player)

    if board.complete():
        print(board.winner() + ' won')
        clientSocket.close()
        break  # TODO: HERE!!!!!!
    player = get_enemy(player)
    client_move = determine(board, player)
    board.make_move(client_move, player)
    previousBoard = board.show()
    print('Sent: ' + board.show())
    clientSocket.send(board.show())

clientSocket.close()