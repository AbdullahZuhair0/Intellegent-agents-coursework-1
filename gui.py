import pygame as pg
import sudoku as s
import pywinstyles as pws

# --- Globals ---
g_cells,g_row = [],[]
gen = None
isSolve = False
isSolved = False
status = ""
isReset = True
delay = 0.0
speed = 5
screen = None
delay_active = 0
isMissing = False
isSolvable = True
isExtra = False
start_time = 0 # ADDED: To store the start time of the solver


class Button:
    def __init__(self, x, y, width, height, text, font_size, idle_color=(37, 38, 46), action=None):
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.font = pg.font.SysFont("arialblack", font_size)
        self.color_idle = idle_color    # Default - Shark
        self.color_hover = (52, 54, 61) # Tuna
        self.color_click = (80, 80, 80) # Emperor
        self.current_color = self.color_idle

    def draw(self, screen):
        pg.draw.rect(screen, self.current_color, self.rect, border_radius=25)
        text_surface = self.font.render(self.text, True, (255, 255, 255)) # White text
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pg.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.current_color = self.color_hover
            else:
                self.current_color = self.color_idle
        elif event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.current_color = self.color_click
        elif event.type == pg.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                self.current_color = self.color_hover
                if self.action:
                    self.action()

def Solve():
    global isSolve, gen, delay_active, isMissing, start_time
    if isMissing:
        print("Missing digits from map.txt")
        return
    if isSolved == True:
        print("Already Solved!")
    elif isSolve == False:
        start_time = pg.time.get_ticks() # ADDED: Record the start time in milliseconds
        gen = s.solver(g_cells, 0, 0, delay)
        delay_active = delay
        isSolve = True
        print("Auto-Solver started...")
    else:
        print("Auto-Solver is already running...")

def Reset():
    global g_row, g_cells, gen, isSolve, isSolved, isMissing, isSolvable, isExtra
    isSolve, isSolved, g_cells, g_row = False, False, [], []
    isSolvable, isMissing, isExtra = True, False, False
    with open("map.txt") as f:
        # for each character in the file if it is in the domain or a blank then add it to the chars
        chars = ''.join(c for c in f.read() if c in "0123456789.")
        # if there are missing chars.
        if len(chars) < 81:
            isMissing = True
        elif len(chars) > 81:
            isExtra = True
        else:
            isMissing = False
            for i in range(9):
                g_row = []
                for j in range(9):
                    # since for each row there are 9 values.
                    char = chars[i*9 + j]
                    g_cel = s.cell(i, j, char != ".", char)
                    g_row.append(g_cel)
                g_cells.append(g_row)
            
def increase_speed():
    global delay, speed
    delay = max(0.0, delay - 0.0125) 
    if speed == 5:
        print("Fastest speed reached - delay: " + str(delay))
    else:
        print("Speed increased! delay: " + str(delay))
        speed += 1

def decrease_speed():
    global delay, speed
    delay = min(0.050, delay + 0.0125)
    if speed == 1:
        print("Slowest speed reached - delay: " + str(delay))
    else:
        print("Speed decreased! delay: " + str(delay))
        speed -= 1

#grid properties
grid_props = {
    "rows": 9,
    "cols": 9,
    "cell_size": 40,
    "line_color": (107, 107, 107),
    "line_width": 2,
    "background_color": (23, 24, 31)
}

box_grid_props = {
    "rows": 3,
    "cols": 3,
    "cell_size": 120,
    "line_color": (133, 137, 133),
    "line_width": 3,
    "background_color": (23, 24, 31)
}

#main method to draw the grid
def draw_grid(props):
    rows, cols = props["rows"], props["cols"]
    cell_size = props["cell_size"]
    color = props["line_color"]
    line_width = props["line_width"]

    for x in range(21, (cols * cell_size) + 40, cell_size):
        pg.draw.line(screen, color, (x, 20), (x, (rows * cell_size)+22), line_width)
    for y in range(21, (rows * cell_size) + 40, cell_size):
        pg.draw.line(screen, color, (20, y), ((cols * cell_size)+22, y), line_width)

if __name__ == '__main__':
    pg.init()

    #screen window setup
    screen_width, screen_height = 403, 511
    screen = pg.display.set_mode((screen_width, screen_height))
    pg.display.set_caption("Sudoku Solver")

    font  = pg.font.SysFont("arialblack", 20)
    font1 = pg.font.SysFont("arialblack", 13)
    font2 = pg.font.SysFont("Arial Bold Italic", 11)
    try:
        pws.apply_style(screen, "acrylic")
    except Exception:
        pass

    # Create button instances
    solve_button    = Button(60, 403, 283, 45, "Auto Solve", 20, action=Solve)
    reset_button    = Button(146,  454, 110,  39, "Reset", 14, action=Reset)
    plus_button     = Button(348,  403, 35,  45, "+", 30, (23, 24, 31), action=increase_speed)
    minus_button    = Button(20,  403, 35,  45, "-", 30, (23, 24, 31), action=decrease_speed)
 
    Reset()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            solve_button.handle_event(event)
            reset_button.handle_event(event)
            plus_button.handle_event(event)
            minus_button.handle_event(event)


        screen.fill(grid_props["background_color"])
        draw_grid(grid_props)
        draw_grid(box_grid_props)

        # Write the numbers in the data array
        y = -14
        for l in g_cells:
            x = -4
            y += 40
            for i in l:
                x += 40
                if i.value == ".":
                    # Use the render() method of the font object to create a Surface containing the rendered text.
                    text_surface = font.render(" ", True, (255, 255, 255)) # Black text
                else:
                    text_surface = font.render(i.value, True, (255, 255, 255)) # Black text
                # Blit the created text_surface onto your main display Surface at the desired coordinates.
                screen.blit(text_surface, (x, y))

        screen.blit(font1.render("Speed:", True, (255, 255, 255)),(300, 458))
        screen.blit(font1.render("" + str(speed), True, (255, 255, 255)),(320, 473))

        # Buttons
        reset_button.draw(screen)
        solve_button.draw(screen)
        plus_button.draw(screen)
        minus_button.draw(screen)


        if isSolve:
            if delay != delay_active:
                screen.blit(font2.render("(Reset to apply changes)", True, (255, 255, 255)),(284, 493))

            try:
                next(gen)
            except StopIteration as si:
                s.backtrackcnt, s.stepcnt, s.recursivecnt = 0,0,-1
                if si.value == False:
                    isSolvable = False
                    print("Map is incorrect or unsolvable")
                elif si.value == True:
                    end_time = pg.time.get_ticks()
                    elapsed_time = (end_time - start_time) / 1000.0 # Convert milliseconds to seconds
                    print(f"Solver finished: Puzzle solved successfully in {elapsed_time:.4f} seconds.")
                    isSolve, isSolved = False, True

        
        screen.blit(font1.render("Status:" , True, (255, 255, 255)),(30, 458))
        if not isSolvable:
            screen.blit(font1.render("Unsolvable!" , True, (255, 255, 255)),(30, 473))
        elif isExtra:
            screen.blit(font1.render("Extra digits!" , True, (255, 255, 255)),(30, 473))
        elif isMissing:
            screen.blit(font1.render("Missing digits!" , True, (255, 255, 255)),(30, 473))
        elif isSolved:
            screen.blit(font1.render("Solved!" , True, (255, 255, 255)),(30, 473))
        elif isSolve:
            screen.blit(font1.render("Solving..." , True, (255, 255, 255)),(30, 473))
        else:
            screen.blit(font1.render("Not Solved" , True, (255, 255, 255)),(30, 473))
        pg.display.flip()

                
pg.quit()
