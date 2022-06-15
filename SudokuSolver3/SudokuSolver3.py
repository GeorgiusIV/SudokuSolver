
## here we go again



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

def find_options(sudoku, index):
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
    
def solve_sudoku(sudoku, index, options_dict, depth):

    # is the sudoku solved?
    if index in range(len(sudoku)):
        if sudoku[index] == 0:
            options = find_options(sudoku, index)
            options_dict.update({index:options})
        
            while len(options_dict[index]) > 0:
        
                options = options_dict.pop(index)
                new_entry = options.pop()
                options_dict.update({index:options})
        
                print("( row:", index//9, ". column:", index%9, ") is:", new_entry)
                sudoku[index] = new_entry
                
                solve_sudoku(sudoku, index + 1, options_dict, depth)
            else:
                print("( row:", index//9, ". column:", index%9, ") can't be filled! Stepping back...")
                sudoku[index] = 0
                options_dict.pop(index)
                # let this recursion end
        else:
            solve_sudoku(sudoku, index + 1, options_dict, depth)

solve_sudoku(initial_sudoku, 0, dict(), 0)
