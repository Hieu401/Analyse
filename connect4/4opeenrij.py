board = []
alfacoordinates = []
betacoordinates = []
inputs = []
boardsize = []


def drawboard(numcolumn, numrow):
    boardsize.append(numcolumn)
    boardsize.append(numrow)
    insertcoordinates(numcolumn, numrow)
    x1 = 0
    x2 = numcolumn
    for i in range(numrow):
        betacoordinates.append(alfacoordinates[x1:x2])
        x1 = x2
        x2 = x2 + numcolumn
    print_board()


def print_board():
    for row in betacoordinates[::-1]:
        partboard = []
        for col in row:
            partboard.append(col[2])
        print(' '.join(partboard))
    print(betacoordinates[::-1])


def insertcoordinates(numcolumn, numrow):
    for r in range(numrow):
        for c in range(numcolumn):
            s = 'O'
            alfacoordinates.append((r, c, s))


def player1input():
    inputs.append(int(input('Player 1 please select a column you wish your coin to fall into '
                            '(starting at the most left column = 0) '
                            'or type undo and press enter to undo the previous move')))
    if inputs[-1] > boardsize[0] or inputs[-1] < 0:
        inputs.pop()
        print('Player\'s column number of choice does not exist within the boardsize, please try again')
        player1()
    else:
        x = 0
        for i in range(len(betacoordinates)):
            if betacoordinates[x][inputs[-1]][2] == 'O':
                betacoordinates[x][inputs[-1]] = list(betacoordinates[x][inputs[-1]])
                betacoordinates[x][inputs[-1]][2] = 'R'
                betacoordinates[x][inputs[-1]] = tuple(betacoordinates[x][inputs[-1]])
                break
            else:
                x = x + 1
        print_board()


def player2input():
    inputs.append(int(input('Player 2 please select a column you wish your coin to fall into '
                            '(starting at the most left column = 0) '
                            'or type undo and press enter to undo the previous move')))
    if inputs[-1] > boardsize[0] or inputs[-1] < 0:
        inputs.pop()
        print('Player\'s column number of choice does not exist within the boardsize, please try again')
        player1()
    else:
        x = 0
        for i in range(len(betacoordinates)):
            if betacoordinates[x][inputs[-1]][2] == 'O':
                betacoordinates[x][inputs[-1]] = list(betacoordinates[x][inputs[-1]])
                betacoordinates[x][inputs[-1]][2] = 'Y'
                betacoordinates[x][inputs[-1]] = tuple(betacoordinates[x][inputs[-1]])
                break
            else:
                x = x + 1
        print_board()


def wincondition1():
    p = 1

def player1():
    player1input()
    player2()


def player2():
    player2input()
    player1()


drawboard(int(input('Please enter the number of columns')), int(input('Please enter the number of rows')))
player1()


#todo: wincondition, als de top vol is, als de input niet binnen de gegeven kolomen valt, undo, full board, minimum, boardsize, als de gegeven kollom of rij kleiner is dan de win condition
