import pygame
import config
import grid

CHOSEN_TYPE = 1
UPDATE = False
DRAW_GRID = False
STATIC = False


def handle_input(event):
    global CHOSEN_TYPE, UPDATE, DRAW_GRID, STATIC
    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            UPDATE = not UPDATE
        elif event.key == pygame.K_g:
            DRAW_GRID = not DRAW_GRID
        elif event.key == pygame.K_s:
            STATIC = not STATIC
        elif event.key == pygame.K_r:
            grid.randomize()
            UPDATE = False
        elif event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_SHIFT:
            grid.init(ignore_walls=True)
        elif event.key == pygame.K_c:
            grid.init()
        elif event.key == pygame.K_d:
            CHOSEN_TYPE += 1
            if CHOSEN_TYPE > 5:
                CHOSEN_TYPE = -1
        elif event.key == pygame.K_a:
            CHOSEN_TYPE -= 1
            if CHOSEN_TYPE < -1:
                CHOSEN_TYPE = 5
        elif event.key == pygame.K_1:
            grid.MIN_FRIENDS += 1
            if grid.MIN_FRIENDS > 3:
                grid.MIN_FRIENDS = 0
            print("min friends:", grid.MIN_FRIENDS, "max friends:", grid.MAX_FRIENDS, "min spread:", grid.MIN_SPREAD, "max enemies:", grid.MAX_ENEMIES)
        elif event.key == pygame.K_2:
            grid.MAX_FRIENDS += 1
            if grid.MAX_FRIENDS > 8:
                grid.MAX_FRIENDS = 3
            print("min friends:", grid.MIN_FRIENDS, "max friends:", grid.MAX_FRIENDS, "min spread:", grid.MIN_SPREAD, "max enemies:", grid.MAX_ENEMIES)
        elif event.key == pygame.K_3:
            grid.MIN_SPREAD += 1
            if grid.MIN_SPREAD > 8:
                grid.MIN_SPREAD = 1
            print("min friends:", grid.MIN_FRIENDS, "max friends:", grid.MAX_FRIENDS, "min spread:", grid.MIN_SPREAD, "max enemies:", grid.MAX_ENEMIES)
        elif event.key == pygame.K_4:
            grid.MAX_ENEMIES += 1
            if grid.MAX_ENEMIES > 8:
                grid.MAX_ENEMIES = 2
            print("min friends:", grid.MIN_FRIENDS, "max friends:", grid.MAX_FRIENDS, "min spread:", grid.MIN_SPREAD, "max enemies:", grid.MAX_ENEMIES)

    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        x = pos[0] // config.CELL_SIZE
        y = pos[1] // config.CELL_SIZE
        grid.spawn_cells(x, y, CHOSEN_TYPE)