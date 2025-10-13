import pygame as pg
import sudoku as s
import pywinstyles as pws


pg.init()

# Color definitions
COLOR_NORMAL = (37, 38, 46)
COLOR_HOVER = (52, 54, 61)
COLOR_CLICK = (80, 80, 80)
COLOR_OUTLINE = (200, 200, 200)
COLOR_TEXT = (255, 255, 255)
current_color = COLOR_NORMAL

# Button properties
button_rect = pg.Rect(101, 412, 201, 50)
button_text = "Auto Solve"
button_font = pg.font.SysFont("rupalro", 28)

#window setup
WIDTH, HEIGHT = 403, 491
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Sudoku Solver")
font = pg.font.SysFont("rupalro", 30)
g_cells,g_row = [],[] 
pws.apply_style(WIN, "acrylic")

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
        pg.draw.line(WIN, color, (x, 20), (x, (rows * cell_size)+22), line_width)
    for y in range(21, (rows * cell_size) + 40, cell_size):
        pg.draw.line(WIN, color, (20, y), ((cols * cell_size)+22, y), line_width)

with open("map.txt") as f:
    for i in range(9):
        for j in range(9):
            char = f.read(1)
            while char == "\n" or char == "":
                char =  f.read(1)
            g_cel = s.cell(i, j, char != ".", char)
            g_row.append(g_cel)
        g_cells.append(g_row)
        g_row = []

gen = s.solver(g_cells, 0, 0)

isSolve = False
count = 0
running = True
while running:
    


    WIN.fill(grid_props["background_color"])
    draw_grid(grid_props)
    draw_grid(box_grid_props)

    # --- Drawing the button ---
    pg.draw.rect(WIN, current_color, button_rect, border_radius=25)
    
    text_surf = button_font.render(button_text, True, COLOR_TEXT)
    text_rect = text_surf.get_rect(center=button_rect.center)
    WIN.blit(text_surf, text_rect)

    # Hover effect
    if button_rect.collidepoint(pg.mouse.get_pos()):
        current_color = COLOR_HOVER
    else:
        current_color = COLOR_NORMAL

    # while isSolve == False:
    
    y = -7
    for l in g_cells:
        x = -4
        y += 40
        for i in l:
            # Use the render() method of the font object to create a Surface containing the rendered text.
            if i.value == ".":
                text_surface = font.render(" ", True, (255, 255, 255)) # Black text
                x += 40
                # Blit the created text_surface onto your main display Surface at the desired coordinates.
                WIN.blit(text_surface, (x, y))
                continue
            text_surface = font.render(i.value, True, (255, 255, 255)) # Black text
            x += 40
            # Blit the created text_surface onto your main display Surface at the desired coordinates.
            WIN.blit(text_surface, (x, y))

    pg.display.flip()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if isSolve == False and event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and button_rect.collidepoint(event.pos):
            isSolve = True
            print("Auto-Solver started...")
            next(gen) 
  
    if isSolve:
        try:
            next(gen)
        except StopIteration:
            isSolve = False
            print("Solver finished: Puzzle solved successfully.")