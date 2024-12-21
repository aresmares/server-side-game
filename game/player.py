from typing import Literal
from game.client import Client
from shared.types import Position

MOVES = Literal["UP", "DOWN", "LEFT", "RIGHT"]

MOVES_LOOKUP = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}


class Player:
    position: Position

    def __init__(self, client: Client):
        self.client = client

    async def start(self) -> None:
        await self.client.start()

    async def move(self, move: MOVES) -> None:
        dx, dy = MOVES_LOOKUP[move]
        x, y = await self.client.get_position()
        await self.client.move_player_req(x + dx, y + dy)

    def ready(self) -> bool:
        return self.client.map.players.get(self.client.name) is not None
