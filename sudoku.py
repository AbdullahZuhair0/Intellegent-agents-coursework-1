class cell:
    x = 0
    y = 0
    guesses = []
    value = ""

# 2d array of rows and columns.
def checkRCB(arr, cel):
    rcbValues = []
    box = findBlock(cel)
    rs = 0 if box // 3 == 0 else rs = (3 *(box // 3))
    cs = (3 * (box % 3)) - 3
# finds all numbers in rows
    for i in range(0,9):
        if arr[cel.x][i] != '.':
            rcbValues.append(arr[cel.x][i])
# finds all numbers in columns   
    for i in range(0,9):
        if arr[i][cel.y] != '.':
            rcbValues.append(arr[cel.x][i])
# finds all numbers in block    
    for i in range(1,10):
        if arr[rs][cs] != '.':
            rcbValues.append(arr[rs][cs])    
        if i % 3 == 0:
            rs += 1
            cs -= 2
        else:
            cs += 1
# removes dups and returns all numbers.
    return set(rcbValues)
    
# calculates which box this cell is in.
def findBlock(cel):
    x = cel.x
    y = cel.y
    cnt = 1
    cnt2 = 1

    while x > 3:
        x -= 3
        cnt += 1
    
    while y > 3:
        y -= 3
        cnt2 += 1
# returns block number
    return cnt * cnt2

