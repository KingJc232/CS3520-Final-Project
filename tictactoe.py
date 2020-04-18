"""
File: tictactoe.py
Goal: To Create Tic Tac Toe 
Developer: Jose Ceballos 
"""

import pygame 
import random 

from enum import Enum

from time import sleep

#Initializing Pygame 
pygame.init()

#Initializing pygame font 
pygame.font.init()

"""
    Goals: 
            - Create the minimax AI 
            - Add More Button to the main menu (player vs simple AI) (simple AI vs MiniMax AI) (MiniMax AI vs MiniMax AI)
            - add options in the GameState to play with different AI's 
            - Link all the buttons in the main menu with the correct AI 
            - Also Stopped To Draw a Line For the Winner that Won 
            - Add Alpha-Beta Pruning to improve computation speed (If you have time)
            - Create a Enum class for the gameModes Instead of using strings (cosmetics)
            - Clean up the code (Document it / make it more efficient)
            - Clean up the project add better designs/ animations 
            - Implement a timer for the AI (Pause)
            - Create Different Colors for the Main Menu Buttons ??? 


"""

"""
Side Notes:
    - The Number 0 Represents an Empty Square 
    - The Number 1 Represents a "X" Square 
    - The Number 2 Represents a "O" Square
"""

#Super Simple Object that has a x and a y 
class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#Simple ButtonColor Class
class ButtonColor:
    def __init__(self, idleColor, hoverColor, pressedColor):
        self.idleColor = idleColor
        self.hoverColor = hoverColor
        self.pressedColor = pressedColor

#Simple Enum Class Used to Determine the State of the  Button 
class ButtonState(Enum):
    IDLE = 1 
    HOVER = 2
    PRESSED = 3

#Simple Button Class 
class Button(pygame.Surface):
    
    def __init__(self, message, buttonColors, position, sizeOfText = 30, dimensions = (200,100) ):

        super().__init__(dimensions) #Setting the Dimensions of the Surface 
        self.buttonColors = buttonColors #Saving the Different Colors of the Button 
        self.position = position #Saving the position of the Button 
        self.buttonState = ButtonState.IDLE #Initially The Button is IDLE 

        self.font = pygame.font.Font("FreeSans.ttf",sizeOfText)

        self.text = self.font.render(message,True, (0,0,0))

        self.active = False #initally Falsed Only True When Pressed

    #Update Method For the Button 
    def update(self, mouseState):
        
        self.buttonState = ButtonState.IDLE #The User is not pressing the Button 

        #Getting the Mouse Position 
        mousePos = pygame.mouse.get_pos()

        #Checking if the Mouse is Hovering over the Button 
        if mousePos[0] >= self.position[0] and mousePos[0] <= (self.position[0] + self.get_width()):
            if mousePos[1] >= self.position[1] and mousePos[1] <= (self.position[1] + self.get_height()):
                #The Mouse Is Hovering over the button change its state 
                self.buttonState = ButtonState.HOVER
                #Checking if the Mouse is Pressing the Button 
                if mouseState[0] == True: #If the user is left clicking on the button 
                    self.buttonState = ButtonState.PRESSED 
                    self.active = True #Since it Was Pressed We 
        
        pass

    def draw(self, screen):

        #Filling the Correct Color Based on the Button State 
        if self.buttonState == ButtonState.IDLE:
            self.fill(self.buttonColors.idleColor) #Filling the button with the idle color 
        elif self.buttonState == ButtonState.HOVER:
            self.fill(self.buttonColors.hoverColor)
        elif self.buttonState == ButtonState.PRESSED:
            self.fill(self.buttonColors.pressedColor)

        #Drawing the Outline of the button 
        pygame.draw.rect(screen, (0,0,0), (self.position[0]-2,self.position[1]-2,self.get_width()+4,self.get_height()+4),0)

        #Drawing the Button to the Screen 
        screen.blit(self,self.position)

        #Drawing the Text of the Button 
        screen.blit(self.text,(self.position[0] + 20, self.position[1] + 25))

        pass


    pass


