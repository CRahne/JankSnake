from tkinter import *
import keyboard
import time
import RPi.GPIO as GPIO
import random
import Constants

# Sets up the window
root = Tk()
root.geometry(f'{Constants.WindowWidth}x{Constants.WindowHeight}+0+0') # 1920x1040
root.configure(bg=Constants.WindowBackground)

# Sets the speed of the snake
Speed = Constants.SnakeSpeed

# Sets the button pin numbers
UpButton = Constants.UpButtonPin
DownButton = Constants.DownButtonPin
RightButton = Constants.RightButtonPin
LeftButton = Constants.LeftButtonPin

AddSection = False # Checks if a section needs to be added to the snake or not
GameOver = False # Checks if the snake has run into a wall or itself
DirectionChanged = False # Checks to see if the direction has been changed

# Sets up the starting values for the snake
NumberOfSections = Constants.NumberOfSections
HeadX = Constants.SnakeHeadX
HeadY = Constants.SnakeHeadY
BodyX = []
BodyY = []
SnakeDirection = Constants.SnakeDirection # 0 is up, 1 is right, 2 is down, 3 is left

# Declares variables to be used later
AppleX = 0
AppleY = 0

Labels = []

# Sets up the GPIO Pins so that button input can be detected
GPIO.setmode(GPIO.BCM)

# Resets the game once GameOver == True
def ResetGame():
    global BodyX
    global BodyY
    global HeadX
    global HeadY
    global GameOver
    global SnakeDirection
    global DirectionChanged
    global Speed
    
    # Pauses the program for 3 seconds
    time.sleep(3)
    
    # Removes the snake from the grid
    for x in range(len(BodyX)):
        Labels[BodyY[x]][BodyX[x]].config(bg = Constants.BackgroundColor)
    Labels[AppleY][AppleX].config(bg = Constants.BackgroundColor)
    
    # Resets all the snake variables
    HeadX = Constants.SnakeHeadX
    HeadY = Constants.SnakeHeadY
    SnakeDirection = Constants.SnakeDirection
    Speed = Constants.SnakeSpeed
    SnakeInit()
    DirectionChanged = False
    GenerateApple()
    GameOver = False


# Sets up the grid
def GridInit():
    ColumnCounter = -1
    RowCounter = 0
    for x in range(Constants.NumberOfRows):
        # Adds another array to Labels for every row in the grid
        Labels.append([])
        
    for x in range(Constants.NumberOfColumns):
        RowCounter =  0
        ColumnCounter += 1
        for y in range(Constants.NumberOfRows):
            # Adds a blank label to every spot in the grid
            Labels[RowCounter].insert(ColumnCounter, Label(root, text=" ",bg=Constants.BackgroundColor,padx=Constants.ColumnSize,pady=Constants.RowSize))
            Labels[RowCounter][ColumnCounter].grid(column = ColumnCounter, row = RowCounter)
            RowCounter+=1

# Puts the snake in it's starting position
def SnakeInit():
    global BodyX
    global BodyY
    BodyX = []
    BodyY = []
    for x in range(NumberOfSections):
        if(x != 0):
            # Sets up the Snake body depending on which way the snake is facing
            if(SnakeDirection == 0):
                BodyX.append(HeadX)
                BodyY.append(HeadY + x)
            elif(SnakeDirection == 1):
                BodyX.append(HeadX - x)
                BodyY.append(HeadY)
            elif(SnakeDirection == 2):
                BodyX.append(HeadX)
                BodyY.append(HeadY - 1)
            elif(SnakeDirection == 3):
                BodyX.append(HeadX + x)
                BodyY.append(HeadY)
                

# Draws the snake in the grid
def DrawSnake(BlackoutY,BlackoutX):
    global AddSection
    global BodyX
    global BodyY
    global GameOver
    global DirectionChanged
    global Speed
    if(GameOver == False):
        if(AddSection == False):
            # Changes the background color of the last snake section back to black
            Labels[BlackoutY][BlackoutX].config(bg=Constants.BackgroundColor)
        else:
            # Adds a section to the snake
            BodyX.append(BlackoutX)
            BodyY.append(BlackoutY)
            Speed -= Constants.SnakeSpeedAdd
            AddSection = False
        # Colors in the new head
        Labels[HeadY][HeadX].config(bg=Constants.SnakeHeadColor)
        # Colors in the body
        for x in range(len(BodyX)):
            Labels[BodyY[x]][BodyX[x]].config(bg=Constants.SnakeBodyColor)
        DirectionChanged = False


