

## here we go again again



initial_sudoku = [9,0,8,3,1,0,0,6,0,
                  0,0,0,0,0,6,0,9,7,
                  0,5,0,0,0,0,8,0,0,
                  2,0,0,0,0,0,1,4,0,
                  0,6,4,0,3,0,9,8,0,
                  0,1,9,0,0,0,0,0,3,
                  0,0,5,0,0,0,0,1,0,
                  7,9,0,4,0,0,0,0,0,
                  0,8,0,0,9,2,4,0,5]


def find_row(sudoku, index):
    # determine the in-row depth of the index
    # subtract this to find the start of the row
    # because all rows are 9 wide, add 9 to the start to find the end
    # parse the list between these two indices
    # return the list of numbers, this is the row
    
    start = index - (index % 9)
    end = start + 9
    row = sudoku[start:end]
    
    return row

def find_col(sudoku, index):
    # determine the in-row depth of the index, this is the start of the column
    # as each row is 9 wide, each entry in the column is 9 apart
    # as each column is 9 long, the last entry is 8*9 = 72 indices away
    # (there will always be 7 of the 81 numbers to the left or right of 'start' and 'end')
    # append numbers together from start to end in steps of 9 indices each
    # return a list of numbers, this is the column
    
    start = index % 9
    end = start + 81
    col = list()
    
    for x in range(start, end, 9):
        col.append(sudoku[x])
    
    return col

def findOptions(sudoku, index):
    # find the row and col, convert them to sets and remove any zeroes
    # produce two sets of the missing numbers for the row and column
    # return the set containing all shared missing numbers

    all_options = set([1,2,3,4,5,6,7,8,9])
    row = find_row(sudoku, index)
    row_options = set(all_options).difference(row)
    col = find_col(sudoku, index)
    col_options = set(all_options).difference(col)

    return row_options & col_options

def print_sudoku(sudoku):
    for i in range(0,9):
        print(find_row(sudoku, 9*i))
    
def checkSolved(sudoku):
    solved = True
    for cell in sudoku:
        if cell == 0:
            solved = False
    return solved


def solveSudoku(sudoku, index, optionsDict = dict()):

    print("CALLED AT ", index)
    if checkSolved(sudoku):
        completedSudoku = sudoku
        print('SOLVED')
        return completedSudoku

    if index > (9*9):
        print("index too high")

    if index == (71):
        print_sudoku(sudoku)

    if sudoku[index] != 0:
        completedSudoku = solveSudoku(sudoku, index+1, optionsDict)
        if completedSudoku != None:
            return completedSudoku
    else:
        options = findOptions(sudoku, index)
        optionsDict.update({index:options})

        while len(options) > 0:
            tryOption = options.pop()
            optionsDict.update({index:options})

            sudoku[index] = tryOption
            completedSudoku = solveSudoku(sudoku, index+1, optionsDict)
            if completedSudoku != None:
                return completedSudoku

        print(optionsDict)
        optionsDict.pop(index)
        sudoku[index] = 0
    return None

sudoku = solveSudoku(initial_sudoku, 0)
print_sudoku(sudoku)
