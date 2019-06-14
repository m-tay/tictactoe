import random

class Board:
    # hold state of board, initialise to '-' when creating Board
    state = ['-'] * 9

    # prints the board state
    def printState(self):
        print(" " + self.state[0] + " | " + self.state[1] + " | " + self.state[2])
        print("-----------")
        print(" " + self.state[3] + " | " + self.state[4] + " | " + self.state[5])
        print("-----------")
        print(" " + self.state[6] + " | " + self.state[7] + " | " + self.state[8])
    
    # sets the state of a given cell
    def setState(self, cell, value):

        # check if cell already filled
        if(self.state[cell] == '-'):
            self.state[cell] = value
            return True
        else:
            return False

    # clears the state of a given cell
    def clearState(self, cell):
        self.state[cell] = '-'

    # returns the character of winner, D is draw or False if no winner
    def isGameWon(self):
        
        # check for winning rows
        if(self.state[0] == self.state[1] and self.state[1] == self.state[2] and self.state[0] is not '-'):
            return self.state[0]

        if(self.state[3] == self.state[4] and self.state[4] == self.state[5] and self.state[3] is not '-'):
            return self.state[3]

        if(self.state[6] == self.state[7] and self.state[7] == self.state[8] and self.state[6] is not '-'):
            return self.state[6]

        # check for winning columns
        if(self.state[0] == self.state[3] and self.state[3] == self.state[6] and self.state[0] is not '-'):
            return self.state[0]

        if(self.state[1] == self.state[4] and self.state[4] == self.state[7] and self.state[1] is not '-'):
            return self.state[1]

        if(self.state[2] == self.state[5] and self.state[5] == self.state[8] and self.state[2] is not '-'):
            return self.state[2]

        # check for diagonals
        if(self.state[0] == self.state[4] and self.state[4] == self.state[8] and self.state[0] is not '-'):
            return self.state[0]

        if(self.state[2] == self.state[4] and self.state[4] == self.state[6] and self.state[2] is not '-'):
            return self.state[2]

        # check for a draw
        count = 0
        for cell in self.state:
            if cell == 'X' or cell == 'O':
                count += 1

        if count == 9:
            return 'D'

        # otherwise, return false - no end state detected
        return False
   
    # used by basic AI to play
    def getRandomFreePosition(self):
        while(True):
            randomCell = random.randint(0,8)
            if(self.state[randomCell] == '-'):
                return randomCell

    # check if cell is free
    def isCellFree(self, cell):
        if(self.state[randomCell] == '-'):
            return True
        else:
            return False

    # returns list of free cell positions
    def getFreeCells(self):
        i = 0
        freeCells = []

        for cell in self.state:
            if cell == '-':
                freeCells.append(i)
            
            i += 1

        return freeCells

class AiPlayer:
    def __init__(self, cpu):
        # set character cpu will play as
        self.cpu = cpu

        # derive human char
        if(cpu == 'X'):
            self.human = 'O'
        else:
            self.human = 'X'

    # gets the opposite player to the current player
    def getOpposite(self, player):
        if(player == 'X'):
            return 'O'
        else:
            return 'X'
        
    # implements recursive minimax algorithm 
    def minimax(self, board, player):
        
        # set up best score initial values 
        if(player == self.cpu):
            bestScore = 0
        else:
            bestScore = 10            

        # base cases - check for terminal board states
        boardOutcome = board.isGameWon()

        if(boardOutcome == self.cpu):   # cpu has won (yay)
            return 10
        if(boardOutcome == self.human):  # fleshy human has won (boo)
            return 0
        if(boardOutcome == 'D'):    # draw (meh)
            return 5
                         
        # get free cells and loop through them
        freeCells = board.getFreeCells()
        for cell in freeCells:
            board.setState(cell, player)    
            moveScore = self.minimax(board, self.getOpposite(player)) # get score
            board.clearState(cell)   # undo move

            # if cpu, maximise score
            if(player == self.cpu):
                bestScore = max(bestScore, moveScore)

            # if human, minimise score
            if(player == self.human):
                bestScore = min(bestScore, moveScore)

        return bestScore

    # function to manage minimax results and select the best move
    def getBestMove(self, board, player):
        
        # get free cells and make empty list to store options
        freeCells = board.getFreeCells()
        freeCellOptions = []
        
        # loop through all available cells
        for cell in freeCells:

            board.setState(cell, player) # add move 

            # get score from minimax (minimising player first)
            moveScore = self.minimax(board, self.getOpposite(player))
            
            board.clearState(cell)   # undo move
            
            # check score to see if worth saving
            if moveScore > 5:               # is it better than a draw?
                freeCellOptions = [cell]    # winning move becomes the list
                
            elif moveScore == 5:
                freeCellOptions.append(cell) # draws just add to list

        # return the best move
        if len(freeCellOptions) > 0:
            # if multiple best moves, return a random one
            return random.choice(freeCellOptions)
        else:
            # otherwise just play whatever
            return random.choice(board.getFreeCells())


# setup
b = Board()
print("Tic Tac Toe")
print("-----------")


# get player's character (x goes first)
player = input("Do you want to be X or O? ")
if(player == 'X'):
    cpu = 'O'
else:
    cpu = 'X'

# create cpu object
ai = AiPlayer(cpu)

# if cpu goes first, make starting move
if(player=='O'):
    b.setState(b.getRandomFreePosition(), 'X')
    
# game loop
while(not b.isGameWon()):
    # get player move, check for validity
    validInput = False
    while(not validInput):
        cell = int(input("Enter cell: "))
        validInput = b.setState(cell, player)
 
    # update after player move
    b.printState()

    # check if player won
    if(b.isGameWon()):
        break
    
    # get random cpu move
    b.setState(ai.getBestMove(b, cpu), cpu)
    print("Cpu played: ")
    b.printState()


print("\nGAME OVER")
print("Winner is " + b.isGameWon())