# Changes the Position of the snake based on the direction the snake is moving
def UpdateSnakePos():
    global HeadX
    global HeadY
    CheckSnakePos()
    if(GameOver == False):
        PrevHeadX = HeadX
        PrevHeadY = HeadY
        # Makes a copy of the previous body coordinates for reference
        PrevBodyX = BodyX.copy()
        PrevBodyY = BodyY.copy()
        # Changes the head coordinates based on the direction the snake is moving
        if(SnakeDirection == 0):
            HeadY-=1
        elif(SnakeDirection == 1):
            HeadX+=1
        elif(SnakeDirection == 2):
            HeadY+=1
        elif(SnakeDirection == 3):
            HeadX-=1
        # Changes the body coordinates
        for x in range(len(BodyX)):
                if(x == 0):
                    BodyX[0] = PrevHeadX
                    BodyY[0] = PrevHeadY
                else:
                    BodyX[x] = PrevBodyX[x-1]
                    BodyY[x] = PrevBodyY[x-1]
        
        CheckSnakePos()
        DrawSnake(PrevBodyY[-1], PrevBodyX[-1])


# Creates the main loop that moves the snake
def RunGame():
    UpdateSnakePos()
    root.after(Speed, RunGame)
    mainloop()


# Changes the snake's direction based on button input
def ButtonHandler(channel):
    global SnakeDirection
    global DirectionChanged
    if(DirectionChanged == False):
        if(channel == UpButton and SnakeDirection != 2):
            SnakeDirection = 0
        elif(channel == DownButton and SnakeDirection != 0):
            SnakeDirection = 2
        elif(channel == LeftButton and SnakeDirection !=1):
            SnakeDirection = 3
        elif(channel == RightButton and SnakeDirection != 3):
            SnakeDirection = 1
    DirectionChanged = True


# Checks if the snake has run into an apple, the edge, or itself
def CheckSnakePos():
    global AddSection
    global GameOver
    if(GameOver == False):
        if HeadX < 0 or HeadX > Constants.NumberOfColumns - 1 or HeadY < 0 or HeadY > Constants.NumberOfRows - 1:
            # Resets the game
            GameOver = True
            ResetGame()
        if(HeadX == AppleX and HeadY == AppleY):
            # Generates a new apple and adds a section to the body of the snake
            GenerateApple()
            AddSection = True
        for x in range(len(BodyX)):
            try:
                if BodyX[x] == HeadX and BodyY[x] == HeadY:
                    # Resets the game
                    GameOver = True
                    ResetGame()
            except:
                print("Try failed")


# Generates a new apple
def GenerateApple():
    global AppleX
    global AppleY
    AppleGenerated = False
    while(AppleGenerated == False):
        # Picks a random coordinates for the apple
        AppleX = random.randint(0,(Constants.NumberOfColumns - 1))
        AppleY = random.randint(0,(Constants.NumberOfRows - 1))
        if not(AppleX == HeadX and AppleY == HeadY):
            # Checks if the apple coordinates are empty
            for x in range(len(BodyX)):
                if(AppleX == BodyX[x] and AppleX == BodyY[x]):
                    AppleGenerated = False
                    break
                else: AppleGenerated = True
    # Colors in the apple
    Labels[AppleY][AppleX].config(bg = Constants.AppleColor)
        

# Sets up the snake and the grid
SnakeInit()
GridInit()

# Starts the game loop after 500 milliseconds
root.after(500,RunGame)
root.after(750,GenerateApple)


# Adds event catchers for all of the buttons
GPIO.setup(UpButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(UpButton, GPIO.RISING, callback=ButtonHandler, bouncetime=Constants.UpButtonBouncetime)

GPIO.setup(DownButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(DownButton, GPIO.RISING, callback=ButtonHandler, bouncetime=Constants.DownButtonBouncetime)

GPIO.setup(LeftButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(LeftButton, GPIO.RISING, callback=ButtonHandler, bouncetime=Constants.LeftButtonBouncetime)

GPIO.setup(RightButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(RightButton, GPIO.RISING, callback=ButtonHandler, bouncetime=Constants.RightButtonBouncetime)
