from tkinter import *
import keyboard

root = Tk()
root.geometry('1920x1040+0+0')

root.configure(bg='white')

mainframe = Frame(root)
mainframe["bg"] = 'black'
mainframe.grid(sticky=(N, W, E, S))

#mainframe.columnconfigure(100, weight=50, minsize=49)
#
#mainframe.rowconfigure(100, weight=50, minsize=49)

grid_list = [
    ["N","0","1","2","3","4","5","6","7","8","9"],
    ["0"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
    ["1"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
    ["2"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
    ["3"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
    ["4"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
    ["5"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
    ["6"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
    ["7"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
    ["8"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
    ["9"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "]]
column_counter = -1
counter = 0
for x in grid_list:
    column_counter += 1
    row_counter = 0
    for y in x:
        theStringVar = grid_list[column_counter][row_counter]
        this_Label = Label(mainframe, text=theStringVar,bg='black',padx=10,pady=5)
        this_Label.grid(column=column_counter, row=row_counter)
        counter += 1
        row_counter += 1

def update():
    column_counter = -1
    counter = 0
    for x in grid_list:
        column_counter += 1
        row_counter = 0
        for y in x:
            theStringVar = grid_list[column_counter][row_counter]
            if (column_counter == 1 and row_counter == 1) or (column_counter == 1 and row_counter == 2) :
                this_Label = Label(mainframe, text=theStringVar, bg='yellow',padx=8,pady=2)
            else:
                this_Label = Label(mainframe, text=theStringVar,bg='black',fg='orange',padx=10,pady=5)
            this_Label.grid(column=column_counter, row=row_counter)
            counter += 1
            row_counter += 1
update()