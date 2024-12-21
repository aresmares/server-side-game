import os

import pygame
from game.client import Client
from game.player import Player
from nats.aio.client import Client as NATS
import asyncio


# Constants
GRID_SIZE = 10
CELL_SIZE = 50
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE

client_name = os.getenv("CLIENT_NAME", "client")

nats = NATS()
client = Client(nats=nats, name=client_name)
player = Player(client=client)


async def main():
    await nats.connect()
    await player.start()

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

        player.client.map.draw(screen, CELL_SIZE, WIDTH, HEIGHT)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            await player.move("LEFT")
        if keys[pygame.K_RIGHT]:
            await player.move("RIGHT")
        if keys[pygame.K_UP]:
            await player.move("UP")
        if keys[pygame.K_DOWN]:
            await player.move("DOWN")

        # Update the display
        pygame.display.flip()
        await asyncio.sleep(0.01)  # will yield control to the event loop


asyncio.run(main())
