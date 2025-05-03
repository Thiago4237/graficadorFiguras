import pygame
import asyncio
import platform
from ui import setup
from event import update_loop
from config import FPS

# Initialize Pygame
pygame.init()

async def main():
    """
    Función principal asincrónica que controla el ciclo de vida de la aplicación.

    Esta función:
    - Inicializa la interfaz gráfica llamando a `setup()`.
    - Ejecuta un bucle infinito donde:
        - Llama a `update_loop()` para procesar eventos y lógica de dibujo.
        - Espera una fracción de segundo basada en los FPS configurados, 
          para mantener una tasa de actualización constante sin bloquear la interfaz.

    Es compatible con entornos asincrónicos, como Emscripten (para WebAssembly).
    """
    setup()
    while True:
        update_loop()
        await asyncio.sleep(1.0 / FPS)

# Inicio de la aplicación según la plataforma
# - Si se ejecuta en un navegador (Emscripten), se usa `asyncio.ensure_future` para agendar la tarea principal.
# - Si se ejecuta como un script estándar en escritorio, se usa `asyncio.run` para iniciar el bucle de eventos.
if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())