#Class will be used to represent the 9 squares in the tic tac toe game 
class Square(pygame.Surface):
    
    def __init__(self,position, width = 200, height = 200):
        super().__init__((width,height)) #Every Surface By Default needs a Width and Height 
        
        #self.position is a tuple 
        self.position = position #Saving the position of the Square 

        #Loading All the Images to the Square 
        self.xImage = pygame.image.load("x.png")
        self.oImage = pygame.image.load("o.png")
        self.emptyImage = pygame.image.load("empty.png")

        self.active = False #Initially the Square is not active because its not pressed

    #Updates the Square 
    def update(self,mouseState ):


        #MouseState is a list of booleans of all the mouse buttons states 
        #mousePos is a tuple
        mousePos = pygame.mouse.get_pos() #Getting the Mouse position

        #If the square is empty 
        #Need this if statement so that the player and the AI are not able to override already active squares 
        if self.active == False: 
            #Checking if the mouse position is within the squares position 
            if mousePos[0] >= self.position[0] and mousePos[0] <= (self.position[0] + self.get_width()):
                if mousePos[1] >= self.position[1] and mousePos[1] <= (self.position[1] + self.get_height()):
                    #Mouse is Hovering over the square 
                    #Checking if the Mouse is pressed 
                    if mouseState[0]: #If this doesnt work try [0]
                        self.active = True #The square got pressed therefore its active
        pass
    #Draws the Square onto the Screen 
    def draw(self, screen, num):
        
        if num == 0:
            screen.blit(self.emptyImage, self.position) 
        elif num == 1: 
            screen.blit(self.xImage,self.position)
        elif num == 2:
            screen.blit(self.oImage,self.position)
        else:
            screen.blit(self.emptyImage, self.position)
        pass
    pass


#Simple Enum Class that Helps determine the win state throughout the game 
class WinState(Enum):
    NONE = 0 
    X = 1
    O = 2
    TIE = 3 

