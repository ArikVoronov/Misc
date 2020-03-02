import tkinter as tk
import boggle_engine as bg
    
class Boggle():
    """ Boggle GUI class,
        it uses only the mouse as input
        creates a main GUI window
        adds a menu frame which allows to play or quit the game
        adds a game frame where the player interacts with the board and plays boggle
        presents all game info: score, timer, collected words and the validity of the current word.
    """
    def __init__(self,boggleDict,gameTime):
        self.HEIGHT = "500"
        self.WIDTH = "600"
        self.playing = False
        self.gameTime = gameTime
        self.boggleDict = boggleDict
        self.remainGrid = None
        
        # root properties
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.iconbitmap('.\\assets\\b.ico')
        self.root.title("Boggle Game")
        self.root.geometry(self.WIDTH+"x"+self.HEIGHT)

        self.MakeGameFrame()
        self.MakeMenuFrame()
        self.UpdateTimer()
        self.menuFrame.tkraise()
        self.root.mainloop()
        
    def MakeMenuFrame(self):
        """ Create the Menu frame, allowing to play (again) or quit the game """
        # MENU FRAME
        self.menuFrame = tk.Frame(self.root)
        self.menuFrame.place(relwidth=1,relheight=1)
        # background image
        self.menuBackground_image = tk.PhotoImage(file='.\\assets\\matrix.png')
        self.menuBackgroundLabel = tk.Label(self.menuFrame,image=self.menuBackground_image)
        self.menuBackgroundLabel.place(relwidth=1,relheight=1)
        # play button
        self.playButton = tk.Button(self.menuFrame, text='Play',font=('Courier',24),bg='black',fg='light green',
                                   command=lambda :self.PlayButtonCallback())
        self.playButton.place(relx=0.5,rely=0.4,anchor='n')
        # quit button
        self.quitButton = tk.Button(self.menuFrame, text='Quit',font=('Courier',24),bg='black',fg='light green',
                                   command=lambda :self.root.destroy())
        self.quitButton.place(relx=0.5,rely=0.6,anchor='n')
        # game over message (doesn't appear on first play)
        self.game_overLabel= tk.Label(self.menuFrame,font=('Courier',24),fg='black',bg='light green',
                               text='')
        
        
    def MakeGameFrame(self):
        """ Create the game frame, where the player interacts with the board and receives all relevant game info"""
        # GAME FRAME
        self.gameFrame = tk.Frame(self.root)
        self.gameFrame.place(relwidth=1,relheight=1)
        # background image
        self.gameBackground_image = tk.PhotoImage(file='.\\assets\\matrix.png')
        self.gameBackgroundLabel = tk.Label(self.gameFrame,image=self.gameBackground_image)
        self.gameBackgroundLabel.place(relwidth=1,relheight=1)
        # boggle grid
        self.gridframe = tk.Frame(self.gameFrame,bg='green')
        self.gridframe.place(relx=0.4,rely=0.1,anchor='n')
        self.buttonGrid = [[None for x in range(4)] for y in range(4)] 
        for row in range(4):
            for col in range(4):
                self.buttonGrid[row][col] = tk.Button(self.gridframe, font=('Courier',28),bg='black',fg='green',
                                                       text='#', 
                                   command=lambda row=row, col=col: self.GridCallback(row,col))
                self.buttonGrid[row][col].grid(row=row, column=col, sticky="nsew")
        # check word button
        self.checkButton = tk.Button(self.gameFrame, text='Check',font=('Courier',18),bg = 'light green', fg='black',
                                   command=lambda :self.CheckCallback())
        self.checkButton.place(relx=0.4,rely=0.75,anchor='s')
        # end game button
        self.endGameButton = tk.Button(self.gameFrame, text='X',font=('Courier',18),bg = 'light green', fg='black',command=lambda :self.EndGame())
        self.endGameButton.place(relx=1.0,rely=0.0,relwidth=0.1,anchor='ne')
        # score label
        self.scoreLabel = tk.Label(self.gameFrame,font=('Courier',18),bg='black',fg='light green',
                                    text = "Score:{}".format(0))
        self.scoreLabel.place(relx=1,rely=1,anchor='se')
        # current word label
        self.currentWord = tk.Label(self.gameFrame,font=('Courier',18),bg='black',fg='light green')
        self.currentWord.place(relx=0,relwidth=0.8,relheight=0.1,anchor='nw')
        # timer
        self.timer = tk.Label(self.gameFrame ,font=('Courier',18),bg='black',fg='light green')
        self.timer.place(relx=0.9,relwidth=0.1,relheight=0.1,anchor='ne')
        # found words list
        self.foundList = tk.Listbox(self.gameFrame,font=('Courier',18),bg='black',fg='light green',highlightbackground='light green')  
        self.foundList.place(relx=1,rely=0.1,relwidth=0.25,relheight=0.84,anchor='ne')
        # scroll bar for list (UGLY)
        self.scrollbar = tk.Scrollbar(self.foundList)
        self.scrollbar.pack(side='right', fill='y')
        self.scrollbar.config(command=self.foundList.yview)
        # remaining words by length
        self.remainingWordsLabel = tk.Label(self.gameFrame ,font=('Courier',16),bg='black',fg='light green',justify='center')
        self.remainingWordsLabel.place(relx=0,rely=1,relwidth=0.75,relheight=0.2,anchor='sw')
        
        

    def UpdateTimer(self):
        """ Update the game timer and end the game when time runs out"""
        self.root.after(10, self.UpdateTimer)
        if self.playing:
            self.boggleGame.Timer()
            self.timer['text']= self.boggleGame.timeLeft
            if self.boggleGame.timeLeft <=0:
                self.EndGame()
                    
    def EndGame(self):
        """ Stop the timer and return to the main menu """
        self.playing=False
        self.game_overLabel['text']='Game over! Score: {}'.format(self.boggleGame.score)
        self.game_overLabel.place(relx=0.5,rely=0.2,anchor='n')
        self.playButton['text']='Play Again'
        self.menuFrame.tkraise()
        
    def GridCallback(self,row,col):
        """ Callback from the buttons on the boggle grid (under gameFrame),
            check if the players pick is valid and add the letter
            to the current word, highlight the picked cell"""
        valid = self.boggleGame.CollectWord(row, col)
        if valid:
            self.currentWord['text']=self.boggleGame.word
            self.currentWord['fg'] = 'light green'
            self.buttonGrid[row][col]['bg']='light green'
            self.buttonGrid[row][col]['fg']='black'
        
    def CheckCallback(self):
        """  Callback from the check button (under gameFrame),
            check if the current word is valid, and if it hasn't been found by the player already,
            add the word to the found words list and add the score for the word"""

        validWord,newWord=self.boggleGame.CheckWord()
        currentWord = self.currentWord['text']
        if validWord:
            if newWord:
                self.foundList.insert(0, currentWord)
                self.currentWord['text']= 'You found {}!'.format(currentWord)
                self.currentWord['fg'] = 'light green'
                self.wordsByLength[len(currentWord)]-=1
                self.RemainingWordsUpdate()
            else:
                self.currentWord['text']= 'You already found {}'.format(currentWord)
                self.currentWord['fg'] = 'light yellow'
        else:
            self.currentWord['text']='{} is not a word'.format(currentWord)
            self.currentWord['fg'] = 'red'
        self.scoreLabel['text']= "Score:{}".format(self.boggleGame.score)
        self.ResetGridColors()
        
    def PlayButtonCallback(self):
        """ Callback for the play button (under menuFrame)
            reset the game, start the timer and switch to the game frame"""
        self.ResetGame()
        self.gameFrame.tkraise()
        self.playing=True

    def RemainingWordsUpdate(self):
        if self.maxLetters<=7:
            cols=3; fontSize=24
        else:
            cols = 5; fontSize=16

        # Delete existing grid
        if self.remainGrid!=None:
            for r in self.remainGrid:
                for g in r:
                    if g != None:
                        g.grid_forget()
        # Create new remaining words grid
        self.remainGrid = [[None for x in range(cols)] for y in range(5)]
        for row in range(5):
            for col in range(cols):
                wordLength = cols*row+col+2 # length of word (must be >2)
                if wordLength > self.maxLetters: pass
                else:
                    self.remainGrid[row][col] = tk.Label(self.remainingWordsLabel, font=('Courier',fontSize),bg='black',fg='light green',
                                                           text=" {}: {} ".format(wordLength, self.wordsByLength[wordLength]))
                    self.remainGrid[row][col].grid(row=row, column=col, sticky="n",ipadx=1)
        
    def ResetGame(self):
        """ Reset all the relevant parameters to start a new boggle game"""
        board = bg.RandomBoard(self.boggleDict)
        self.boggleGame = bg.BoggleEngine(board,self.boggleDict,self.gameTime)
        self.wordList = FindAllWords(board,boggleDict)
        self.wordsByLength = WordsByLength(self.wordList)
        self.maxLetters = max(self.wordsByLength, key=int)
        # Fill out the dictionary
        for i in range(16):
            if i not in self.wordsByLength.keys():
                self.wordsByLength[i]=0
        self.wordsByLength = {k: v for k, v in sorted(self.wordsByLength.items(), key=lambda item: item[0])}
        self.RemainingWordsUpdate()
        self.ResetGridColors()
        self.foundList.delete(0,'end')
        self.currentWord['text']= ''
        self.currentWord['fg'] = 'light green'
        self.scoreLabel['text']= "Score:{}".format(self.boggleGame.score)
        
    def ResetGridColors(self):
        """ Reset the boggle grid highlights"""
        for r in range(4):
            for c in range(4):
                self.buttonGrid[r][c]['bg']='black'
                self.buttonGrid[r][c]['fg']='light green'
                self.buttonGrid[r][c]['text']=self.boggleGame.board[r][c]

if __name__=="__main__":
    from boggle_solver import *
    
    boggleDict = bg.ImportBoggleDict()  
    boggle=Boggle(boggleDict,gameTime=180)
