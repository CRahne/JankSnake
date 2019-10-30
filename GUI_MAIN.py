from tkinter import *

root = Tk()
root.geometry('1920x1040+0+0')

root.configure(bg='white')

mainframe = Frame(root)
mainframe["bg"] = 'pink'
mainframe.grid(sticky=(N, W, E, S))

mainframe.columnconfigure(100, weight=50, minsize=49)

mainframe.rowconfigure(100, weight=50, minsize=49)

grid_list = [
    [" "," "," "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "," "," "]]

column_counter = -1
counter = 0
for x in grid_list:
    column_counter += 1
    row_counter = 0
    for y in x:
        print(f'{row_counter} | {column_counter}')
        grid_list[column_counter][row_counter] = counter
        this_Label = Label(mainframe, text=grid_list[column_counter][row_counter],bg='blue',padx=20,pady=20)
        this_Label.grid(column=column_counter, row=row_counter)
        counter += 1
        row_counter += 1