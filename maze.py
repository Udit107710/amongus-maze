from tkinter import *
import numpy as np
import random
import time
import math

#pylint: skip-file

"""Information:
Board is 9x3 (much wider)
19 width, 7 height
"""

class Maze():
    def __init__(self):  
        self.tkroot = Tk()
        self.color = '#a6a48f'
        self.debug = False

    def input(self):
        """Initialize canvas"""
        self.canvas = Canvas(self.tkroot, width=950, height=350)
        self.canvas.pack(expand=True, fill=BOTH)
        self.canvas.configure(bg=self.color)

        """Entries:
        Default is 19x7 board
        """
        self.eheight = Entry(self.tkroot, font='Times 16')
        self.ewidth = Entry(self.tkroot, font='Times 16')
        self.eheight.insert(END, 7)
        self.ewidth.insert(END, 19)
        self.canvas.create_window(450, 150, anchor=CENTER, window=self.eheight)
        self.canvas.create_window(450, 200, anchor=CENTER, window=self.ewidth)

        """Home screen text"""
        self.canvas.create_text(450, 50, font='Times 30 bold', text="Among Us Maze Task")
        self.canvas.create_text(300, 150, font='Times 20', text="Height: ")
        self.canvas.create_text(300, 200, font='Times 20', text="Width: ")

        """Input button"""
        self.begin_button = Button(self.canvas, font='Times 20', text="Begin", command=lambda:self.begin())
        self.canvas.create_window(450, 300, anchor=CENTER, window=self.begin_button)
        self.tkroot.mainloop()

    """Errors:
    Inputs must be integer and odd
    """
    def error_screen(self):
        self.canvas.pack_forget() #Temporarily hide the home screen

        """Create new temporary canvas"""
        self.errorc = Canvas(self.tkroot, width=950, height=350)
        self.errorc.pack(expand=True, fill=BOTH)
        self.errorc.configure(bg=self.color)

        self.errorc.create_text(450, 100, font='Times 20', text="Make sure the height and width you put are odd integers!")

        """Button for returning to home screen"""
        self.go_back = Button(self.errorc, text="Return to main page", 
            command=lambda:[self.errorc.destroy(), self.canvas.pack()])
        self.errorc.create_window(450, 250, anchor=CENTER, window=self.go_back)

    def begin(self):
        try:
            self.height = int(self.eheight.get())
            self.width = int(self.ewidth.get())

            """inputs must be odd"""
            if self.height%2 == 0 or self.width%2 == 0:
                print("Not odd")
                raise Exception("Error")
            
            """Destroy old canvas and reinitalize new one of appropriate size"""
            self.canvas.destroy()
            self.canvas = Canvas(self.tkroot, width=50*self.width, height=50*self.height)
            self.canvas.pack(expand=True, fill=BOTH)
            self.canvas.configure(bg='#a6a48f')
        except:
            self.error_screen() #If not successful, go to error screen

        self.setup() #Execute setup command if everything else is successful

    def setup(self):
        """Initialize square pegs:
        I did this section first, which is why the code is quite naive;
        More space efficient in the future could be using the final_grid created to insert the square pegs
        """
        self.square_img = PhotoImage(file="resized_square.png") #Square peg thing image for maze task
        for i in range(math.floor(self.width/2)+1):
            for j in range(math.floor(self.height/2)+1):
                self.canvas.create_image(100*i, 100*j, anchor=NW, image=self.square_img)

        """Call DFS algorithm:
        Keep trying until algorithm finds a maze that works
        """
        self.retries = 0
        while True:
            try: 
                self.grid = np.zeros([self.height, self.width], dtype=np.int8)
                self.vis = np.zeros([self.height, self.width])
                self.final_grid, self.peg, self.barrier, self.no_barrier, self.count = self.dfs(self.grid, 
                    self.vis, 1, 1, 0)
                self.final_grid[0][1] = self.no_barrier #Start point cannot have barrier
                self.final_grid[self.height-1][self.width-2] = self.no_barrier #End point cannot have barrier
                print("Number of retries: %d \n Length of Path: %d" % (self.retries, self.count))
                break
            except:
                self.retries += 1
                pass
        
        """Add random barriers"""  
        self.total_spots = math.floor(self.width/2)*(math.floor(self.height/2)+1) + math.floor(self.height/2)*(math.floor(
            self.width/2)+1) #Total spots given configuration
        self.num_barriers = random.randint(int(self.total_spots*0.45), int(self.total_spots*0.55)) #45% to 55% of the board is barrier
        self.final_grid = self.add_barriers(self.final_grid, self.num_barriers)
        print("Number of barriers: %d" % self.num_barriers)

        """Initialize barriers"""
        self.topdown = PhotoImage(file="topdown_resize.png")
        self.leftright = PhotoImage(file="leftright_resize.png")

        for i in range(self.height):
            for j in range(self.width):
                if self.final_grid[i][j] == 8:
                    if i%2 == 1:
                        self.canvas.create_image(12.5+50*j, 50*i+0.4, anchor=NW, image=self.topdown) #create_image=(width, height)
                    else:
                        self.canvas.create_image(50*j+2, 12.5+50*i, anchor=NW, image=self.leftright)

        """Initialize variables"""
        self.tkroot.setvar(name="xvar", value=50)
        self.tkroot.setvar(name="yvar", value=0)
        self.tkroot.setvar(name="xvis", value=1)
        self.tkroot.setvar(name="yvis", value=0)
        self.tkroot.setvar(name="done", value=0)
        self.visited = []

        """Bind buttons"""
        self.canvas.bind('<B1-Motion>', self.draw_line)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

        self.start = time.perf_counter() #Start of timer
        self.local_start = time.perf_counter()

    """Depth first search algorithm:
    Finds a possible maze;
    Legends are defined by numbers and found in the comments below;
    Semi-naive, could use self.peg/self.barrier/self.no_barrier initializations
    """
    def dfs(self, grid, vis, i, j, count):
        grid[i][j] = 1
        """
        North - 0
        East - 1
        South - 2
        West - 3
        """

        """Legend
        7 - Peg
        8 - Barrier
        9 - None
        """
        peg = 7
        barrier = 8
        no_barrier = 9

        """Stop at end"""
        if i == self.height-2 and j == self.width-2:
            return grid, peg, barrier, no_barrier, count

        possible_dir = [] #Array of possible directions

        """North"""
        if i != 1:
            if vis[i-2][j] == 0:
                possible_dir.append(0)
                vis[i-2][j] = 1

        """South"""
        if i != self.height-2:
            if vis[i+2][j] == 0:
                possible_dir.append(2)
                vis[i+2][j] = 1

        """West"""
        if j != 1:
            if vis[i][j-2] == 0:
                possible_dir.append(3)
                vis[i][j-2] = 1
        
        """East"""
        if j != self.width-2:
            if vis[i][j+2] == 0:
                possible_dir.append(1)   
                vis[i][j+2] = 1 

        direction = np.random.choice(possible_dir, 1)
        if direction == 0:
            grid[i-1][j] = no_barrier
            return self.dfs(grid, vis, i-2, j, count+1)
        if direction == 1:
            grid[i][j+1] = no_barrier
            return self.dfs(grid, vis, i, j+2, count+1)
        if direction == 2:
            grid[i+1][j] = no_barrier
            return self.dfs(grid, vis, i+2, j, count+1)
        if direction == 3:
            grid[i][j-1] = no_barrier
            return self.dfs(grid, vis, i, j-2, count+1)

    """Driver function for adding barriers, used above"""
    def add_barriers(self, grid, num):
        """Add pegs into the grid (so those grid spots are ignored when tracking motion)"""
        for i in range(0, self.height, 2):
            for j in range(0, self.width, 2):
                grid[i][j] = self.peg

        while num:
            direction = np.random.choice(['LR', 'UD'], 1)
            if direction == 'LR':
                i = np.random.choice(np.arange(0, self.height, 2))
                j = np.random.choice(np.arange(1, self.width, 2))
            else:
                i = np.random.choice(np.arange(1, self.height, 2))
                j = np.random.choice(np.arange(0, self.width, 2))
            if grid[i][j] == 0:
                grid[i][j] = self.barrier
                num -= 1

        return grid

    """Draw Line Function:
    Tracks cursor motion and leaves a trail;
    There is an issue of skipping corners;
    Sensitivity could be improved/optimized;
    Math is very dependent on 50 pixel grid squares;
    Real Among Us is not just 50 pixel grid squares, therefore this function is not that flexible;

    Code specific -
    Keep track of visited array so you cannot visit the same square (error: sometimes the grid square isn't drawn in but
    the code assumes you are there so you cannot visit the square you were at previously)
    """
    def draw_line(self, event):
        y = int(event.y/50) #y pos of cursor
        x = int(event.x/50) #x pos of cursor
        if y >= self.height or x >= self.width:
            return #Don't go off screen

        """Read as if NOT peg AND NOT visited and NOT visited then keep going"""
        val = self.final_grid[y][x]
        if val != 7 and val != 8 and [x, y] not in self.visited:
            xc = self.tkroot.getvar(name="xvar")
            yc = self.tkroot.getvar(name="yvar")
            if yc == 0 and xc == 50:
                if yc+75 > event.y > yc+50 and xc < event.x < xc+50:
                    self.tkroot.setvar(name="yvar", value=yc+50)
                    self.canvas.create_rectangle(xc, yc, xc+50, yc+50, fill='white', width=0, tag="line")

            else:
                """y-axis then x-axis motion"""
                if xc < event.x < xc+50:
                    if event.y > yc+25:
                        self.canvas.create_rectangle(xc, yc, xc+50, yc+50, fill='white', width=0, tag="line")
                        self.canvas.create_rectangle(xc, yc, xc+50, yc+50, fill='yellow', width=0, tag="tmp")
                        self.done = self.tkroot.getvar(name="done")
                        if x == self.width-2 and y == self.height-1 and not self.done:
                            self.tkroot.setvar(name="done", value=1)
                            self.congrats()
                    elif yc-49 < event.y < yc-25:
                        self.canvas.create_rectangle(xc, yc-50, xc+50, yc, fill='white', width=0, tag="line")
                        self.canvas.create_rectangle(xc, yc-50, xc+50, yc, fill='yellow', width=0, tag="tmp")
                elif yc < event.y < yc+50:
                    if event.x > xc+25:
                        self.canvas.create_rectangle(xc, yc, xc+50, yc+50, fill='white', width=0, tag="line")
                        self.canvas.create_rectangle(xc, yc, xc+50, yc+50, fill='yellow', width=0, tag="tmp")
                    elif xc-49 < event.x < xc-25:
                        self.canvas.create_rectangle(xc-50, yc, xc, yc+50, fill='white', width=0, tag="line")
                        self.canvas.create_rectangle(xc-50, yc, xc, yc+50, fill='yellow', width=0, tag="tmp")
                
                xvis = self.tkroot.getvar(name="xvis")
                yvis = self.tkroot.getvar(name="yvis")
                if xc < event.x < xc+50:
                    if yc+99 > event.y > yc+50:
                        self.tkroot.setvar(name="yvar", value=yc+50)
                        self.visited.append([x, y-1])
                        self.tkroot.setvar(name="yvis", value=yvis+1)
                    elif yc-49 < event.y < yc-25:
                        self.tkroot.setvar(name="yvar", value=yc-50)
                        self.visited.append([x, y+1])
                        self.tkroot.setvar(name="yvis", value=yvis-1)

                    if yc+49 <= event.y <= yc+60 or yc+1 >= event.y >= yc-10:
                        self.canvas.itemconfig("tmp", fill="white") #Remove trail
                elif yc < event.y < yc+50:
                    if xc+99 > event.x > xc+50:
                        self.tkroot.setvar(name="xvar", value=xc+50)
                        self.visited.append([x-1, y])
                        self.tkroot.setvar(name="xvis", value=xvis+1)
                    elif xc-49 < event.x < xc-25:
                        self.tkroot.setvar(name="xvar", value=xc-50)
                        self.visited.append([x+1, y])
                        self.tkroot.setvar(name="xvis", value=xvis-1)
                    
                    if xc+49 <= event.x <= xc+60 or xc+1 >= event.x >= xc-10:
                        self.canvas.itemconfig("tmp", fill="white") #Remove trail
            
            if self.debug:
                print(int(event.x/50), int(event.y/50), xc, yc)

        if self.debug and [x, y] in self.visited:
            #print(self.visited)
            print('Value: %d' % val)

    """Reset if mouse is released"""
    def reset(self, event):
        self.canvas.delete("line")
        self.canvas.delete("tmp")
        self.tkroot.setvar(name="xvar", value=50)
        self.tkroot.setvar(name="yvar", value=0)
        self.tkroot.setvar(name="xvis", value=1)
        self.tkroot.setvar(name="yvis", value=0)
        self.tkroot.setvar(name="done", value=0)
        self.visited.clear()
        self.local_start = time.perf_counter()
        print('Reset')

    """Congratulations screen"""
    def congrats(self):
        self.end = time.perf_counter() #End timer
        print('Congratulations on finishing the maze!')

        """Initialize new canvas"""
        self.congratsc = Canvas(self.tkroot, width=950, height=350) #Each space is 50px
        self.congratsc.pack(expand=True, fill=BOTH)
        self.congratsc.configure(bg='#a6a48f')
        self.canvas.pack_forget()

        self.congratsc.create_text(450, 75, font="Times 16 bold", text="Congratulations! You completed the maze in %.3f seconds for a total of %.3f seconds."
            % (float(self.end)-float(self.local_start), float(self.end)-float(self.start)))

        """Recover old maze"""
        self.recover = Button(self.congratsc, text="Try the maze again", command=lambda:[self.congratsc.pack_forget(), self.canvas.pack(), self.reinit_timer()])
        self.congratsc.create_window(400, 200, anchor=CENTER, window=self.recover)

        """Create new maze"""
        self.new_maze = Button(self.congratsc, text="New maze!", command=lambda:[self.congratsc.pack_forget(), self.canvas.pack(), self.setup()])
        self.congratsc.create_window(500, 200, anchor=CENTER, window=self.new_maze)

    """Reinitialize timer"""
    def reinit_timer(self):
        self.start = time.perf_counter()
        self.local_start = time.perf_counter()

maze = Maze()
maze.input()