from abc import ABC
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True, unsafe_hash=True)
class Tile:
    x: int
    y: int


@dataclass(unsafe_hash=True)
class GameObject:
    position: Tile
    ...


class GameState(ABC):
    _state: dict[Tile, list[GameObject]]

    def __init__(self, tiles: list[Tile]) -> None:
        self._state = {tile: [] for tile in tiles}

    def occupy(self, tile: Tile, object: GameObject) -> None:
        if not self._state.get(tile):
            raise Exception("Tile not found")

        if object not in self._state[tile]:
            self._state[tile].append(object)

    def unoccupy(self, object: GameObject) -> None:
        for tile, objects in self._state.items():
            if object in objects:
                self._state[tile].remove(object)
                return

MOVES = Literal["UP", "DOWN", "LEFT", "RIGHT"]


@dataclass        
class Player(GameObject):
    _action_map: dict[]
    
    

grid_map = []
for x in range(10):
    for y in range(10):
        grid_map.append(Tile(x, y))
        
game = GameState(grid_map)
