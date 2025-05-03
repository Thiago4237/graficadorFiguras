import pygame

# Initialize Pygame
pygame.init()

# Window settings
ANCHO = 800  # Ancho total de la ventana
LARGO = 600  # Alto total de la ventana
BUTTON_ANCHO = 150  # Ancho del panel de botones
CANVAS_ANCHO = ANCHO - BUTTON_ANCHO  # Ancho del área de dibujo (800 - 150 = 650)
FPS = 60  # Frames por segundo

# Directorio de iconos
ICONS_DIR = "icons"

# Colores básicos en formato RGB
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
PANEL_COLOR = (234, 234, 234)

# Colores personalizados
COLORES = {
    "ROJO": ROJO,
    "VERDE": VERDE,
    "AZUL": AZUL,
    "NEGRO": NEGRO,
    "PURPLE": PURPLE,
    "CYAN": CYAN,
    "ORANGE": ORANGE,
    "MAGENTA": MAGENTA,
    "YELLOW": YELLOW,
    "GRIS": GRIS
}

# Mapa inverso para obtener el nombre del color a partir de su valor RGB
COLORES_INVERSO = {v: k for k, v in COLORES.items()}

# Lista de modos de dibujo disponibles
MODOS = [
    "Linea (DDA)",
    "Linea (Bresenham)",
    "Circulo (Bresenham)",
    "Curva (Bézier)",
    "Triangulo",
    "Rectangulo",
    "Poligono",
    "Ellipse"
]

# Diccionario que asocia cada forma con su color predeterminado
COLORES_FORMA = {
    "Linea (DDA)": AZUL,
    "Linea (Bresenham)": VERDE,
    "Circulo (Bresenham)": ROJO,
    "Curva (Bézier)": PURPLE,
    "Triangulo": CYAN,
    "Rectangulo": ORANGE,
    "Poligono": MAGENTA,
    "Ellipse": YELLOW
}

# Mapeo de nombres de modos a nombres de archivo de iconos
ICONOS = {
    "Linea (DDA)": "linea.png",
    "Linea (Bresenham)": "line_bresenham.png",
    "Circulo (Bresenham)": "circle.png",
    "Curva (Bézier)": "bezier.png",
    "Triangulo": "triangle.png",
    "Rectangulo": "rectangle.png",
    "Poligono": "polygon.png",
    "Ellipse": "ellipse.png"
}

# Configuración global de la aplicación
pantalla = pygame.display.set_mode((ANCHO, LARGO))  # Creación de la ventana
pygame.display.set_caption("GRAFICADOR")  # Título de la ventana

# Fuentes
debug_font = font = pygame.font.SysFont("arial", 16, bold=True)