#Player VS AI 
class GameState():
    #Default Constructor 
    def __init__(self, screenD, gameMode):
        #Going to Represent the Board With a 2d Array 
        # 0 represents ""
        # 1 represents "X"
        # 2 represents "O"
        # 4x4 
        self.board = [[0,0,0],
                      [0,0,0],
                      [0,0,0]]
        
        #How to Create an Unitialized Two D Array 
        #[[0 for x in range(col_count)] for y in range (row_count)]
        self.visualBoard = [[0 for x in range(3)] for y in range(3)] #Two Dimensional List  

        #Initializing the VisualBoard 
        self._initializeBoard() 

        self.playersTurn = True #Initially the Player Goes First He will be "X"

        self.winner = None

        self.isStateActive = True #Initially the State is Active 
        #Determines

        #Determines what GameMode to Play 
        self.gameMode = gameMode

        pass

    def _initializeBoard(self):
        #These Values Help Determine the Position of every Square in the Visual Board 
        i = 0
        j = 0 
        #Initializing the Visual Board 
        for row in range(len(self.visualBoard)): 
            for col in range(len(self.visualBoard[0])):
                self.visualBoard[row][col] = Square((i,j)) #Creating a Square At The Correct Position 
                i = i + 200
            #Updating j     
            j = j + 200
            #Resetting i  
            i = 0  

    def update(self, mouseState):

        #Check for winner 
        self.winner = self._checkForWinner()# Checking for the winner before the player go 
        

        #This Code Allows the player to pick a position on the board 
        #Do this while there is no winner 
        if self.winner == WinState.NONE: 
            #if its the player the turn 
            if self.playersTurn:
                for row in range(len(self.board)):
                    for col in range(len(self.board[0])):
                        #If the Square is Empty then see if the player wants to pick that square 
                        if self.board[row][col] == 0: 
                            self.visualBoard[row][col].update(mouseState) #Update it 
                        
                            #If the player picked the square then its now the AI's Turn 
                            if self.visualBoard[row][col].active == True:
                                #Link It with the board
                                self.board[row][col] = 1
                                #Changing Turns 
                                
                                self.playersTurn = False
    

        self.winner = self._checkForWinner()# Checking for the winner before the Ai goes
        if self.winner == WinState.NONE: 
            #Its The AI's Turn Now 
            if self.playersTurn == False:   
                #Call the _chooseBestMove For the AI To Select a Move 
                self._chooseBestMove() #Calling the AI To Pick a Move 
                self.playersTurn = True #Also Its Now the Players Turn 
                pass

        #If someone won then turn off the State
        if self.winner != WinState.NONE:    
            self.isStateActive = False #State is being turned off 


    def _availablePositions(self):
        available = [] #Initially Empty 
        #First Find all available positions store them in a list and pick a random element in that list 
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                #If its available 
                if self.board[row][col] == 0: 
                    available.append(Vector2D(row,col)) #Vector2D is a custom object that has a x and y 
        return available #Returning the Available List 
        pass
    #Choose the Best Move for the AI using the minimax algorithm 
    def _chooseBestMove(self):

        #Add Minimax algorithm here later 
        #Simple AI that picks a random place in the board 
        available = self._availablePositions()
        #Choosing a Random Index from the available list 
        if len(available) > 0:
            randIndex = random.randint(0, len(available)-1)

            row = available[randIndex].x
            col = available[randIndex].y
            #Update both boards 
            self.visualBoard[row][col].active = True #Marking it as taken 
            self.board[row][col] = 2 #Placing a "O" in the board 
        pass


    #Function Checks the Board for a winner 
    def _checkForWinner(self):
        
        #Remember:
        # - No Winner Yet represented with a 0 
        # - player "X" is represented with a 1 
        # - player "O" is represented with a 2 
        # - Tie Represented by a 3

        winner = WinState.NONE #initially no one won 
        
        #Checking Horizontal 
        for i in range(len(self.board)):
            #If they are all the same elements 
            if self._sameElements(self.board[i][0],self.board[i][1],self.board[i][2]):
                if self.board[i][0] == 1:
                    winner = WinState.X
                elif self.board[i][0] == 2:
                    winner = WinState.O
        #Checking Vertically 
        for i in range(len(self.board[0])):
            if self._sameElements(self.board[0][i], self.board[1][i], self.board[2][i]):
                if self.board[0][i] == 1:
                    winner = WinState.X
                elif self.board[0][i] == 2:
                    winner = WinState.O

        #Checking Diagonally 
        if self._sameElements(self.board[0][0],self.board[1][1], self.board[2][2]):
                if self.board[0][0] == 1:
                    winner = WinState.X
                elif self.board[0][0] == 2:
                    winner = WinState.O

        if self._sameElements(self.board[2][0],self.board[1][1],self.board[0][2]):
                if self.board[2][0] == 1:
                    winner = WinState.X
                elif self.board[2][0] == 2:
                    winner = WinState.O

        if winner == WinState.NONE and len(self._availablePositions()) == 0:
            return WinState.TIE #TIE 
        else:
            return winner #Either NONE, X, or O 

    #Private Helper Method determines if the Elements passed are the same 
    def _sameElements(self,first, second, third):
        return first == second == third
        pass

    def draw(self, screen):
        #Drawing the Tic Tac Toe Board 
        for row in range(len(self.visualBoard)):
            for col in range(len(self.visualBoard[0])):
                #Drawing Every Element in the VisualBoard
                self.visualBoard[row][col].draw(screen,self.board[row][col])

        #Drawing the Winner Line if there is a Winner 
        if self.winner != WinState.NONE or self.winner != WinState.TIE:
            pass
    pass

    #Drawas the Line Indicating the Winner 
    def drawWinnerLine(self):
        pass

