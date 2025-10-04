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
    rs = 3 * ((box - 1) // 3) 
    cs = 3 * ((box - 1) % 3)   

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
# adds cells (is wrong rn cuz duh)
f = open("map.txt")
for i in range(0,9):
    # adds 9 cells per row
    for j in range(0,9):
        char = f.read(1)
        cel = cell(i, j, True if char != "." else False, char)
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
    currCell.addGuesses(domain,checkRCB(cells, currCell))
    currCell.setValue(currCell.removeGuess())
    
    # if the original cell that didn't have a guess still doesn't have a value
    # could definitly be improved.
    while cells[i][j].value == ".":
        # if it's the first iteration
        if x == 0 and y == 0:
            x,y = i-1, j-1
            currCell = cells[x][y]
            GuessesNotEmpty.append(currCell)
        if currCell.isClue == False:
            currCell.setValue(currCell.removeGuess())
        elif currCell.isClue == True and z == "next":
            vals = currCell.prev()
            x,y = vals[0], vals[1]
        else:
            vals = currCell.next()
            x,y = vals[0], vals[1]
        # if even the previous cell is empty
        if currCell.value == ".":
            GuessesNotEmpty.pop(GuessesNotEmpty.index(currCell))
            vals = currCell.prev()
            x,y,z = vals[0], vals[1], "next"
        # go to the next cell
        elif currCell.isClue == False:
            vals = currCell.next()
            x,y,z = vals[0], vals[1], "prev"
        # whether we go back by 1 cell or we go to the next cell.
        currCell = cells[x][y]
        if currCell not in GuessesNotEmpty and currCell.isClue == False:
            GuessesNotEmpty.append(currCell)
            currCell.addGuesses(domain, checkRCB(cells, currCell))
    # end of nested while loop    
    GuessesNotEmpty,x,y = [], 0,0
    
        
    if j == 8:
        # if final row then exit
        if i != 8:
           i += 1
           j = 0
    else:
        j += 1
for row in cells:
    for col in row:
        print(col.value)
