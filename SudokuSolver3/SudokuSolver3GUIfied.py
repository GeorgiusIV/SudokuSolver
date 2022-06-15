import pygame
from sys import exit

print('THE RIGHT FILE')

pygame.init()

SCREENWIDTH, SCREENHEIGHT = 400, 400
RESOLUTION = (SCREENWIDTH, SCREENHEIGHT)
CELLWIDTH, CELLHEIGHT = SCREENWIDTH//9, SCREENHEIGHT//9
SCREEN = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption('Sudoku Solver')
CLOCK = pygame.time.Clock()

SUDOKU_FONT = pygame.font.Font(None, 12)

class Cell():
    def __init__(self, x = 0, y = 0, entry = 0):
        # coords begin from the top left
        self.x = x
        self.y = y
        self.entry = entry

        if self.entry == 0:
            self.static = True
        else:
            self.static = False


# draw lines 
# colour blind friendly?
# fill grid one of three colours
# green = current square
# faded red = point to return to
# grey = unsolved

# place surfaces, fill them with fonts

def eventHandler():
    if event.type == event.QUIT: 

def solveSudoku():

    def createGrid(SCREEN, CELLWIDTH, CELLHEIGHT, cells = list()):
        # returns a list of Cell() objects
        # Cell().entry = 0 and the x and y coords are distributed evenly
        # incomplete

        cells = list()
        for c in range(0,9*9):
            cells.append(Cell(x = CELLWIDTH*c, y = CELLHEIGHT%9, entry = 0))
            
            # i dont really like how i display things on the screen mid function
            # this feels like it should be separate
            if (c < 9):
                pygame.draw.line(SCREEN, 'BLACK', (CELLWIDTH*c, 0), (CELLWIDTH*c, SCREENHEIGHT), 1)
                pygame.draw.line(SCREEN, 'BLACK', (0, CELLHEIGHT*c), (SCREENWIDTH, CELLHEIGHT*c), 1)

        return cells

    pass
    #insertSudoku = True
    insertSudoku = False
    cells = createGrid(SCREEN, CELLWIDTH, CELLHEIGHT)
    while insertSudoku:
        pass

    while not insertSudoku:
        pass

        # CREATE GRID
        
            


    pygame.quit()
    print('EXIT FILE')
    exit()