#Simple State that Shows the Winner and Adds two options (Play Again/ Main Menu)
#Instead of a winner State Just draw a line in game state and just use this to display buttons 
class WinnerState():
    def __init__(self, screenD, winner):
        self.background = pygame.Surface(screenD)
        self.backgroundPosition = (0,0) 
        self.background.fill((200,200,200))
        self.isStateActive = True #Initially True Used to switch states 

        
        #Creating a Play Again Button 
        idleColor = (50,100,200)#Light Blue 
        hoverColor = (200,50,50)#Light Red
        pressedColor = (255,0,0)#Dark Red When Pressed 

        self.buttonColors = ButtonColor(idleColor, hoverColor, pressedColor)
        #self, message, buttonColors, position, sizeOfText = 30, dimensions = (200,100)
        self.playAgainButton = Button("Play Again", self.buttonColors,(screenD[0]/2 -100, screenD[1]/2))

        self._getWinner(winner) #Getting the winner based off the winner passed in the state

        #Text that Shows who won the game 
        self.font = pygame.font.Font("FreeSans.ttf",50) 
        #Text to show on to the screen 
        self.winnerDisplay = self.font.render(self.winner,True, (0,0,0))

        self.winnerDisplayPosition = (screenD[0]/2 -100, screenD[1]/4)

    #Gets the winner Display string based off the winner 
    def _getWinner(self, winner):
        if winner == WinState.TIE:
            self.winner = "    TIE"

        elif winner == WinState.X:
            self.winner = "Winner: X"

        elif winner == WinState.O:
            self.winner = "Winner: O"

        else:
            self.winner = "BROKEN" #Something went wrong this should never occur 

        pass

    def update(self,mouseState):

        self.playAgainButton.update(mouseState) #Updating the Button 

        #Button Was Pressed
        if self.playAgainButton.active == True: 
            sleep(.1) #Need this quick pause so that the user can select from the menu again 
            #Turn the State off 
            self.isStateActive = False 
            pass
        pass

    def draw(self, screen):
        screen.blit(self.background, self.backgroundPosition) #Displaying the WinnerStateBackground
        #Drawing the playAgain Button 
        self.playAgainButton.draw(screen)

        #Printing the winner Display on to the screen 
        screen.blit(self.winnerDisplay,self.winnerDisplayPosition)
        pass


#Creating a Main Menu State 
class MainMenuState:
    def __init__(self, screenD):
        self.screenD = screenD
        self.background = pygame.image.load("background.png")
        self.backgroundPosition = (0,0) #Want it to be on the corner 

        self.isStateActive = True #initially The State is Active 

        self.gameMode = "None" #Controls what GameMode to Play 

        idleColor = (50,100,200)#Light Blue 
        hoverColor = (200,50,50)#Light Red
        pressedColor = (255,0,0)#Dark Red When Pressed 

        self.buttonColors = ButtonColor(idleColor, hoverColor, pressedColor)
        #self, message, buttonColors, position, sizeOfText = 40, dimensions = (200,100)
        #Creating the player v.s Minimax Button That will switch them to GameState
        self.playerMiniMaxButton = Button("Player v.s MiniMax AI",self.buttonColors,(self.screenD[0]/2-165,self.screenD[1]/2 -75), 25, (325,75))

        #Creating the player v.s Simple AI button 
        self.playerSimpleAIButton = Button("Player v.s Simple AI",self.buttonColors,(self.screenD[0]/2-165,self.screenD[1]/2), 25, (325,75))
        
        #Creating the SimpleAI v.s MiniMax Button 
        self.simpleAIMiniMaxButton = Button("SimpleAI v.s MiniMax AI",self.buttonColors,(self.screenD[0]/2-165,self.screenD[1]/2 +75), 25, (325,75))

        #Creating the MiniMaxAI v.s MiniMax AI Button 
        self.miniMaxButton = Button("MiniMax AI v.s MiniMax AI", self.buttonColors,(self.screenD[0]/2-165,self.screenD[1]/2 +150), 25, (325,75))

        pass

    def update(self, mouseState):

        #Updating the playerMiniMaxButton 
        self.playerMiniMaxButton.update(mouseState)

        #Updating the playerSimpleAIButton 
        self.playerSimpleAIButton.update(mouseState)

        #Updating the simpleAIMiniMaxButton
        self.simpleAIMiniMaxButton.update(mouseState)

        #Updating the miniMaxButton
        self.miniMaxButton.update(mouseState)

        #If the user presses this button 
        if self.playerMiniMaxButton.active == True:
            sleep(.1)
            self.isStateActive = False #Turn off the Main Menu State 
            self.gameMode = "playerMiniMax" #Go to the player MiniMax Game State

        #If the User pressed the playerSimpleAIButton
        if self.playerSimpleAIButton.active == True:
            sleep(.1)
            self.isStateActive = False #Turnning off the Main Menu State
            self.gameMode = "playerSimpleAI" #Go TO the player Simple AI Game State 

        #If the User presses the simpleAIMiniMaxButton
        if self.simpleAIMiniMaxButton.active == True:
            sleep(.1)
            self.isStateActive = False #Turnning off the Main Menu State
            self.gameMode = "simpleAIMiniMax"

        #If the User presses the miniMaxButton 
        if self.miniMaxButton.active == True:
            sleep(.1)
            self.isStateActive = False #Turnning off the Main Menu State
            self.gameMode = "miniMax"

        pass

    def draw(self, screen):
        #Drawing the background of the Main Menu 
        screen.blit(self.background, self.backgroundPosition)
        #Drawing the playerMiniMaxButton using its draw function 
        self.playerMiniMaxButton.draw(screen)

        #Drawing the playerSimpleAIButton using its draw function 
        self.playerSimpleAIButton.draw(screen)

        #Drawing the simpleAIMiniMaxButton using its draw function 
        self.simpleAIMiniMaxButton.draw(screen)

        #Drawing the miniMaxButton using its draw function 
        self.miniMaxButton.draw(screen)
        pass


