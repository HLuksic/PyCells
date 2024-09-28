import random
import numpy as np
from scipy.ndimage import convolve
import controls
import config

CELL_GRID = None

MIN_FRIENDS = 3
MAX_FRIENDS = 7
MIN_SPREAD = 2
MAX_ENEMIES = 5


def init(ignore_walls=False):
    global CELL_GRID
    if not ignore_walls:
        CELL_GRID = np.zeros((config.GRID_WIDTH, config.GRID_HEIGHT), dtype=int)
    else:
        CELL_GRID = np.where(CELL_GRID == config.CellType.WALL.value, CELL_GRID, config.CellType.EMPTY.value)


def randomize():
    global CELL_GRID
    CELL_GRID = np.random.choice([-1, 0, 1, 2, 3, 4, 5], (config.GRID_WIDTH, config.GRID_HEIGHT))


def get_random_spawnable_neighbor(x, y, types):
    neighbors = []
    
    # Determine the boundaries
    x_min = max(0, x - 1)
    x_max = min(config.GRID_WIDTH - 1, x + 1)
    y_min = max(0, y - 1)
    y_max = min(config.GRID_HEIGHT - 1, y + 1)
    
    # Collect all neighbors
    for i in range(x_min, x_max + 1):
        for j in range(y_min, y_max + 1):
            if i == x and j == y:
                continue
            type = CELL_GRID[i][j]
            if type in types:
                neighbors.append((i, j, type))
    
    # Return a random neighbor
    if neighbors:
        return random.choice(neighbors)
    
    return None


def update_cells():
    if not controls.UPDATE:
        return
    
    global CELL_GRID
    
    # Count total live neighbors
    neighbor_kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
    live_mask = np.isin(CELL_GRID, config.CellType.LIVE.value)
    total_neighbors = convolve(live_mask.astype(int), neighbor_kernel, mode='constant', cval=0)

    # Count same-type neighbors
    red_mask = (CELL_GRID == config.CellType.RED.value)
    green_mask = (CELL_GRID == config.CellType.GREEN.value)
    blue_mask = (CELL_GRID == config.CellType.BLUE.value)
    yellow_mask = (CELL_GRID == config.CellType.YELLOW.value)

    same_neighbors = (
        red_mask * convolve(red_mask.astype(int), neighbor_kernel, mode='constant', cval=0) +
        green_mask * convolve(green_mask.astype(int), neighbor_kernel, mode='constant', cval=0) +
        blue_mask * convolve(blue_mask.astype(int), neighbor_kernel, mode='constant', cval=0) +
        yellow_mask * convolve(yellow_mask.astype(int), neighbor_kernel, mode='constant', cval=0)
    )
    
    # Death rules
    population_mask = (same_neighbors < MIN_FRIENDS) | (same_neighbors > MAX_FRIENDS)
    too_many_enemies_mask = (total_neighbors - same_neighbors) > MAX_ENEMIES
    die_mask = live_mask & (population_mask | too_many_enemies_mask)
    
    # Spread rules
    spread_mask = same_neighbors >= MIN_SPREAD
    
    if controls.STATIC:
        empty_nearby = convolve((CELL_GRID == config.CellType.EMPTY.value).astype(int), neighbor_kernel, mode='constant', cval=0)
        spread_cells = spread_mask & (empty_nearby > 0)
    else:
        empty_food_mask = (CELL_GRID == config.CellType.EMPTY.value) | (CELL_GRID == config.CellType.FOOD.value)
        empty_food_nearby = convolve(empty_food_mask.astype(int), neighbor_kernel, mode='constant', cval=0)
        spread_cells = spread_mask & (empty_food_nearby > 0)
    
    new_grid = CELL_GRID.copy()

    # Kill cells
    new_grid[die_mask] = config.CellType.FOOD.value
    
    # Shuffle types to avoid bias
    live_types = list(config.CellType.LIVE.value)
    random.shuffle(live_types)
    
    # Spreading logic
    for live_type in live_types:
        spread_mask = spread_cells & (CELL_GRID == live_type)
        spread_positions = np.argwhere(spread_mask)
        
        for x, y in spread_positions:
            # Static mode: don't spawn on food cells
            n = get_random_spawnable_neighbor(x, y, [config.CellType.EMPTY.value]) if controls.STATIC else get_random_spawnable_neighbor(x, y, [config.CellType.EMPTY.value, config.CellType.FOOD.value])
            if n is not None:
                new_grid[n[0], n[1]] = live_type # Spawn a new cell
                # Remove a food cell if the new cell wasn't spawned over one
                if not controls.STATIC and n[2] == config.CellType.EMPTY.value: # Static mode: don't consume food
                    n = get_random_spawnable_neighbor(x, y, [config.CellType.FOOD.value])
                    if n is not None:
                       new_grid[n[0]][n[1]] = config.CellType.EMPTY.value # Remove a food cell
                continue
    
    CELL_GRID = new_grid


def spawn_cells(x, y, cell_type):
    # Spawn cells in cluster
    brush_size = 2
    for i in range(x - brush_size, x + brush_size + 1):
        for j in range(y - brush_size, y + brush_size + 1):
            if i >= 0 and i < config.GRID_WIDTH and j >= 0 and j < config.GRID_HEIGHT:
                CELL_GRID[i][j] = cell_type