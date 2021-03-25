"""Game of Life Simulator"""
from tkinter import * #import tkinter without needing to prepend 'tkinter'
import model #uses the functions from model.py

cell_size = 5 #used to scale the pixels
is_running = False #set the initial state of the program to false

def setup(): 
    global root, grid_view, cell_size, start_button, clear_button, choice

    root = Tk() #the top level window aka root
    root.title('The Game of Life')

    grid_view = Canvas(root, width=model.width*cell_size,   #this creates the board
                             height=model.height*cell_size,
                             borderwidth=0,
                             highlightthickness=0,
                             bg='white')

    start_button = Button(root, text = 'Start', width=12) #instantiate the 'Start' button
    start_button.bind('<Button-1>', start_handler) #binding the 'Start' button to event handler
    clear_button = Button(root, text = 'Clear', width=12) #instantiate the 'Clear' button
    clear_button.bind('<Button-1>', clear_handler)  #binding the 'Clear' button to event handler 

    choice = StringVar(root) #tk object, instantiate the option menu
    choice.set('Choose a Pattern') #instruction
    option = OptionMenu(root, choice, 'Choose a Pattern', #options
                                      'glider',
                                      'glider gun',
                                      'random',
                                command=option_handler) #argument for event handler
    option.config(width=20)
#uses grid method for placing the grid and buttons
    grid_view.grid(row=0, columnspan=3, padx=20, pady=20)
    grid_view.bind('<Button-1>', grid_handler) #binding the grid to event handler
    start_button.grid(row=1, column=0, sticky=W, padx=20, pady=20)
    option.grid(row=1, column=1, padx=20)
    clear_button.grid(row=1, column=2, sticky=E, padx=20, pady=20)

def grid_handler(event):
    global grid_view, cell_size

    x = int(event.x / cell_size) #use int if the coordinates are float
    y = int(event.y / cell_size) #divide by cell size for the exact coordinate

    if (model.grid_model[x][y] == 1): #if cell is alive then make it dead
        model.grid_model[x][y] = 0
        draw_cell(x, y, 'white')
    else:
        model.grid_model[x][y] = 1 #vice versa
        draw_cell(x, y, 'black')

def option_handler(event):
    global is_running, start_button, choice

    is_running = False  #make the simulation stop
    start_button.configure(text='Start') #then set the button to start

    selection = choice.get() #assign the chosen option to selection

    if selection == 'glider':
        model.load_pattern(model.glider_pattern, 10, 10)

    elif selection == 'glider gun':
        model.load_pattern(model.glider_gun_pattern, 10, 10)

    elif selection == 'random':
        model.randomize(model.grid_model, model.width, model.height)

    update()

def start_handler(event):
    global is_running, start_button

    if is_running:  
        is_running = False
        start_button.configure(text='Start')
    else:
        is_running = True
        start_button.configure(text='Pause')
        update()

def clear_handler(event):
    global is_running, start_button

    is_running = False
    start_button.configure(text='Start')
    for i in range(0, model.height):
        for j in range(0, model.width):
            model.grid_model[i][j] = 0
    update()
    

    

def update():
    global grid_view, root, is_running

    grid_view.delete(ALL)

    model.next_gen()
    for i in range(0, model.height):
        for j in range(0, model.width):
            if model.grid_model[i][j] == 1:
                draw_cell(i, j, 'black')
    if is_running:
        root.after(100, update) #call update function every 100 ms

def draw_cell(row, col, color):
    global grid_view, cell_size

    if color == 'black':
        outline = 'gray'
    else:
        outline = 'white'

    grid_view.create_rectangle(row*cell_size,           #creates the live cell using create_rectangle of tkinter
                               col*cell_size,
                               row*cell_size+cell_size,
                               col*cell_size+cell_size,
                               fill=color, outline=outline)

if __name__ == '__main__':
    setup()
    update()
    mainloop()




