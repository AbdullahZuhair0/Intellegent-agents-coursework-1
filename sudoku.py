class cell:
    def __init__(self, x, y, isClue, value):
        self.x = 0
        self.y = 0
        self.isClue = True if isClue else False
        self.guesses = []
        self.value = value
        self.poppedValues = []

    def addGuess(self, val):
        if val not in self.guesses and val not in self.poppedValues:
            self.guesses.append(val)
            print("added")

    def removeGuess(self):
        val = self.guesses.pop()
        print("val check" + val)
        self.poppedValues.append(val)
        print("val check" + val)
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
# give it a proper condition later.
# error-free :):):) (syntax-wise ehm ehm)
while 1:
    currCell = cells[i][j]
    check = checkRCB(cells, currCell)
    for num in domain:
        if num in check:
            print("nah dude")
        else:
            currCell.addGuess(num)
    # very rough implementation
    currCell.setValue(currCell.removeGuess())
    if currCell.value == ".":
        if j == 0:
            cells[i-1][j+7].setValue( cells[i-1][j+7].removeGuess())
        else:
            cells[i][j-1].setValue( cells[i][j-1].removeGuess())
        # doesn't actually go back sooooo
    if j == 8:
        # if final row then exit
        if i == 8:
            break
        i += 1
        j = 0
    else:
        j += 1
