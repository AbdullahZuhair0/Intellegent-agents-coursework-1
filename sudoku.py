import time
global domain
domain = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
class cell:
    def __init__(self, x, y, isClue, value):
        self.x = x
        self.y = y
        self.isClue = isClue
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
            val = self.guesses.pop(0)
            return val

    def setValue(self, val):
        self.value = val
        return self.value

    def next(self):
        x,y = self.x, self.y
        if self.y == 8:
            x += 1
            y = 0
        else:
            y += 1
        if x > 8:
            return None  
        return [x, y]

    def prev(self):
        x,y = self.x, self.y
        if y == 0:
            x -= 1
            y = 8
        else:
            y -= 1
        if x < 0:
            return None
        return [x, y]

# 2d array of rows and columns.
def checkRCB(arr, cel):
    rcbValues = []
    box = findBlock(cel)
    rs = 3 * (box // 3)
    cs = 3 * (box % 3)

    x, y = cel.x,cel.y
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

def findBlock(cel):
    # calculates which box this cell is in.
    return 3 * (cel.x // 3) + (cel.y // 3)

def solver(cells, x, y):
    # if the current index is out of bounds
    if x is None:
        return True  

    cur = cells[x][y]
    if cur.isClue:
        vals = cur.next()
        # if the next index is out of bounds
        if vals is None:
            return True
        return (yield from solver(cells, vals[0], vals[1]))

    cur.addGuesses(domain, checkRCB(cells, cur)) 
    while cur.guesses:
        time.sleep(0.015) # 15 ms
        cur.setValue(cur.removeGuess()) #remove guess applies next
        yield (x, y, cur.value)

        vals = cur.next()

        if vals is None:
            return True
        if (yield from solver(cells, vals[0], vals[1])):
            return True
        
        cur.setValue(".")
        yield (x, y, ".")

    # if the backtracking loop fails it is unsolveable 
    return False

def main():
    cells,row = [],[]

    with open("map.txt") as f:
        for i in range(9):
            for j in range(9):
                char = f.read(1)
                while char == "\n" or char == "":
                    char =  f.read(1)
                cel = cell(i, j, char != ".", char)
                row.append(cel)
            cells.append(row)
            row = []
    solver(cells, 0, 0)
# uncomment this if you wanna check solver output.
    for row in cells:
        for col in row:
            print(col.value)
        print()
if __name__ == "__main__":
    main()
