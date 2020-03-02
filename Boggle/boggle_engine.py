# boggle game
from time import time
import random, string
from numpy.random import choice
def PrintBoard(board):
    """
    Print out the board directly to the console.
    """
    for row in range(len(board)):
        print('| ',end='')
        for col in range(len(board[row])):
            print(board[row][col],end=' | ')
        print('')
        
def GetLetterFrequencies(boggleDict):
    """
    Get freuqency of letters in given dictionary
    Results can be compared with:
    http://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
    """
    dictString = ''.join(boggleDict)
    letterFrequency = {}
    currentLetter = None
    for i,letter in enumerate(dictString):
        if currentLetter == 'QU':
            if letter=='U': continue
        if letter == 'Q': currentLetter = 'QU'
        else: currentLetter = letter
        if currentLetter not in letterFrequency:
            letterFrequency[currentLetter]=0
        else:
            letterFrequency[currentLetter]+=1

    for key,value in letterFrequency.items():
        letterFrequency[key] = round(value/len(dictString),4)
    remainder = 1-sum(letterFrequency.values())
    letterFrequency['E'] = letterFrequency['E']+remainder
    letterFrequency={k: v for k, v in sorted(letterFrequency.items(), key=lambda item: item[1],reverse=True)}
    frequencies = list(letterFrequency.values())
    letters = list(letterFrequency.keys())
    return letters,frequencies


def RandomBoard(boggleDict):
    """
    Create a 2D list of random characters (boggle board)
    """
    
    letters,frequencies = GetLetterFrequencies(boggleDict)
    
    board = []
    for r in range(4):
        board.append([])
        for c in range(4):
            randomLetter = choice(letters,p=frequencies)
            board[r].append(randomLetter)
    return board

def ImportBoggleDict(file = None):
    """
    Import a dictionary of words
    words.txt from https://github.com/dwyl/english-words/blob/master/words.txt
    usa.txt from http://www.gwicks.net/dictionaries.htm
    """
    if file==None:
        path = 'assets\\usa.txt'
    else:
        path = file
    f = open(path, 'r')
    words = f.readlines()
    f.close()
    boggleDict=[]
    upperAlphabet = string.ascii_uppercase
    for word in words:
        badWord = False
        fixedWord = word.rstrip('\n').upper()
        for letter in fixedWord:
            if letter not in upperAlphabet:
                badWord = True
        if ('Q' in fixedWord) and not ('QU' in fixedWord) or len(fixedWord)<2:
            badWord = True
        if badWord:
            continue
        else:
            boggleDict.append(fixedWord)
    return boggleDict



class BoggleEngine():
    """
    The main engine class for the boggle game, it allows the player to
    checks if player input cell is valid,
    collects words and checks for valid words,
    keeps score,
    keeps game time
    """
    def __init__(self,board,boggleDict,gameTime):
        self.board = board
        self.t0 = time() # Time at creation of class
        self.timeLeft=1 # This prevents the game from ending before timers is updated
        self.gameTime = gameTime
        self.boggleDict = boggleDict
        self.score=0
        self.foundWords = []
        self.gameOver = False
        self.ResetPicks()
    def Timer(self):
        """ Keep remaimng game time """
        self.timeLeft = self.gameTime-round((time()-self.t0))
        
    def ResetPicks(self):
        """ Reset the picked cells and collected word """
        self.pickedCells=[]
        self.word = ''
        self.lastPicked= None
    def CheckWord(self):
        """ Check if the current word appears in the dictionary
            and hasn't been already found by the player"""
        validWord = self.ValidWord(self.word,self.boggleDict)
        wordIsNew = self.word not in self.foundWords
        if validWord and wordIsNew:
            self.score+= len(self.word)**2
            self.foundWords.append(self.word)
        self.ResetPicks()
        return validWord,wordIsNew
    def CollectWord(self,row,col):
        """ Check if the cell picked by the players is valid and if so
            collects the new letter to the current word"""
        currentCell = [row,col]
        if self.lastPicked==None: # The first letter picked is always valid
            valid = True
        else:
            valid = self.CheckIfNeighbor(self.lastPicked,currentCell) and (currentCell not in self.pickedCells)
        if valid:
            self.pickedCells.append(currentCell)
            currentLetter = self.board[row][col]
            self.word += currentLetter
            self.lastPicked = currentCell
        return valid
    def ValidWord(self,word,boggleDict):
        """
        Check if the word appears in the dictionary
        """
        fixedWord = word.upper() #Transform word to the format given in the dictionary
        if fixedWord in boggleDict:
            return True
        return False
        
    def Dist(self,x1,x2):
        """
        Calculate the euclidean distance between two points
        """
        d = ( (x2[0]-x1[0])**2+(x2[1]-x1[1])**2 )**(1/2)
        return d

    def CheckIfNeighbor(self,x1,x2):
        """
        Check whether 2 points are neighbors on the boggle grid
        """
        if self.Dist(x1,x2) <2:
            return True
        else:
            return False


def PlayWithoutGUI(boggleGame):
    """
    Play boggle without GUI
    """
    print("Input options:")
    print("1) \'row,column\' - pick a cell.")
    print("2) \'check\' - check if your word is valid")
    print("3) \'!\' - quit game")
    while True:
        userInput = input('Enter input: ')
        if userInput == "!":
            break
        elif userInput=="check":
            valid,wordIsNew = boggleGame.CheckWord()
            if valid:
                if wordIsNew:
                    print('valid, score:',boggleGame.score)
                else:
                    print('already got that one')
            else:
                print('invalid')
        else:
            if len(userInput)!=3:
                print('bad input')
            elif userInput[1]!=',':
                print('bad input')
            else:
                row = int(userInput[0])
                col = int(userInput[2])
                boggleGame.CollectWord(row,col)
                print(boggleGame.word)


     
if __name__=='__main__':
    # This part runs a boggle game from the engine, which can be played without the GUI

    boggleDict = ImportBoggleDict()
    board = RandomBoard(boggleDict)
    PrintBoard(board)

    
    
    
            
        
    boggleGame = BoggleEngine(board,boggleDict,60)
##    PlayWithoutGUI(boggleGame)

    
