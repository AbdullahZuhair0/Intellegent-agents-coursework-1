class cell:
    def __init__(self, x, y, isClue, value):
        self.x = 0
        self.y = 0
        self.isClue = True if isClue else False
        self.guesses = []
        self.value = ""

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
            rcbValues.append(int(arr[x][i]))
# finds all numbers in columns   
    for i in range(0,9):
        if arr[i][cel.y] != '.':
            rcbValues.append(int(arr[i][y]))
# finds all numbers in block    
    for i in range(1,10):
        if arr[rs][cs] != '.':
            rcbValues.append(int(arr[rs][cs]))    
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

