from tkinter import *
import keyboard
import time
import RPi.GPIO as GPIO
import random
import Constants

root = Tk()
root.geometry(f'{Constants.WindowWidth}x{Constants.WindowHeight}+0+0') # 1920x1040
root.configure(bg=Constants.WindowBackground)

Speed = Constants.SnakeSpeed

UpButton = Constants.UpButtonPin
DownButton = Constants.DownButtonPin
RightButton = Constants.RightButtonPin
LeftButton = Constants.LeftButtonPin

SnakeHeadColor = 'green'
SnakeBodyColor = 'yellow'
BackgroundColor = 'black'

AddSection = False
GameOver = False
DirectionChanged = False

NumberOfSections = Constants.NumberOfSections
HeadX = Constants.SnakeHeadX
HeadY = Constants.SnakeHeadY
BodyX = []
BodyY = []
SnakeDirection = Constants.SnakeDirection # 0 is up, 1 is right, 2 is down, 3 is left

AppleX = 0
AppleY = 0

PrevSnakeEndX = 0
PrevSnakeEndY = 0

Labels = []# [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

GPIO.setmode(GPIO.BCM)

def ResetGame():
    global BodyX
    global BodyY
    global HeadX
    global HeadY
    global GameOver
    global SnakeDirection
    global DirectionChanged
    time.sleep(3)
    for x in range(len(BodyX)):
        Labels[BodyY[x]][BodyX[x]].config(bg = BackgroundColor)
    # Labels[HeadY][HeadX].config(bg = BackgroundColor)
    Labels[AppleY][AppleX].config(bg = BackgroundColor)
    HeadX = Constants.SnakeHeadX
    HeadY = Constants.SnakeHeadY
    SnakeDirection = Constants.SnakeDirection
    SnakeInit()
    DirectionChanged = False
    GenerateApple()
    GameOver = False

def GridInit():
    ColumnCounter = -1
    RowCounter = 0
    for x in range(Constants.NumberOfRows):
        Labels.append([])
    for x in range(Constants.NumberOfColumns):
        RowCounter =  0
        ColumnCounter += 1
        for y in range(Constants.NumberOfRows):
            Labels[RowCounter].insert(ColumnCounter, Label(root, text=" ",bg=BackgroundColor,padx=Constants.ColumnSize,pady=Constants.RowSize))
            Labels[RowCounter][ColumnCounter].grid(column = ColumnCounter, row = RowCounter)
            RowCounter+=1

def SnakeInit():
    global BodyX
    global BodyY
    BodyX = []
    BodyY = []
    for x in range(NumberOfSections):
        if(x != 0):
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
                
                
def DrawSnake(BlackoutY,BlackoutX):
    global AddSection
    global BodyX
    global BodyY
    global GameOver
    global DirectionChanged
    if(GameOver == False):
        if(AddSection == False):
            Labels[BlackoutY][BlackoutX].config(bg=BackgroundColor)
        else:
            BodyX.append(BlackoutX)
            BodyY.append(BlackoutY)
            AddSection = False
        Labels[HeadY][HeadX].config(bg=SnakeHeadColor)
        for x in range(len(BodyX)):
            Labels[BodyY[x]][BodyX[x]].config(bg=SnakeBodyColor)
        Labels[PrevSnakeEndY][PrevSnakeEndX].config(bg=BackgroundColor)
        DirectionChanged = False


def UpdateSnakePos():
    global HeadX
    global HeadY
    CheckSnakePos()
    if(GameOver == False):
        PrevHeadX = HeadX
        PrevHeadY = HeadY
        PrevBodyX = BodyX.copy()
        PrevBodyY = BodyY.copy()
        if(SnakeDirection == 0):
            HeadY-=1
        elif(SnakeDirection == 1):
            HeadX+=1
        elif(SnakeDirection == 2):
            HeadY+=1
        elif(SnakeDirection == 3):
            HeadX-=1
        for x in range(len(BodyX)):
                if(x == 0):
                    BodyX[0] = PrevHeadX
                    BodyY[0] = PrevHeadY
                else:
                    BodyX[x] = PrevBodyX[x-1]
                    BodyY[x] = PrevBodyY[x-1]
        CheckSnakePos()
        DrawSnake(PrevBodyY[-1], PrevBodyX[-1])

def RunGame():
    UpdateSnakePos()
    root.after(Speed, RunGame)
    mainloop()

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

def CheckSnakePos():
    global AddSection
    global GameOver
    if(GameOver == False):
        if HeadX < 0 or HeadX > Constants.NumberOfColumns - 1 or HeadY < 0 or HeadY > Constants.NumberOfRows - 1:
            GameOver = True
            ResetGame()
        if(HeadX == AppleX and HeadY == AppleY):
            GenerateApple()
            AddSection = True
        for x in range(len(BodyX)):
            try:
                if BodyX[x] == HeadX and BodyY[x] == HeadY:
                    GameOver = True
                    ResetGame()
            except:
                print("Try failed")

def GenerateApple():
    global AppleX
    global AppleY
    AppleGenerated = False
    while(AppleGenerated == False):
        AppleX = random.randint(0,(Constants.NumberOfColumns - 1))
        AppleY = random.randint(0,(Constants.NumberOfRows - 1))
        if not(AppleX == HeadX and AppleY == HeadY):
            for x in range(len(BodyX)):
                if(AppleX == BodyX[x] and AppleX == BodyY[x]):
                    AppleGenerated = False
                    break
                else: AppleGenerated = True
    Labels[AppleY][AppleX].config(bg = 'red')
        

SnakeInit()
GridInit()
root.after(500,RunGame)
root.after(750,GenerateApple)


GPIO.setup(UpButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(UpButton, GPIO.RISING, callback=ButtonHandler, bouncetime=1000)

GPIO.setup(DownButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(DownButton, GPIO.RISING, callback=ButtonHandler, bouncetime=1000)

GPIO.setup(LeftButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(LeftButton, GPIO.RISING, callback=ButtonHandler, bouncetime=1000)

GPIO.setup(RightButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(RightButton, GPIO.RISING, callback=ButtonHandler, bouncetime=1000)

GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(4, GPIO.RISING, callback=ButtonHandler, bouncetime=1000)


