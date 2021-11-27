from tkinter import *
from tkinter.ttk import *
from random import random
from collections import deque
from copy import deepcopy


lookup = {'v': 'Visited', 'e':'Empty', 'c':'Current', 's':'Start', 'b':'End', 'h':'Hurdle'}

class State():
    visited = "v"
    empty = "e"
    current = "c"
    start = "s"
    end = "b"
    hurdle = "h"
    path = "p"


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Board():
    def __init__(self, hurdle_rate = 30, rows = 10, columns = 10, start :Point = Point(0, 0), end : Point = Point(9, 9)):
        self.rows = rows
        self.columns = columns
        self.start_x = start.x
        self.start_y = start.y
        self.end_x = end.x
        self.end_y = end.y
        self.hurdle_rate = hurdle_rate
        self.board()
        self.add_hurdles()

    def board(self):
        self.board = [[State.empty for _ in range(self.columns)] for _ in range(self.rows)]


    def add_hurdles(self):
        for row in range(self.rows):
            for column in range(self.columns):
                if random() <= self.hurdle_rate/100:
                    self.board[row][column] = State.hurdle
        self.board[self.start_x][self.start_y] = State.start
        self.board[self.end_x][self.end_y] = State.end

class Maze():
    def __init__(self):
        self.main_window = Tk()
        self.main_window.geometry('1480x800')
        self.frame = Frame(self.main_window)
        self.frame.grid(row=0, column=0, sticky=N+S+W+E)
        self.initialize_styles()
        self.add_selection()
        self.main_window.mainloop()


    def setup_board(self, hurdle_rate, num_rows, num_cols, start_x, start_y, end_x, end_y):
        board = Board(hurdle_rate, num_rows, num_cols, Point(start_x, start_y), Point(end_x, end_y))
        self.board = deepcopy(board.board)
        self.duplicate_board = list(board.board)
        self.m = len(self.board)
        self.n = len(self.board[0])
        self.label_box = [[Label(self.frame) for _ in range(self.n)] for _ in range(self.m)]
        self.height = 480/len(self.board[0])/3
        self.width = 480/len(self.board)/2
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.dq = deque()
        self.dq.append((self.start_x,self.start_y))
        self.stack = []
        self.stack.append((self.start_x,self.start_y))
        self.visited = [[False for _ in range(self.n)] for _ in range(self.m)]
        self.visited_duplicate = [[False for _ in range(self.n)] for _ in range(self.m)]
        self.all_paths = []
        display_btn = Button(self.new_frame, text="Run BFS", command= lambda: self.run_bfs())
        display_btn.grid(row=7, column=1)
        display_btn = Button(self.new_frame, text="Run DFS", command= lambda: self.run_dfs())
        display_btn.grid(row=7, column=2)

    def initialize_styles(self):
        style = Style()
        style.theme_use('classic')
        style.configure(State.visited + ".TLabel", foreground="red", background="red")
        style.configure(State.empty + ".TLabel", foreground="#fac785", background="#fac785")
        style.configure(State.current + ".TLabel", foreground="green", background="green")
        style.configure(State.start + ".TLabel", foreground="purple", background="yellow")
        style.configure(State.end + ".TLabel", foreground="purple", background="yellow")
        style.configure(State.hurdle + ".TLabel", foreground="black", background="black")
        style.configure(State.path + ".TLabel", foreground="#538868", background="#538868")
        style.configure('w' + ".TLabel", foreground="ffe4c4", background="blue")
        style.configure('n' + ".TLabel", foreground="ffe4c4", background="#8dec61")
        style.configure(".TLabel", foreground="black", background="black")


    def display_grids(self):
        # self.frame.grid_forget()
        for row_idx, row in enumerate(self.board):
            for column_idx, column in enumerate(row):
                label = self.label_box[row_idx][column_idx]
                label.configure(style = column + ".TLabel")
                label.grid(row=row_idx, column=column_idx, ipadx=self.width, ipady=self.height, sticky=N+S+E+W)

    def add_selection(self):
        self.new_frame = Frame(self.main_window)
        self.new_frame.grid(row=0, column=50)
        
        label = Label(self.new_frame, text="Choose num of rows")
        label.grid(row=1, column=0)
        default_row = IntVar()
        default_row.set(10)
        options = [10]+[i for i in range(5, 21)]
        row_options = OptionMenu(self.new_frame, default_row, *options)
        row_options.grid(row=1, column=1)

        label = Label(self.new_frame, text="Choose num of columns")
        label.grid(row=2, column=0)
        default_col = IntVar()
        default_col.set(10)
        options = [10] + [i for i in range(5, 21)]
        col_options = OptionMenu(self.new_frame, default_col, *options)
        col_options.grid(row=2, column=1)

        label = Label(self.new_frame, text="Choose which row and col to start")
        label.grid(row=3, column=0)
        default_start_x = IntVar()
        default_start_x.set(0)
        options = [i for i in range(1, 15)]
        start_x_options = OptionMenu(self.new_frame, default_start_x, *options)
        start_x_options.grid(row=3, column=1)
        default_start_y = IntVar()
        default_start_y.set(0)
        options = [i for i in range(1, 15)]
        start_y_options = OptionMenu(self.new_frame, default_start_y, *options)
        start_y_options.grid(row=3, column=2)

        label = Label(self.new_frame, text="Choose which row and col to end")
        label.grid(row=4, column=0)
        default_end_x = IntVar()
        default_end_x.set(0)
        options = [9]+[i for i in range(0, 20)]
        end_x_options = OptionMenu(self.new_frame, default_end_x, *options)
        end_x_options.grid(row=4, column=1)
        default_end_y= IntVar()
        default_end_y.set(0)
        options = [9]+[i for i in range(0, 20)]
        end_y_options = OptionMenu(self.new_frame, default_end_y, *options)
        end_y_options.grid(row=4, column=2)

        label = Label(self.new_frame, text="Hurdle rate")
        label.grid(row=5, column=0)
        options = [i for i in range(0, 30, 5)]
        hurdle_default = IntVar()
        hurdle_default.set(30)
        hurdle_options = OptionMenu(self.new_frame, hurdle_default, *options)
        hurdle_options.grid(row=5, column=1)

        self.label_error = Label(self.new_frame, wraplength=400, font="Helvetica 20")
        self.label_error.grid(row=9, column=0)

        self.label_not_valid = Label(self.new_frame, wraplength=400, font="Helvetica 30")
        self.label_not_valid.grid(row=10, column=0)
        
        display_btn = Button(self.new_frame, text="Create Board", command= lambda: self.check(hurdle_default.get(), default_row.get(), default_col.get(), default_start_x.get(), default_start_y.get(), default_end_x.get(), default_end_y.get()))
        display_btn.grid(row=6, column=0, columnspan=2)


    def check(self, hurdle_rate, num_rows, num_cols, start_x, start_y, end_x, end_y):
        if start_x < num_rows and end_x < num_rows and start_y < num_cols and end_y < num_cols:
            self.label_error.configure(text=" ")
            self.label_not_valid.configure(text=" ")
            self.setup_board(hurdle_rate, num_rows, num_cols, start_x-1, start_y-1, end_x, end_y)
            self.display_grids()
        else:
            error = "Error: "
            if start_x >= num_rows:
                error += " The x co-ordinate of starting point is more than the number of rows."
            if start_y >= num_cols:
                error += " The y co-ordinate of starting point is more than the number of columns."
            if end_x >= num_rows:
                error += " The x co-ordinate of ending point is more than the number of rows."
            if end_y >= num_cols:
                error += " The y co-ordinate of ending point is more than the number of columns."
            error += " Please reconsider your co-ordinates again."
            self.label_error.configure(text=error)

    def show_path(self):
        for x, y in self.all_paths:
            self.board[x][y] = "p"
        self.display_grids()

    def run_dfs(self):
        self.board = deepcopy(self.duplicate_board)
        self.visited = deepcopy(self.visited_duplicate)
        self.display_grids()
        self.stack = [(self.start_x, self.start_y)]
        self.all_paths = []
        self.dfs()

    def dfs(self):
        x_coor, y_coor = self.stack.pop()

        if x_coor == self.end_x and y_coor == self.end_y:
            self.board[x_coor][y_coor] = 'w'
            self.show_path()
            return

        self.visited[x_coor][y_coor] = True

        self.board[x_coor][y_coor] = 'v'
        self.display_grids()

        self.all_paths.append((x_coor, y_coor))

        for i in [[1,0], [0,1], [-1,0], [0,-1]]:
            new_x, new_y = x_coor + i[0], y_coor + i[1]
            if 0 <= new_x < self.m and 0 <= new_y < self.n and (self.board[new_x][new_y] == 'e' or self.board[new_x][new_y] == 'b') and self.visited[new_x][new_y] == False:
                self.stack.append((new_x, new_y))

        self.board[x_coor][y_coor] = 'e'
        if not self.stack:
            error="Hurdles in between start and end point"
            self.label_not_valid.configure(text=error)
        self.frame.after(50, self.dfs)

    
    def run_bfs(self):
        self.board = deepcopy(self.duplicate_board)
        self.visited = deepcopy(self.visited_duplicate)
        self.dq = deque()
        self.dq.append((self.start_x, self.start_y))
        self.display_grids()
        self.bfs()

    def bfs(self):
        x_coor, y_coor = self.dq.popleft()
        if x_coor == self.end_x and y_coor == self.end_y:
            self.board[x_coor][y_coor] = 'w'
            self.display_grids()
            return
        self.visited[x_coor][y_coor] = True
        self.board[x_coor][y_coor] = 'v'
        self.display_grids()

        for i in [[1,0], [-1,0], [0,1], [0,-1]]:
            new_x, new_y = x_coor + i[0], y_coor + i[1]
            if 0 <= new_x < self.m and 0 <= new_y < self.n and (self.board[new_x][new_y] == 'e' or self.board[new_x][new_y] == 'b') and self.visited[new_x][new_y] == False:
                self.dq.append((new_x, new_y))
                self.board[new_x][new_y] = 'n'
                self.display_grids()
        if not self.dq:
            error="Hurdles in between start and end point"
            self.label_not_valid.configure(text=error)
        self.frame.after(20, self.bfs)


new_maze = Maze()