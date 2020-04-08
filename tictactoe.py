"""
File: tictactoe.py
Goal: To Create Tic Tac Toe 
Developer: Jose Ceballos 
"""

import pygame 
import random 

#Initializing Pygame 
pygame.init()

"""
	Side Goals: 
		- Make a simple GUI 
		- Make Player V.s AI (minimax Algorithm)
		- Make AI v.s AI (minimax Algorithm one is min the other is max)
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

#Template to all State classes 
class State:
	#Template 
	def __init__(self):
		self.isStateActive = True #Initially the State is Active 
		pass


	#Template 
	def update(self, mouseState):
		print("Update Method In State Class")
		pass

	#Template 
	def draw(self, screen):
		print("Draw Method In State Class")
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


#Player VS AI 
class GameState(State):
	#Default Constructor 
	def __init__(self):
		#Going to Represent the Board With a 2d Array 
		# 0 represents ""
		# 1 represents "X"
		# 2 represents "O"
		self.board = [[0,0,0],
					  [0,0,0],
					  [0,0,0]]
		
		#How to Create an Unitialized Two D Array 
		#[[0 for x in range(col_count)] for y in range (row_count)]
		self.visualBoard = [[0 for x in range(3)] for y in range(3)] #Two Dimensional List  

		#Initializing the VisualBoard 
		self._initializeBoard() 

		self.playersTurn = True #Initially the Player Goes First He will be "X"
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
						
					
		#Its the AIs Turn 
		else: 
 			#Call the _chooseBestMove For the AI To Select a Move 
 			self._chooseBestMove() #Calling the AI To Pick a Move 
 			self.playersTurn = True #Also Its Now the Players Turn 
 			pass
		pass

	#Choose the Best Move for the AI using the minimax algorithm 
	def _chooseBestMove(self):

		#Add Minimax algorithm here later 
		#Simple AI that picks a random place in the board 
		available = [] #Initially Empty 
		#First Find all available positions store them in a list and pick a random element in that list 
		for row in range(len(self.board)):
			for col in range(len(self.board[0])):
				#If its available 
				if self.board[row][col] == 0: 
					available.append(Vector2D(row,col)) #Vector2D is a custom object that has a x and y 
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
		pass

	def draw(self, screen):
		#Drawing the Tic Tac Toe Board 
		for row in range(len(self.visualBoard)):
			for col in range(len(self.visualBoard[0])):
				#Drawing Every Element in the VisualBoard
				self.visualBoard[row][col].draw(screen,self.board[row][col])
	pass



#Controls all the States of the Game 
class Game: 
	def __init__(self, screenW = 600, screenH = 600):
		self.screen = pygame.display.set_mode((screenW,screenH)) #Creating a Screen 
		pygame.display.set_caption("Tic Tac Toe") #Changing the name of the Window 

		self.states = [] #Creating a Empty Stack That will Store the states of the game 
		#Pushing the Game State 
		self.states.append(GameState()) #Right Now the GameState is On top of the Stack 
		
		pass

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
			self.states[len(self.states) - 1].update(mouseState) #Calling Update Method 
			
			pass
		pass

	def draw(self):
		#Calling the Draw Method of the Current State (Ensuring the States are not Empty)
		if len(self.states) > 0:
			#Peeking the Top State in the "Stack"
			self.states[len(self.states)-1].draw(self.screen)
			pass
		pass

def main():

	ticTacToe = Game()

	ticTacToe.start()
	pass


if __name__ == "__main__":
	main()
