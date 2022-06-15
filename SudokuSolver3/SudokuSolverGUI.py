
import pygame
from sys import exit

pygame.init()

SCREENWIDTH, SCREENHEIGHT = 400, 400
RESOLUTION = (SCREENWIDTH, SCREENHEIGHT)
CELLWIDTH, CELLHEIGHT = SCREENWIDTH//9, SCREENHEIGHT//9
SCREEN = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption('Sudoku Solver')
CLOCK = pygame.time.Clock()

BLACK = (0, 0, 0)
GRAY = (92, 92, 92)
LIGHTGRAY = (204, 204, 204)
DARKGREEN = '#004D40'
YELLOW = '#FFC107'

INITIALSUDOKU = [9,0,8,3,1,0,0,6,0,
                  0,0,0,0,0,6,0,9,7,
                  0,5,0,0,0,0,8,0,0,
                  2,0,0,0,0,0,1,4,0,
                  0,6,4,0,3,0,9,8,0,
                  0,1,9,0,0,0,0,0,3,
                  0,0,5,0,0,0,0,1,0,
                  7,9,0,4,0,0,0,0,0,
                  0,8,0,0,9,2,4,0,5]




def main():


    class Cell():
        """
        This object is called from the Sudoku object where all the x,y and entry values are defined for it
        all of the necessary values to translate the entry onto the screen are here
        renderEntry appropriately positions the box on the screen and colours it in
        makeSubCells controls which entries are not hints and therefore can have possible entries
        rewriteSubCells allows the subcell list to be deleted as the program backtracks in the Sudoku.solve() function
        """
        def __init__(self, x = 0, y = 0, w = CELLWIDTH, h = CELLHEIGHT, entry = 0):
            self.x = x
            self.y = y
            self.font = pygame.font.Font(None, w)

            self.entry = entry
            if entry != 0: 
                self.ishint = True  
                self.subCells = None
            else:
                self.ishint = False
                self.subCells = self.makeSubCells()
            self.Surf = None
            self.Rect = pygame.Rect((x,y), (w,h)) 
            self.textPosition = None    

        def renderEntry(self, color = 'BLACK', background = None):
            self.Surf = self.font.render(str(self.entry), True, color, background) 
            textRect = self.Surf.get_rect()
            self.textPosition = (self.Rect.center[0] - textRect.width//2, self.Rect.center[1] - textRect.height//2)
            return self.Surf

        def makeSubCells(self):
            subCells = list() 
            for i in range(0,9):
                w, h = CELLWIDTH//3, CELLHEIGHT//3
                x = self.x + w*(i%3)
                y = self.y + h*(i//3)
                
                subCells.append(Cell(x, y, w, h, entry = ''))
            return subCells

        def rewriteSubCells(self, entries = list(''*9)):

            shortestLen = min(len(self.subCells),len(entries))
            longestLen = max(len(self.subCells),len(entries))
            for s in range(shortestLen):
                self.subCells[s].entry = str(entries[s])
            for l in range(shortestLen,longestLen):
                self.subCells[l].entry = ''


    class Sudoku():
        """
        Receives a list input of 81 sudoku entries
        Converts each entry into a cell object, which is stored in 'cells'
        Holds the solve command, the main function of the code
        """

        def __init__(self, initialsudoku, x = CELLWIDTH, y = CELLHEIGHT):
            
            self.solved = False
            self.initial = initialsudoku
            self.cells = list()
            self.reInitialise()

        def __repr__(self):
            # this function produces easy output for debugging via the print(objectInstance) command
            printString = '---------'
            for c, cell in enumerate(self.cells):
                if c%9 == 0:
                    printString += '\n'
                printString += str(cell.entry)
                
            printString += '\n --------- \n'
            return printString
                
        def reInitialise(self):
            self.solved = False
            self.cells = list()
            for c in range(0,9*9):
                self.cells.append(Cell(x = CELLWIDTH*(c%9), y = CELLHEIGHT*(c//9), entry = self.initial[c]))

        def solve(self, index = 0, optionsDict = dict()):
            """
            Returns a generator object of the sudoku run through a backtracking algorithm
            Every step yields a 'cells' object at each stage - to be displayed on the screen 
            The function then checks if it is complete
            If not, it uses the findRow, findCol, findBox functions inside findOptions, to produce a list of possible values for the current index
            And iterates through the available options until either a solution has been found or there are no more options
            in the event of no more options, the function will backtrack until it finds a possible entry earlier in the tree and will continue from there
            The possible options are tracked on the display using the subcells in the cell object
            """

            def checkSolved():
                solved = True
                for cell in self.cells:
                    if cell.entry == 0:
                        solved = False
                return solved
      
            def findRow(index):
                row = set()
                start = index - (index % 9)
                end = start + 9
                for c in range(start,end):
                    row.add(self.cells[c].entry)
                return row

            def findCol(index):
                col = set()
                start = index % 9
                end = start + 81
                for c in range(start,end,9):
                    col.add(self.cells[c].entry)
                return col

            def findBox(index):
                box = set()
                start = (index//27)*27 + (index%9) - index%3
                for i in range(0,3):
                    box.add(self.cells[start+0 +9*i].entry)
                    box.add(self.cells[start+1 +9*i].entry)
                    box.add(self.cells[start+2 +9*i].entry)
                return box

            def findOptions(index):

                allOptions = set([1,2,3,4,5,6,7,8,9])
                row = findRow(index)
                rowOptions = set(allOptions).difference(row)
                col = findCol(index)
                colOptions = set(allOptions).difference(col)
                box = findBox(index)
                boxOptions = set(allOptions).difference(box)

                return rowOptions & colOptions & boxOptions

            yield self.cells
            
            if checkSolved():
                self.solved = True 

            elif self.cells[index].entry != 0:
                if not self.solved:
                    yield from self.solve(index+1, optionsDict)

            else:
                options = findOptions(index)
                optionsDict.update({index:options})

                while len(options) > 0:
                    tryOption = options.pop()
                    optionsDict.update({index:options})

                    self.cells[index].entry = tryOption
                    if self.cells[index].subCells:
                        self.cells[index].rewriteSubCells(list(options))

                    if not self.solved:
                        yield from self.solve(index+1, optionsDict)

                optionsDict.pop(index)
                self.cells[index].entry = 0
                if self.cells[index].subCells:
                    self.cells[index].rewriteSubCells()
            
            return None


    def drawGrid(SCREEN, CELLWIDTH, CELLHEIGHT, cells):
        """
        Renders cells' text to the screen
        Colours cells' boxes in a colour-blind friendly manner
        Draws sudoku grid lines
        """

        # CELL TEXT & COLOURS
        for cell in cells:

            if cell.ishint:
                pygame.draw.rect(SCREEN, DARKGREEN, cell.Rect)
                cell.renderEntry(color = LIGHTGRAY)
                SCREEN.blit(cell.Surf, cell.textPosition)

            if not cell.ishint and cell.entry != 0:
                pygame.draw.rect(SCREEN, YELLOW, cell.Rect)
                cell.renderEntry(color = BLACK)
                SCREEN.blit(cell.Surf, cell.textPosition)

            if not cell.ishint and cell.subCells:
                for subcell in cell.subCells:
                    subcell.renderEntry(color = GRAY, background = None)
                    SCREEN.blit(subcell.Surf, subcell.textPosition)
                
              
        # GRID LINES
        for cell in cells:
            if (cell.x == cell.y) and not (cell.x == 0 or cell.x == CELLWIDTH*9):
                if cell.x % (CELLWIDTH*3) == 0:
                    lineWidth = 3
                else:
                    lineWidth = 1
                pygame.draw.line(SCREEN, BLACK, (0, cell.y), (CELLWIDTH*9, cell.y), lineWidth)
                pygame.draw.line(SCREEN, BLACK, (cell.x, 0), (cell.x, CELLHEIGHT*9), lineWidth)


    


    solvedSudoku = Sudoku(INITIALSUDOKU)
    steps = solvedSudoku.solve()

    SCREEN.fill('WHITE')
    drawGrid(SCREEN, CELLWIDTH, CELLHEIGHT, solvedSudoku.cells)
    pygame.display.update()

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT: 
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONUP:
                for s in steps:
                    SCREEN.fill('WHITE')
                    drawGrid(SCREEN, CELLWIDTH, CELLHEIGHT, s)
                    pygame.display.update()

            pygame.event.pump()

    
main()