#Controls all the States of the Game (Main Menu)
class Game: 
    def __init__(self, screenW = 600, screenH = 600):
        self.screen = pygame.display.set_mode((screenW,screenH)) #Creating a Screen 
        pygame.display.set_caption("Tic Tac Toe") #Changing the name of the Window 
        self.screenD = (screenW, screenH)
        self.states = [] #Creating a Empty Stack That will Store the states of the game 

    def start(self):
        #Main Game Loop 
        isOver = False
        while not isOver:
            #Event Loop Handler 
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    isOver = True

            mouseState = pygame.mouse.get_pressed() #Getting the State of all the buttons on the mouse

            #Updating all the Componenets of the Current State
            self.update(mouseState)

            #Drawing all the Componenets of the Current State
            self.draw()

            #Updating all display Modules 
            pygame.display.update()

        pygame.quit() #Quitting pygame 
        pass
    
    
    def update(self, mouseState):
        #Calling the Update Method of the Current State (Ensuring the States are not Empty)
        if len(self.states) > 0:
            #Peeking the Top State in the "Stack" 
            self.states[len(self.states) - 1].update(mouseState)  #Calling Update Method 
            
            #If the State is turned Off Show WinState
            if self.states[len(self.states) -1].isStateActive == False: 
                
                #If its an instance of GameState then Switch to WinnerState 
                if isinstance(self.states[len(self.states)-1], GameState): 
                    #Saving the Winner from the gameState
                    tempWinner = self.states[len(self.states) -1].winner
                    #First poping off the gameState 
                    self.states.pop()
                    self.states.append(WinnerState(self.screenD, tempWinner)) #Poping the Winner State on to be displayed 
                    
                #If its an instance of WinnerState then Switch to Main Menu (So pop everything off)
                elif isinstance(self.states[len(self.states)-1], WinnerState):
                    self.states.pop()
                    pass

                #If Its an instance of MainMenu
                elif isinstance(self.states[len(self.states)-1], MainMenuState):
                    gameMode = self.states[len(self.states)-1].gameMode #Getting the GameMode from the MainMenu 

                    #Popping off the MainMenuState
                    self.states.pop()

                    #Adding the Correct GameMode
                    self.states.append(GameState(self.screenD, gameMode))
                    pass
                
                pass

        #If empty then Push MainMenu State
        else:
            self.states.append(MainMenuState(self.screenD)) #Pushing the Mainmenu State

        pass

    def draw(self):
        #Calling the Draw Method of the Current State (Ensuring the States are not Empty)
        if len(self.states) > 0:
            #Peeking the Top State in the "Stack"
            self.states[len(self.states)-1].draw(self.screen)
        pass

def main():

    ticTacToe = Game()

    ticTacToe.start()
    pass


if __name__ == "__main__":
    main()
