import pygame
from sudoku import solve, valid
import time
pygame.font.init()

class Grid:
    board = [
        [7,8,0,4,0,0,1,2,0],
        [6,0,0,0,7,5,0,0,9],
        [0,0,0,6,0,1,0,7,8],
        [0,0,7,0,4,0,2,6,0],
        [0,0,1,0,5,0,9,3,0],
        [9,0,4,0,6,0,0,0,5],
        [0,7,0,3,0,0,0,1,2],
        [1,2,0,0,0,7,4,0,0],
        [0,4,9,2,0,6,0,0,7]
    ]

    def __init__(self, rows, columns, width, height):
        self.rows = rows
        self.columns = columns
        self.width = width
        self.height = height
        self.model = None
        self.selected = None
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(columns)] for i in range(rows)]

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.columns)] for i in range(self.rows)]

    def place(self, value):
        row, column = self.selected
        if self.cubes[row][column].value == 0:
            self.cubes[row][column].set(value)
            self.update_model()

            if valid(self.model, value, (row, column)) and solve(self.model):
                return True
            else:
                self.cubes[row][column].set(0)
                self.cubes[row][column].set_temp(0)
                self.update_model()
                return False

    def sketch(self, value):
        row, column = self.selected
        self.cubes[row][column].set_temp(value)

    def draw(self, win):
        space = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i !=0:
                thickness = 4
            else:
                thickness = 1
            pygame.draw.line(win, (0, 0, 0), (0, i*space), (self.width, i * space), thickness)
            pygame.draw.line(win, (0, 0, 0), (i*space, 0), (i * space, self.height), thickness)

        for i in range(self.rows):
            for j in range(self.columns):
                self.cubes[i][j].draw(win)

    def select(self, row, column):
        for i in range(self.rows):
            for j in range(self.columns):
                self.cubes[i][j].selected = False
                
        self.cubes[row][column].selected = True
        self.selected = (row, column)

    def clear(self):
        row, column = self.selected
        if self.cubes[row][column].value == 0:
            self.cubes[row][column].set_temp(0)

    def click(self, position):
        if position[0] < self.width and position[1] < self.height:
            space = self.width / 9
            x = position[0] // space
            y = position[1] // space
            return (int(y), int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.cubes[i][j] == 0:
                    return False
        return True

class Cube:
    rows = 9
    columns = 9

    def __init__(self, value, row, column, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.column = column
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        font = pygame.font.SysFont("comicsans", 40)
        space = self.width / 9
        x = self.column * space
        y = self.row * space

        if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp), 1 , (128, 128, 128))
            win.blit(text, (x+5, y + 5))

        elif not(self.value == 0):
            text = font.render(str(self.value), 1 , (0, 0, 0))
            win.blit(text, (x + (space/2 - text.get_width()/2), y + (space/2 - text.get_height()/2)))
        
        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, space, space), 3)

    def set(self, value):
        self.value = value
    
    def set_temp(self, value):
        self.temp = value

def redraw_window(win, board, time, strikes):
    win.fill((255, 255, 255))

    font = pygame.font.SysFont("comicsans", 40)
    text = font.render("Time:" + format_time(time), 1, (0, 0, 0))
    
    text = font.render("X" * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))

    board.draw(win)
    
def format_time(secs):
    sec = secs%60
    minute = secs // 60
    hour = minute // 60

    tformat = " " + str(hour) + ":" + str(minute) + " : " + str(sec)
    return tformat

def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540)
    key = None
    run = True
    start = time.time()
    strikes = 0