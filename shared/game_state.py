from shared.map import Map


Position = tuple[int, int]


class GameState:
    players: dict[str, Position]
    grid: list[list[int]]

    def __init__(self, map: Map):
        self.players = {}
        self.map = map

    def validate_move(self, player_id: str, x: int, y: int) -> bool:
        if not self.map.can_move(x, y):
            print("Invalid move, out of bounds")
            return False

        if self.map.is_occupied(x, y):
            print("Invalid move, occupied")
            return False

        self.map.set_player_position(player_id, x, y)
        return True

    def get_spawn_point(self) -> Position:
        return self.map.get_spawn_point()

