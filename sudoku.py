class cell:
    x = 0
    y = 0
    guesses = []
    value = ""

# 2d array of rows and columns.
def checkRCB(arr, cel):
    for i in range(0,9):
        arr[cel.x]
# calculates which box this cell is in.
def findBox(cel):
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
    return cnt * cnt2