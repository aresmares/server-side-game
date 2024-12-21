from contextlib import contextmanager
from typing import Generator, Tuple
import pygame
import sys

# Constants
GRID_SIZE = 10
CELL_SIZE = 50
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE


def run_game() -> Generator[Tuple[pygame.Surface, int, int, int, int], None, None]:
    # Initialize pygame
    pygame.init()
    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Grid Game")

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            yield screen, GRID_SIZE, CELL_SIZE, WIDTH, HEIGHT

        # Update the display
        pygame.display.flip()

    # Quit pygame
    pygame.quit()
    sys.exit()
