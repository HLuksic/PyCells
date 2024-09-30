import pygame
import numpy as np
import config
import grid
import controls


def draw_cells(win):
    colors = {
        config.CellType.WALL.value: (100, 100, 100),
        config.CellType.EMPTY.value: (0, 0, 0),
        config.CellType.RED.value: (196, 47, 47),
        config.CellType.GREEN.value: (54, 181, 73),
        config.CellType.BLUE.value: (52, 155, 235),
        config.CellType.YELLOW.value: (201, 186, 48),
        config.CellType.FOOD.value: (90, 60, 40)
    }
    
    for i in range(config.GRID_HEIGHT):
        for j in range(config.GRID_WIDTH):
            cell_type = grid.CELL_GRID[i][j]
            
            if cell_type in colors:
                pygame.draw.rect(win, colors[cell_type], (i*config.CELL_SIZE, j*config.CELL_SIZE, config.CELL_SIZE, config.CELL_SIZE))


def draw_grid(win):
    for i in range(0, config.GRID_LINES + 1, config.CELL_SIZE):
        pygame.draw.line(win, (50, 50, 50), (i, 0), (i, config.GRID_LINES))
        pygame.draw.line(win, (50, 50, 50), (0, i), (config.GRID_LINES, i))


def render_type(win, r, g, b, text="   "):
    font = pygame.font.Font(None, 36)
    text = font.render(text, True, (255, 255, 255), (r, g, b))
    win.blit(text, (100, config.SCREEN_WIDTH + 20))


def draw_text(win, clock):
    font = pygame.font.Font(None, 36)
    text = font.render("Brush: ", True, (255, 255, 255))
    win.blit(text, (10, config.SCREEN_WIDTH + 20))
    
    if controls.CHOSEN_TYPE == -1:
        render_type(win, 100, 100, 100, "Wall")
    elif controls.CHOSEN_TYPE == 0:
        render_type(win, 0, 0, 0, "Erase")
    elif controls.CHOSEN_TYPE == 1:
        render_type(win, 196, 47, 47)
    elif controls.CHOSEN_TYPE == 2:
        render_type(win, 54, 181, 73)
    elif controls.CHOSEN_TYPE == 3:
        render_type(win, 52, 155, 235)
    elif controls.CHOSEN_TYPE == 4:
        render_type(win, 201, 186, 48)
    elif controls.CHOSEN_TYPE == 5:
        render_type(win, 90, 60, 40)
        
    if not controls.UPDATE:
        text = font.render("Paused", True, (255, 255, 255))
        win.blit(text, (10, config.SCREEN_WIDTH + 60))
        
    if controls.SHOW_FPS:
        font = pygame.font.Font(None, 36)
        text = font.render(str(int(clock.get_fps())) + " FPS", True, (255, 255, 255))
        win.blit(text, (config.SCREEN_WIDTH - 100, config.SCREEN_WIDTH + 20))
        
    if controls.STATIC:
        text = font.render("Static Mode", True, (255, 255, 255))
        win.blit(text, (config.SCREEN_WIDTH - 160, config.SCREEN_WIDTH + 60))
    

def draw_statistics(win):
    # Count number of each type of cell
    red = np.count_nonzero(grid.CELL_GRID == config.CellType.RED.value)
    green = np.count_nonzero(grid.CELL_GRID == config.CellType.GREEN.value)
    blue = np.count_nonzero(grid.CELL_GRID == config.CellType.BLUE.value)
    yellow = np.count_nonzero(grid.CELL_GRID == config.CellType.YELLOW.value)
    
    # Calculate relative percentages
    total = red + green + blue + yellow
    if total == 0:
        return
    
    red_percent = red / total * 100
    green_percent = green / total * 100
    blue_percent = blue / total * 100
    yellow_percent = yellow / total * 100
    
    # Draw bars
    pygame.draw.rect(win, (196, 47, 47), (230, config.SCREEN_WIDTH + 15, red_percent, 10))
    pygame.draw.rect(win, (54, 181, 73), (230, config.SCREEN_WIDTH + 35, green_percent, 10))
    pygame.draw.rect(win, (52, 155, 235), (230, config.SCREEN_WIDTH + 55, blue_percent, 10))
    pygame.draw.rect(win, (201, 186, 48), (230, config.SCREEN_WIDTH + 75, yellow_percent, 10))
    


