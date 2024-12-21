from dataclasses import dataclass
from typing import Optional
import pygame
from abc import ABC
from shared.types import Position

BLUE = (0, 0, 255)




class Map:
    spawn_points: list[Position]

    def __init__(self, size: int = 10):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.spawn_points = [(0, 0), (9, 9), (0, 9), (9, 0)]
        self.players: dict[str, Position] = {}

    def can_move(self, x: int, y: int) -> bool:
        return 0 <= x < self.size and 0 <= y < self.size

    def get_spawn_point(self) -> Position:
        return self.spawn_points.pop()

    def occupy(self, x: int, y: int):
        self.grid[x][y] = 1

    def free(self, x: int, y: int):
        self.grid[x][y] = 0

    def set_player_position(self, player_id: str, x: int, y: int) -> None:
        if player_id in self.players:
            self.free(*self.players[player_id])
        self.occupy(x, y)
        self.players[player_id] = (x, y)

    def is_occupied(self, x: int, y: int) -> bool:
        return (x, y) in self.players.values()

    def draw(self, screen: pygame.Surface, cell_size, width, height) -> None:
        screen.fill((255, 255, 255))

        # Draw the grid
        for x in range(0, width, cell_size):
            for y in range(0, height, cell_size):
                rect = pygame.Rect(x, y, cell_size, cell_size)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)

        # Draw the player (blue dot) in the specified cell
        for player_id, (player_grid_x, player_grid_y) in self.players.items():
            player_pos = (
                player_grid_x * cell_size + cell_size // 2,
                player_grid_y * cell_size + cell_size // 2,
            )
            pygame.draw.circle(screen, BLUE, player_pos, cell_size // 2)
