from nats.aio.client import Client as NATS
from nats.aio.msg import Msg
from shared.map import Map
from shared.models import RequestPlayerJoin, RequestPlayerMove, PlayerJoin, PlayerMove


class Client:
    def __init__(self, nats: NATS, name: str):
        self.nats = nats
        self.name = name
        self._js = nats.jetstream()
        self.map = Map()

    async def start(self):
        await self._js.subscribe(
            "client.player_move", durable=f"cons-{self.name}", cb=self._on_player_move
        )
        await self._js.subscribe(
            "client.player_join", durable=f"dur-{self.name}", cb=self._on_player_join
        )
        await self.join_player_req()

    async def join_player_req(self):
        await self._js.publish(
            "request.player_join",
            RequestPlayerJoin(player_id=self.name).model_dump_json().encode(),
        )

    async def _on_player_join(self, msg: Msg):
        req = PlayerJoin.model_validate_json(msg.data)
        print(
            f"[{self.name}]: {req.player_id} joined the game. Spawning at {req.x}, {req.y}"
        )
        self.map.set_player_position(req.player_id, req.x, req.y)
        self.map.grid = req.game_state.grid
        self.map.players = req.game_state.players

    async def move_player_req(self, x: int, y: int):
        await self._js.publish(
            "request.player_move",
            RequestPlayerMove(player_id=self.name, x=x, y=y).model_dump_json().encode(),
        )

    async def _on_player_move(self, msg: Msg):
        req = PlayerMove.model_validate_json(msg.data)
        print(f"[{self.name}]: {req.player_id} moved to {req.x}, {req.y}")
        self.map.set_player_position(req.player_id, req.x, req.y)

    async def get_position(self):
        return self.map.players[self.name]

    async def do_action_req(self, action, params) -> None: ...

    async def _on_action(self, msg) -> None: ...
