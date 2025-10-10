import pygame
import sudoku

pygame.init()

#window setup
WIDTH, HEIGHT = 360, 360
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid Example")

# note for adham you can call all functions by sudoku.funcName and to run the solver just type sudoku.main()
# can't really do more since you haven't pushed yet.
#grid properties
grid_props = {
    "rows": 9,
    "cols": 9,
    "cell_size": 40,
    "line_color": (180, 180, 180),
    "line_width": 2,
    "background_color": (255, 255, 255)
}

#main method to draw the grid
def draw_grid(props):
    rows, cols = props["rows"], props["cols"]
    cell_size = props["cell_size"]
    color = props["line_color"]
    line_width = props["line_width"]

    for x in range(0, cols * cell_size, cell_size):
        pygame.draw.line(WIN, color, (x, 0), (x, rows * cell_size), line_width)
    for y in range(0, rows * cell_size, cell_size):
        pygame.draw.line(WIN, color, (0, y), (cols * cell_size, y), line_width)

running = True
while running:
    WIN.fill(grid_props["background_color"])
    draw_grid(grid_props)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

