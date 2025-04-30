import pygame
import asyncio
import platform
import math

# Initialize Pygame
pygame.init()

# Window settings
ANCHO = 800  # Ancho total de la ventana
LARGO = 600  # Alto total de la ventana
BUTTON_ANCHO = 150  # Ancho del panel de botones
CANVAS_ANCHO = ANCHO - 2 * BUTTON_ANCHO  # Ancho del área de dibujo (800 - 150 - 150 = 500)
pantalla = pygame.display.set_mode((ANCHO, LARGO))  # Creación de la ventana
pygame.display.set_caption("GRAFICADOR")  # Título de la ventana
FPS = 60  # Frames por segundo

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
    "YELLOW": YELLOW
}

# Mapa inverso para obtener el nombre del color a partir de su valor RGB
COLORES_INVERSO = {v: k for k, v in COLORES.items()}

# Diccionario que asocia cada forma con su color predeterminado
COLORES_FORMA = {
    "Linea (DDA)": AZUL,
    "Linea (Bresenham)": VERDE,
    "Circulo (Bresenham)": ROJO,
    "Curva (Bézier)": PURPLE,
    "Triangulo": CYAN,
    "Recatangulo": ORANGE,
    "Poligono": MAGENTA,
    "Ellipse": YELLOW
}

# Lista de modos de dibujo disponibles
MODOS = [
    "Linea (DDA)",
    "Linea (Bresenham)",
    "Circulo (Bresenham)",
    "Curva (Bézier)",
    "Triangulo",
    "Recatangulo",
    "Poligono",
    "Ellipse"
]

modo_actual = None  # Modo de dibujo actual
color_activo = None  # Color seleccionado por el usuario
puntos = []  # Lista de puntos para el dibujo actual
puntos_poligono = []  # Puntos específicos para polígonos
dibujado = False  # Estado de dibujo

# Configuración de botones
botones_izquierda = []
botones_derecha = []

# Fuente para texto
font = pygame.font.SysFont("arial", 16)
debug_font = pygame.font.SysFont("arial", 16)

# Creación de botones para cada modo de dibujo (panel izquierdo)
for i, mode in enumerate(MODOS):
    botones_izquierda.append({
        "rect": pygame.Rect(10, 50 + i * 40, 130, 30),
        "text": font.render(f"{i+1}: {mode}", True, NEGRO),
        "mode": mode
    })

# Botones de selección de color (panel derecho)
for i, (name, color) in enumerate(COLORES.items()):
    botones_derecha.append({
        "rect": pygame.Rect(ANCHO - BUTTON_ANCHO + 10, 50 + i * 40, 130, 30),
        "text": font.render(name, True, BLANCO),
        "color": color,
        "name": name
    })

# Botones de limpiar y reiniciar (panel derecho)
clear_button = {"rect": pygame.Rect(ANCHO - BUTTON_ANCHO + 10, 530, 130, 30), "text": font.render("Limpiar (C)", True, NEGRO)}
reset_button = {"rect": pygame.Rect(ANCHO - BUTTON_ANCHO + 10, 570, 130, 30), "text": font.render("Reiniciar (R)", True, NEGRO)}

# Datos selección activa
modo_dibujo_activo = debug_font.render("Modo: Ninguno", True, NEGRO)
color_aplicado = debug_font.render("Color: Ninguno", True, NEGRO)
puntos_seleccionados = debug_font.render("Puntos: 0", True, NEGRO)

def limpiar_zona():
    """Limpia el área de dibujo"""
    pantalla.fill(BLANCO, (BUTTON_ANCHO, 0, CANVAS_ANCHO, LARGO))
    # Limpia el área de los textos de debug
    pantalla.fill(BLANCO, (BUTTON_ANCHO + 10, 0, 240, 70))
    # Actualiza los textos de debug
    pantalla.blit(modo_dibujo_activo, (BUTTON_ANCHO + 10, 10))
    pantalla.blit(puntos_seleccionados, (BUTTON_ANCHO + 10, 30))
    pantalla.blit(color_aplicado, (BUTTON_ANCHO + 10, 50))
    pygame.display.flip()

def reinciar_app():
    """Retorna todas las variables a su estado original"""
    global modo_actual, puntos, puntos_poligono, dibujado, color_activo, modo_dibujo_activo, puntos_seleccionados, color_aplicado
    modo_actual = None
    puntos = []
    puntos_poligono = []
    dibujado = False
    color_activo = None
    modo_dibujo_activo = debug_font.render("Modo: Ninguno", True, NEGRO)
    color_aplicado = debug_font.render("Color: Ninguno", True, NEGRO)
    puntos_seleccionados = debug_font.render("Puntos: 0", True, NEGRO)
    limpiar_zona()

