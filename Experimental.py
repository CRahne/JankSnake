from tkinter import *
import keyboard
import time
import RPi.GPIO as GPIO 

root = Tk()
root.geometry('1920x1040+0+0')

CurrentTime = 0
PrevTime = 0

root.configure(bg='white')

mainframe = Frame(root)
mainframe["bg"] = 'black'
mainframe.grid(sticky=(N, W, E, S))

SnakeHeadColor = 'green'
SnakeBodyColor = 'yellow'
BackgroundColor = 'black'

Initialized = False

HeadX = 10
HeadY = 10
BodyX = [11, 12]
BodyY = [10, 10]
PrevSnakeEndX = 0
PrevSnakeEndY = 0

SnakeDirection = 3 # 0 is up, 1 is right, 2 is down, 3 is left

Labels = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

GPIO.setmode(GPIO.BCM)

def GridInit():
    ColumnCounter = -1
    RowCounter = 0
    for x in range(20):
        RowCounter =  0
        ColumnCounter += 1
        for y in range(20):
            Labels[RowCounter].insert(ColumnCounter, Label(mainframe, text=" ",bg=BackgroundColor,padx=10,pady=5))
            Labels[RowCounter][ColumnCounter].grid(column = ColumnCounter, row = RowCounter)
            RowCounter+=1
            if(y == 19 and x == 19): Initialized = True

def DrawSnake():
    Labels[HeadY][HeadX].config(bg=SnakeHeadColor)
    for x in range(len(BodyX)):
        Labels[BodyY[x]][BodyX[x]].config(bg=SnakeBodyColor)
    Labels[PrevSnakeEndY][PrevSnakeEndX].config(bg=BackgroundColor)


def UpdateSnakePos(channel):
    time.sleep(1)
    global HeadX
    global HeadY
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
        
    Labels[PrevBodyY[-1]][PrevBodyX[-1]].config(bg=BackgroundColor)
    DrawSnake()

GridInit()

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(18, GPIO.RISING, callback=UpdateSnakePos, bouncetime=1000)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(23, GPIO.RISING, callback=UpdateSnakePos, bouncetime=1000)

GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(24, GPIO.RISING, callback=UpdateSnakePos, bouncetime=1000)

GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(25, GPIO.RISING, callback=UpdateSnakePos, bouncetime=1000)

GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(4, GPIO.RISING, callback=UpdateSnakePos, bouncetime=1000)
    

