import pygame
import config
import grid
import controls
import ui


def main():
    pygame.init()
    win = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Cells")
    grid.init()
    grid.randomize()
    
    run = True
    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            controls.handle_input(event)

        win.fill((0, 0, 0))
        ui.draw_cells(win)
        ui.draw_text(win)
        ui.draw_statistics(win)
        if controls.DRAW_GRID:
            ui.draw_grid(win)   
        grid.update_cells()
        pygame.display.update()
        #print(clock.get_fps())

    pygame.quit()
    
if __name__ == "__main__":
    print("Controls:")
    print("Space - Start/Stop")
    print("G - Toggle Grid")
    print("S - Toggle Static Mode (Spawning on and Consuming Food)")
    print("R - Randomize")
    print("C - Clear")
    print("Shift + C - Clear All But Walls")
    print("A/D - Change Brush")
    print("1/2/3/4 - Change Cell Rules")
    print("Left Click - Draw")
    main()