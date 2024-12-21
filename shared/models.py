from pydantic import BaseModel


class RequestPlayerJoin(BaseModel):
    player_id: str


class RequestPlayerMove(BaseModel):
    player_id: str
    x: int
    y: int


############################################
class GameState(BaseModel):
    players: dict[str, tuple[int, int]]
    grid: list[list[int]]


class PlayerJoin(BaseModel):
    player_id: str
    x: int
    y: int
    game_state: GameState


class PlayerMove(BaseModel):
    player_id: str
    x: int
    y: int
