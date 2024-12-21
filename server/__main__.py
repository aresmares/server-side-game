import asyncio
import signal
from shared.models import (
    PlayerJoin,
    PlayerMove,
    RequestPlayerJoin,
    RequestPlayerMove,
    GameState as GameStateModel,
)
from shared.game_state import GameState, Map

from nats.aio.client import Client as NATS
from nats.js.api import StreamConfig
from nats.aio.msg import Msg


class Server:
    def __init__(self, nats: NATS):
        self.nats = nats
        self._js = nats.jetstream()

        self.game_state = GameState(Map())

    async def create_streams(self):
        await self._js.add_stream(
            config=StreamConfig(
                name="server",
                subjects=["request.>"],
            )
        )
        await self._js.add_stream(
            config=StreamConfig(
                name="clients",
                subjects=["client.>"],
            )
        )

    async def start(self):
        await self._js.subscribe(
            "request.player_join", durable="server1", cb=self.on_player_join_req
        )
        await self._js.subscribe(
            "request.player_move", durable="server2", cb=self.on_player_move_req
        )

    async def on_player_join_req(self, msg: Msg) -> None:
        req = RequestPlayerJoin.model_validate_json(msg.data)

        x, y = self.game_state.get_spawn_point()
        self.game_state.map.set_player_position(req.player_id, x, y)
        print(self.game_state.map.players)
        await self._js.publish(
            "client.player_join",
            PlayerJoin(
                player_id=req.player_id,
                x=x,
                y=y,
                game_state=GameStateModel(
                    players=self.game_state.map.players,
                    grid=self.game_state.map.grid,
                ),
            )
            .model_dump_json()
            .encode(),
        )
        print(f"SERVER: Player {req.player_id} joined the game.")

    async def on_player_move_req(self, msg: Msg):
        req = RequestPlayerMove.model_validate_json(msg.data)
        print(f"SERVER: Player {req.player_id} move request.")
        if not self.game_state.validate_move(req.player_id, req.x, req.y):
            print(f"SERVER: Player {req.player_id} move request rejected.")
            return

        self.game_state.map.set_player_position(req.player_id, req.x, req.y)

        await self.nats.publish(
            "client.player_move",
            PlayerMove(player_id=req.player_id, x=req.x, y=req.y)
            .model_dump_json()
            .encode(),
        )


async def main():
    nats = NATS()
    await nats.connect("nats://localhost:4222")

    server = Server(nats)
    await server.create_streams()

    await server.start()

    shutdown_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, shutdown_event.set)

    await shutdown_event.wait()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