def poner_pixel(x, y, color):
    """Dibuja un píxel en la posición (x,y) con el color especificado"""
    if BUTTON_ANCHO <= x < ANCHO - BUTTON_ANCHO and 0 <= y < LARGO:
        pantalla.set_at((x, y), color)

def draw_line_dda(x0, y0, x1, y1, color):
    """Implementa el algoritmo DDA para dibujar líneas"""
    dx = x1 - x0
    dy = y1 - y0
    steps = max(abs(dx), abs(dy)) or 1
    x_inc = dx / steps
    y_inc = dy / steps
    x, y = x0, y0
    for _ in range(int(steps) + 1):
        poner_pixel(int(x), int(y), color)
        x += x_inc
        y += y_inc

def draw_line_bresenham(x0, y0, x1, y1, color):
    """Implementa el algoritmo de Bresenham para dibujar líneas"""
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        poner_pixel(x0, y0, color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def draw_circle_bresenham(xc, yc, r, color, fill=False):
    """Dibuja un círculo usando el algoritmo de Bresenham"""
    def plot_circle_points(xc, yc, x, y, color):
        """Dibuja ocho puntos simétricos para un círculo."""
        poner_pixel(xc + x, yc + y, color)
        poner_pixel(xc - x, yc + y, color)
        poner_pixel(xc + x, yc - y, color)
        poner_pixel(xc - x, yc - y, color)
        poner_pixel(xc + y, yc + x, color)
        poner_pixel(xc - y, yc + x, color)
        poner_pixel(xc + y, yc - x, color)
        poner_pixel(xc - y, yc - x, color)

    x = 0
    y = r
    d = 3 - 2 * r

    # Dibuja el contorno usando el algoritmo de Bresenham
    while x <= y:
        plot_circle_points(xc, yc, x, y, color)
        if d < 0:
            d += 4 * x + 6
        else:
            d += 4 * (x - y) + 10
            y -= 1
        x += 1

    # Rellena el círculo si se solicita
    if fill:
        for y in range(-r, r + 1):
            for x in range(-r, r + 1):
                if x * x + y * y <= r * r:
                    poner_pixel(xc + x, yc + y, color)
                    poner_pixel(xc - x, yc + y, color)

def draw_bezier_cubic(p0, p1, p2, p3, color):
    """Dibuja una curva de Bézier cúbica"""
    t = 0.0
    while t <= 1.0:
        t2 = t * t
        t3 = t2 * t
        mt = 1 - t
        mt2 = mt * mt
        mt3 = mt2 * mt
        x = mt3 * p0[0] + 3 * mt2 * t * p1[0] + 3 * mt * t2 * p2[0] + t3 * p3[0]
        y = mt3 * p0[1] + 3 * mt2 * t * p1[1] + 3 * mt * t2 * p2[1] + t3 * p3[1]
        poner_pixel(int(x), int(y), color)
        t += 0.01

def draw_triangle(p0, p1, p2, color):
    """Dibuja un triángulo usando líneas de Bresenham"""
    draw_line_bresenham(p0[0], p0[1], p1[0], p1[1], color)
    draw_line_bresenham(p1[0], p1[1], p2[0], p2[1], color)
    draw_line_bresenham(p2[0], p2[1], p0[0], p0[1], color)

def draw_rectangle(x0, y0, x1, y1, color):
    """Dibuja un rectángulo usando el algoritmo de Bresenham"""
    draw_line_bresenham(x0, y0, x1, y0, color)
    draw_line_bresenham(x1, y0, x1, y1, color)
    draw_line_bresenham(x1, y1, x0, y1, color)
    draw_line_bresenham(x0, y1, x0, y0, color)

def draw_polygon(puntos, color):
    """Dibuja un polígono conectando puntos consecutivos"""
    for i in range(len(puntos)):
        p1 = puntos[i]
        p2 = puntos[(i + 1) % len(puntos)]
        draw_line_bresenham(p1[0], p1[1], p2[0], p2[1], color)

def draw_ellipse(xc, yc, a, b, color):
    """Dibuja una elipse usando ecuaciones paramétricas"""
    for theta in range(0, 360):
        x = xc + a * math.cos(math.radians(theta))
        y = yc + b * math.sin(math.radians(theta))
        poner_pixel(int(x), int(y), color)

def draw_point(x, y, color):
    """Dibuja un punto como un cuadrado de 5x5 píxeles"""
    for i in range(-2, 3):
        for j in range(-2, 3):
            poner_pixel(x + i, y + j, color)

def get_draw_color():
    """Devuelve el color activo o el predeterminado para el modo actual, junto con su nombre"""
    if color_activo:
        color = color_activo
        nombre = COLORES_INVERSO.get(color, "Desconocido")
    else:
        color = COLORES_FORMA.get(modo_actual, AZUL)
        nombre = COLORES_INVERSO.get(color, "AZUL")
    return color, nombre

def setup():
    """Inicializa la interfaz de usuario"""
    pantalla.fill(BLANCO)
    # Dibuja los paneles de botones (izquierdo y derecho)
    pygame.draw.rect(pantalla, GRIS, (0, 0, BUTTON_ANCHO, LARGO))  # Panel izquierdo
    pygame.draw.rect(pantalla, GRIS, (ANCHO - BUTTON_ANCHO, 0, BUTTON_ANCHO, LARGO))  # Panel derecho

    # Dibuja botones del panel izquierdo (modos)
    for button in botones_izquierda:
        pygame.draw.rect(pantalla, BLANCO, button["rect"])
        text_rect = button["text"].get_rect(center=button["rect"].center)
        pantalla.blit(button["text"], text_rect)

    # Dibuja botones del panel derecho (colores, limpiar, reiniciar)
    for button in botones_derecha:
        pygame.draw.rect(pantalla, button["color"], button["rect"])
        text_rect = button["text"].get_rect(center=button["rect"].center)
        pantalla.blit(button["text"], text_rect)

    pygame.draw.rect(pantalla, BLANCO, clear_button["rect"])
    text_rect = clear_button["text"].get_rect(center=clear_button["rect"].center)
    pantalla.blit(clear_button["text"], text_rect)
    pygame.draw.rect(pantalla, BLANCO, reset_button["rect"])
    text_rect = reset_button["text"].get_rect(center=reset_button["rect"].center)
    pantalla.blit(reset_button["text"], text_rect)

    # Dibuja los textos de debug iniciales
    pantalla.blit(modo_dibujo_activo, (BUTTON_ANCHO + 10, 10))
    pantalla.blit(puntos_seleccionados, (BUTTON_ANCHO + 10, 30))
    pantalla.blit(color_aplicado, (BUTTON_ANCHO + 10, 50))
    pygame.display.flip()

def update_loop():
    global modo_actual, puntos, dibujado, puntos_poligono, modo_dibujo_activo, puntos_seleccionados, color_aplicado, color_activo

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            # Clics en el panel izquierdo (modos)
            if x < BUTTON_ANCHO:
                for button in botones_izquierda:
                    if button["rect"].collidepoint(x, y):
                        modo_actual = button["mode"]
                        puntos = []
                        puntos_poligono = []
                        dibujado = False
                        modo_dibujo_activo = debug_font.render(f"Modo: {modo_actual}", True, NEGRO)
                        puntos_seleccionados = debug_font.render(f"Puntos: 0", True, NEGRO)
                        # Actualizar el color al predeterminado del modo
                        color, nombre_color = get_draw_color()
                        color_aplicado = debug_font.render(f"Color: {nombre_color}", True, NEGRO)
                        # Limpiar área de debug
                        pantalla.fill(BLANCO, (BUTTON_ANCHO + 10, 0, 240, 70))
                        pantalla.blit(modo_dibujo_activo, (BUTTON_ANCHO + 10, 10))
                        pantalla.blit(puntos_seleccionados, (BUTTON_ANCHO + 10, 30))
                        pantalla.blit(color_aplicado, (BUTTON_ANCHO + 10, 50))
                        pygame.display.flip()
                        break
            # Clics en el panel derecho (colores, limpiar, reiniciar)
            elif x >= ANCHO - BUTTON_ANCHO:
                for button in botones_derecha:
                    if button["rect"].collidepoint(x, y):
                        color_activo = button["color"]
                        color_aplicado = debug_font.render(f"Color: {button['name']}", True, NEGRO)
                        # Limpiar área de debug
                        pantalla.fill(BLANCO, (BUTTON_ANCHO + 10, 0, 240, 70))
                        pantalla.blit(modo_dibujo_activo, (BUTTON_ANCHO + 10, 10))
                        pantalla.blit(puntos_seleccionados, (BUTTON_ANCHO + 10, 30))
                        pantalla.blit(color_aplicado, (BUTTON_ANCHO + 10, 50))
                        pygame.display.flip()
                        break
                if clear_button["rect"].collidepoint(x, y):
                    limpiar_zona()
                    puntos = []
                    puntos_poligono = []
                    dibujado = False
                    puntos_seleccionados = debug_font.render(f"Puntos: 0", True, NEGRO)
                    # Limpiar área de debug
                    pantalla.fill(BLANCO, (BUTTON_ANCHO + 10, 0, 240, 70))
                    pantalla.blit(modo_dibujo_activo, (BUTTON_ANCHO + 10, 10))
                    pantalla.blit(puntos_seleccionados, (BUTTON_ANCHO + 10, 30))
                    pantalla.blit(color_aplicado, (BUTTON_ANCHO + 10, 50))
                    pygame.display.flip()
                elif reset_button["rect"].collidepoint(x, y):
                    reinciar_app()
            # Clics en el lienzo
            elif BUTTON_ANCHO <= x < ANCHO - BUTTON_ANCHO and modo_actual:
                puntos.append((x, y))
                draw_point(x, y, ROJO)
                puntos_seleccionados = debug_font.render(f"Puntos: {len(puntos)}", True, NEGRO)
                if modo_actual == "Poligono":
                    puntos_poligono.append((x, y))
                    if len(puntos_poligono) >= 2:
                        color, _ = get_draw_color()
                        draw_line_bresenham(
                            puntos_poligono[-2][0], puntos_poligono[-2][1],
                            puntos_poligono[-1][0], puntos_poligono[-1][1], color
                        )
                dibujado = True
                # Limpiar área de debug
                pantalla.fill(BLANCO, (BUTTON_ANCHO + 10, 0, 240, 70))
                pantalla.blit(modo_dibujo_activo, (BUTTON_ANCHO + 10, 10))
                pantalla.blit(puntos_seleccionados, (BUTTON_ANCHO + 10, 30))
                pantalla.blit(color_aplicado, (BUTTON_ANCHO + 10, 50))
                pygame.display.flip()

        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8):
                index = event.key - pygame.K_1
                if index < len(MODOS):
                    modo_actual = MODOS[index]
                    puntos = []
                    puntos_poligono = []
                    dibujado = False
                    modo_dibujo_activo = debug_font.render(f"Modo: {modo_actual}", True, NEGRO)
                    puntos_seleccionados = debug_font.render(f"Puntos: 0", True, NEGRO)
                    color, nombre_color = get_draw_color()
                    color_aplicado = debug_font.render(f"Color: {nombre_color}", True, NEGRO)
                    # Limpiar área de debug
                    pantalla.fill(BLANCO, (BUTTON_ANCHO + 10, 0, 240, 70))
                    pantalla.blit(modo_dibujo_activo, (BUTTON_ANCHO + 10, 10))
                    pantalla.blit(puntos_seleccionados, (BUTTON_ANCHO + 10, 30))
                    pantalla.blit(color_aplicado, (BUTTON_ANCHO + 10, 50))
                    pygame.display.flip()
            elif event.key == pygame.K_c:
                limpiar_zona()
                puntos = []
                puntos_poligono = []
                dibujado = False
                puntos_seleccionados = debug_font.render(f"Puntos: 0", True, NEGRO)
                # Limpiar área de debug
                pantalla.fill(BLANCO, (BUTTON_ANCHO + 10, 0, 240, 70))
                pantalla.blit(modo_dibujo_activo, (BUTTON_ANCHO + 10, 10))
                pantalla.blit(puntos_seleccionados, (BUTTON_ANCHO + 10, 30))
                pantalla.blit(color_aplicado, (BUTTON_ANCHO + 10, 50))
                pygame.display.flip()
            elif event.key == pygame.K_r:
                reinciar_app()
            elif event.key == pygame.K_RETURN and modo_actual == "Poligono" and len(puntos_poligono) >= 3:
                color, _ = get_draw_color()
                draw_polygon(puntos_poligono, color)
                puntos_poligono = []
                puntos = []
                dibujado = False
                puntos_seleccionados = debug_font.render(f"Puntos: 0", True, NEGRO)
                # Limpiar área de debug
                pantalla.fill(BLANCO, (BUTTON_ANCHO + 10, 0, 240, 70))
                pantalla.blit(modo_dibujo_activo, (BUTTON_ANCHO + 10, 10))
                pantalla.blit(puntos_seleccionados, (BUTTON_ANCHO + 10, 30))
                pantalla.blit(color_aplicado, (BUTTON_ANCHO + 10, 50))
                pygame.display.flip()

    # Previsualización en tiempo real
    if dibujado and modo_actual and len(puntos) >= 2:
        for pt in puntos:
            draw_point(pt[0], pt[1], ROJO)
        if modo_actual in ["Linea (DDA)", "Linea (Bresenham)", "Recatangulo"] and len(puntos) == 2:
            if modo_actual == "Linea (DDA)":
                draw_line_dda(puntos[0][0], puntos[0][1], puntos[1][0], puntos[1][1], GRIS)
            elif modo_actual == "Linea (Bresenham)":
                draw_line_bresenham(puntos[0][0], puntos[0][1], puntos[1][0], puntos[1][1], GRIS)
            elif modo_actual == "Recatangulo":
                draw_rectangle(puntos[0][0], puntos[0][1], puntos[1][0], puntos[1][1], GRIS)
        elif modo_actual == "Triangulo" and len(puntos) == 3:
            draw_triangle(puntos[0], puntos[1], puntos[2], GRIS)
        elif modo_actual == "Curva (Bézier)" and len(puntos) == 4:
            draw_bezier_cubic(puntos[0], puntos[1], puntos[2], puntos[3], GRIS)
        elif modo_actual == "Poligono" and puntos_poligono:
            draw_polygon(puntos_poligono, GRIS)
        # Limpiar área de debug
        pantalla.fill(BLANCO, (BUTTON_ANCHO + 10, 0, 240, 70))
        pantalla.blit(modo_dibujo_activo, (BUTTON_ANCHO + 10, 10))
        pantalla.blit(puntos_seleccionados, (BUTTON_ANCHO + 10, 30))
        pantalla.blit(color_aplicado, (BUTTON_ANCHO + 10, 50))
        pygame.display.flip()

    # Dibujar la forma final
    if dibujado and modo_actual and modo_actual != "Poligono":
        color, nombre_color = get_draw_color()
        if modo_actual == "Linea (DDA)" and len(puntos) == 2:
            draw_line_dda(puntos[0][0], puntos[0][1], puntos[1][0], puntos[1][1], color)
            puntos = []
            dibujado = False
            puntos_seleccionados = debug_font.render(f"Puntos: 0", True, NEGRO)
        elif modo_actual == "Linea (Bresenham)" and len(puntos) == 2:
            draw_line_bresenham(puntos[0][0], puntos[0][1], puntos[1][0], puntos[1][1], color)
            puntos = []
            dibujado = False
            puntos_seleccionados = debug_font.render(f"Puntos: 0", True, NEGRO)
        elif modo_actual == "Circulo (Bresenham)" and len(puntos) == 2:
            xc, yc = puntos[0]
            x1, y1 = puntos[1]
            r = int(((xc - x1) ** 2 + (yc - y1) ** 2) ** 0.5)
            draw_circle_bresenham(xc, yc, r, color)
            puntos = []
            dibujado = False
            puntos_seleccionados = debug_font.render(f"Puntos: 0", True, NEGRO)
        elif modo_actual == "Curva (Bézier)" and len(puntos) == 4:
            draw_bezier_cubic(puntos[0], puntos[1], puntos[2], puntos[3], color)
            puntos = []
            dibujado = False
            puntos_seleccionados = debug_font.render(f"Puntos: 0", True, NEGRO)
        elif modo_actual == "Triangulo" and len(puntos) == 3:
            draw_triangle(puntos[0], puntos[1], puntos[2], color)
            puntos = []
            dibujado = False
            puntos_seleccionados = debug_font.render(f"Puntos: 0", True, NEGRO)
        elif modo_actual == "Recatangulo" and len(puntos) == 2:
            draw_rectangle(puntos[0][0], puntos[0][1], puntos[1][0], puntos[1][1], color)
            puntos = []
            dibujado = False
            puntos_seleccionados = debug_font.render(f"Puntos: 0", True, NEGRO)
        elif modo_actual == "Ellipse" and len(puntos) == 2:
            xc = (puntos[0][0] + puntos[1][0]) // 2
            yc = (puntos[0][1] + puntos[1][1]) // 2
            a = abs(puntos[1][0] - puntos[0][0]) // 2
            b = abs(puntos[1][1] - puntos[0][1]) // 2
            draw_ellipse(xc, yc, a, b, color)
            puntos = []
            dibujado = False
            puntos_seleccionados = debug_font.render(f"Puntos: 0", True, NEGRO)

        if not dibujado:
            # Limpiar área de debug
            pantalla.fill(BLANCO, (BUTTON_ANCHO + 10, 0, 240, 70))
            pantalla.blit(modo_dibujo_activo, (BUTTON_ANCHO + 10, 10))
            pantalla.blit(puntos_seleccionados, (BUTTON_ANCHO + 10, 30))
            pantalla.blit(color_aplicado, (BUTTON_ANCHO + 10, 50))
            pygame.display.flip()

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