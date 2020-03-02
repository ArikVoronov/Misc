import boggle_engine as bg


def Bogglable(word,alphabet):
    """
    Check if it's possible to create a word from characters appearing on the board (bogglable words)
    """
    boggle = True
    for letter in word:
        if letter not in alphabet:
            boggle = False
    return boggle

def MakeAlphabet(board):
    """
    Create a set from letters appearing on board
    """
    alphabet = ''
    for b in board:
        alphabet = alphabet+''.join(b)
    return set(alphabet)

def FindBogglable(board,boggleDict):
    """
    Make a list only of bogglable words, and all prefixes for each word
    e.g. word - PEANUT - prefixes - PE, PEA, PEAN, PEANU
    """
    alphabet = MakeAlphabet(board)
    bogglableWords = set(word for word in boggleDict if Bogglable(word,alphabet))
    prefixes = set(word[:i] for word in bogglableWords for i in range(2, len(word)+1))
    return bogglableWords,prefixes

def FindWords(word,path,i,j,wordList,words,prefixes,board):
    """
    Find all words in dictionary from current cell
    """
    rows = len(board); cols = len(board[0])
    word = word + board[i][j]
    path.append((i,j))
    if word in words:
        wordList.append(word)
    if word in prefixes or len(word)==1:
        for row in range(i-1,i+2):
            for col in range(j-1,j+2):
                if rows>row>=0 and cols>col>=0 and (row,col) not in path:
                    FindWords(word,path,row,col,wordList,words,prefixes,board)
    path.remove((i,j))
    word = word[:-1]

def FindAllWords(board,boggleDict):
    """
    Find all the words on the board
    """
    words,prefixes = FindBogglable(board,boggleDict)
    wordList = []
    for iStart in range(4):
        for jStart in range(4):
            FindWords('',[],iStart,jStart,wordList,words,prefixes,board)
    return wordList

def WordsByLength(wordList):
    """
    Create a dictionary {length of word: count of words on board}
    """
    wordLength = {}
    for w in wordList:
        if len(w) not in wordLength:
            wordLength[len(w)]=1
        else:
            wordLength[len(w)]=wordLength[len(w)]+1
    return wordLength



            
if __name__=="__main__":   
    boggleDict = bg.ImportBoggleDict()
    board = bg.RandomBoard()

    bg.PrintBoard(board)
    wordList = FindAllWords(board,boggleDict)
    wordLength=WordsByLength(wordList)
    
    print(len(list(set(wordList))))
