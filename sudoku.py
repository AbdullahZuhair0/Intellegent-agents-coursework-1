class cell:
    def __init__(self, x, y, isClue, value):
        self.x = 0
        self.y = 0
        self.isClue = True if isClue else False
        self.guesses = []
        self.value = value

    def addGuesses(self, domain, RCB):
        for i in domain:
            if i not in RCB:
                self.guesses.append(i)

    def removeGuess(self):
        if(self.guesses == []):
            return "."
        else:
            val = self.guesses.pop()
            return val

    def setValue(self, val):
        self.value = val

# 2d array of rows and columns.
def checkRCB(arr, cel):
    rcbValues = []
    box = findBlock(cel)
    cs = 0 if box % 3 == 0 else (3 *(box % 3)) - 3
    rs = (3 *(box // 3))
    x,y = int(cel.x), int(cel.y)
# finds all numbers in rows
    for i in range(0,9):
        if arr[cel.x][i] != '.':
            rcbValues.append(arr[x][i].value)
# finds all numbers in columns   
    for i in range(0,9):
        if arr[i][cel.y] != '.':
            rcbValues.append(arr[i][y].value)
# finds all numbers in block    
    for i in range(1,10):
        if arr[rs][cs] != '.':
            rcbValues.append(arr[rs][cs].value)    
        if i % 3 == 0:
            rs += 1
            cs -= 2
        else:
            cs += 1
# removes dups and returns all numbers.
    return set(rcbValues)
    
# calculates which box this cell is in.
def findBlock(cel):
    x = int(cel.x)
    y = int(cel.y)
    xcnt = 1
    ycnt = -2

    while x > 2:
        xcnt += 1
        x -= 3
    
    while y > 2:
        ycnt += 1
        y -= 3

# returns block number
    return (3 * xcnt) + ycnt

cells = []
row = []
domain = ["1","2","3","4","5","6","7","8","9"]
# adds cells (is wrong rn cuz duh)
for i in range(0,9):
    # adds 9 cells per row
    for j in range(0,9):
        cel = cell(i, j, True, "2")
        row.append(cel)
    cells.append(row)

i,j = 0,0
x,y = 0,0
GuessesNotEmpty = []
"""
GuessesNotEmpty is used in the inner loop to keep trying each cell until their guesses list is empty and is removed from GuessesNotEmpty when you go back to a previous value,
we have added this to prevent cells from infinity trying the same guess.
"""
# error-free :):):) (syntax-wise ehm ehm)
# while it''s not the last cell and while cell is not empty (last condition is for last cell).
while i != 8 and j != 8 and currCell.value != "." :
    currCell = cells[i][j]
    currCell.addGuesses(domain,checkRCB(cells, currCell))
    currCell.setValue(currCell.removeGuess)
    
    # if the original cell that didn't have a guess still doesn't have a value
    # could definitly be improved.
    while cells[i][j] == ".":
        # if it's the first iteration
        if x == 0 and y == 0:
            x = i-1, y = j-1
            currCell = cells[x][y]
            currCell.setValue(currCell.removeGuess())
        # if even the previous cell is empty
        if currCell.value == ".":
            GuessesNotEmpty.pop(GuessesNotEmpty.index(currCell))
            if y == 0:
                y = 8
                x -= 1
            else:
                y -= 1
            
        # go to the next cell
        elif y == 8:
            y = 0
            x += 1
        else:
            y += 1
        # whether we go back by 1 cell or we go to the next cell.
        currCell = cells[x][y]
        if currCell in GuessesNotEmpty:
            currCell.setValue(currCell.removeGuess)
        else:
            GuessesNotEmpty.append(currCell)
            currCell.addGuesses(domain, checkRCB(cells, currCell))
            currCell.setValue(currCell.removeGuess)
    # end of nested while loop    

        
    if j == 8:
        # if final row then exit
        if i != 8:
           i += 1
           j = 0
    else:
        j += 1
