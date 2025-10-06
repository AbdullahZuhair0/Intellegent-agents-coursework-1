class cell:
    def __init__(self, x, y, isClue, value):
        self.x = x
        self.y = y
        self.isClue = True if isClue else False
        self.guesses = []
        self.value = value

    def addGuesses(self, domain, RCB):
        if self.isClue == False:
            self.guesses = []
            for i in domain:
                if i not in RCB:
                    self.guesses.append(i)

    def removeGuess(self):
        if self.guesses == []:
            return "."
        else:
            val = self.guesses.pop()
            return val
        
    def setValue(self, val):
        self.value = val
    def next(self):
        x,y = self.x, self.y
        if self.y == 8:
            x += 1
            y = 0
        else:
            y += 1
        if x > 8:
            return 
        return [x,y]
    def prev(self):
        x,y = self.x,self.y
        if self.y == 0:
            x -= 1
            y = 8
        else:
            y -= 1
        if x < 0:
            return 
        return [x,y]

# 2d array of rows and columns.
def checkRCB(arr, cel):
    rcbValues = []
    box = findBlock(cel)
    rs = 3 * (box // 3) 
    cs = 3 * (box % 3)   

    x,y = int(cel.x), int(cel.y)
# finds all numbers in rows
    for i in range(9):
        if arr[cel.x][i].value != '.':
            rcbValues.append(arr[x][i].value)
# finds all numbers in columns   
    for i in range(9):
        if arr[i][cel.y].value != '.':
            rcbValues.append(arr[i][y].value)
# finds all numbers in block    
    for i in range(3):
        for j in range(3):
            if arr[rs + i][cs + j].value != '.':
                rcbValues.append(arr[rs + i][cs + j].value)    
        
# removes dups and returns all numbers.
    return set(rcbValues)
    
# calculates which box this cell is in.
def findBlock(cel):
    x = int(cel.x)
    y = int(cel.y)
    return 3 * (x // 3) + (y // 3)

cells = []
row = []
domain = ["1","2","3","4","5","6","7","8","9"]

f = open("map.txt")
for i in range(0,9):
    # adds 9 cells per row
    for j in range(0,9):
        char = f.read(1)
        cel = cell(i, j,char != ".", char)
        row.append(cel)
    cells.append(row)
    row = []
f.close()
i,j = 0,0
x,y,z = 0,0,"next"
GuessesNotEmpty = []
"""
GuessesNotEmpty is used in the inner loop to keep trying each cell until their guesses list is empty and is removed from GuessesNotEmpty when you go back to a previous value,
we have added this to prevent cells from infinity trying the same guess.
"""
while i < 9 and j < 9:
    currCell = cells[i][j]
    if currCell.isClue == False:
        currCell.addGuesses(domain,checkRCB(cells, currCell))
        currCell.setValue(currCell.removeGuess())
    
    # if the original cell that didn't have a guess still doesn't have a value
    # could definitly be improved.
    while cells[i][j].value == ".":
        # if it's the first iteration
        if x == 0 and y == 0:
            vals = cells[x][y].prev()
            if vals is None:
                break
            x,y = vals[0], vals[1]
            currCell = cells[x][y]
            GuessesNotEmpty.append(cells[x][y])
        if cells[x][y].isClue == False:
            cells[x][y].setValue(cells[x][y].removeGuess())
        # if isClue
        elif cells[x][y].isClue == True and z == "next":
            vals = cells[x][y].prev()
            if vals is None:
                break
            x,y = vals[0], vals[1]
        else:
            vals = cells[x][y].next()
            if vals is None:
                break
            x,y = vals[0], vals[1]
        # if even the previous cell is empty
        if cells[x][y].value == ".":
            GuessesNotEmpty.pop(GuessesNotEmpty.index(cells[x][y]))
            if x == 0 and y == 0:
                cells[x][y].addGuesses()
                cells[x][y].setValue(cells[x][y].removeGuess())
                y = 1
            else:
                vals = cells[x][y].prev()
                if vals is None:
                    break
                x,y,z = vals[0], vals[1], "next"
        # go to the next cell
        elif cells[x][y].isClue == False:
            vals = cells[x][y].next()
            if vals is None:
                break
            x,y,z = vals[0], vals[1], "prev"
        # whether we go back by 1 cell or we go to the next cell.
        if cells[x][y] not in GuessesNotEmpty and cells[x][y].isClue == False:
            GuessesNotEmpty.append(cells[x][y])
            cells[x][y].addGuesses(domain, checkRCB(cells, cells[x][y]))
    # end of nested while loop    
    GuessesNotEmpty,x,y = [], 0,0
    
        
    if j == 8:    
        i += 1
        j = 0
    else:
        j += 1
for row in cells:
    for col in row:
        print(col.value)
