import pygame
import asyncio
import platform
from ui import setup
from event import update_loop
from config import FPS

# Initialize Pygame
pygame.init()

async def main():
    setup()
    while True:
        update_loop()
        await asyncio.sleep(1.0 / FPS)

# Inicio de la aplicación según la plataforma
if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())