


from enum import Enum
import signal
from nats.aio.client import Msg
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers
from nats.aio.client import Client as NATS
from nats.js.api import StreamConfig

import asyncio

from pydantic import BaseModel
import pygame


if __name__ == "__main__":

    async def main():
        nats = NATS()
        await nats.connect("nats://localhost:4222")

        server = Server(nats)
        await server.create_streams()

        client = Client(nats, "client1")
        client2 = Client(nats, "client2")

        await server.start()
        await client.start()
        await client2.start()

        await client.move_player_req(1, 1)
        await client2.move_player_req(2, 2)

        shutdown_event = asyncio.Event()
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, shutdown_event.set)

        await shutdown_event.wait()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
