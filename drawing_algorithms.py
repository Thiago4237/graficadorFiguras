import math
from config import pantalla, BUTTON_ANCHO, ANCHO, LARGO

def poner_pixel(x, y, color):
    """Dibuja un píxel en la posición (x,y) con el color especificado"""
    if 0 <= x < ANCHO - BUTTON_ANCHO and 0 <= y < LARGO:
        pantalla.set_at((x, y), color)

def draw_point(x, y, color):
    """Dibuja un punto como un cuadrado de 5x5 píxeles"""
    # dibuja el cuadrado visible dejando la posición del pixel en el centro
    for i in range(-2, 3):
        for j in range(-2, 3):
            poner_pixel(x + i, y + j, color)

def draw_line_dda(x0, y0, x1, y1, color):
    """Implementa el algoritmo DDA para dibujar líneas"""
    # distancia entre los puntos
    dx = x1 - x0
    dy = y1 - y0
    # número de pasos necesarios para dibujar la línea
    steps = max(abs(dx), abs(dy)) or 1
    # incremento en x e y para cada paso
    x_inc = dx / steps
    y_inc = dy / steps
    x, y = x0, y0
    # dibuja el pixel en cada paso
    for _ in range(int(steps) + 1):
        poner_pixel(int(x), int(y), color)
        x += x_inc  
        y += y_inc

def draw_line_bresenham(x0, y0, x1, y1, color):
    """Implementa el algoritmo de Bresenham para dibujar líneas"""
    # distancia entre los puntos
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    # dirección de la línea
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    # error acumulado
    err = dx - dy
    # dibuja el pixel en cada paso
    while True:
        poner_pixel(x0, y0, color)
        # si se ha llegado al final de la línea, salir del bucle
        if x0 == x1 and y0 == y1:
            break
        # calcular el error acumulado
        e2 = 2 * err
        # ajustar la posición del pixel según el error acumulado
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

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

def draw_circle_bresenham(xc, yc, r, color, fill=True):
    """Dibuja un círculo usando el algoritmo de Bresenham"""
    # Inicializa las variables
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
    # p0, p1, p2, p3 son los puntos de control
    t = 0.0
    # Incremento de t para el trazado de la curva
    while t <= 1.0:
        # Fórmula de Bézier cúbica
        t2 = t * t
        t3 = t2 * t
        mt = 1 - t
        mt2 = mt * mt
        mt3 = mt2 * mt
        # Calcula las coordenadas x e y de la curva
        x = mt3 * p0[0] + 3 * mt2 * t * p1[0] + 3 * mt * t2 * p2[0] + t3 * p3[0]
        y = mt3 * p0[1] + 3 * mt2 * t * p1[1] + 3 * mt * t2 * p2[1] + t3 * p3[1]
        # Dibuja el pixel en la posición calculada
        poner_pixel(int(x), int(y), color)
        t += 0.01

def draw_triangle(p0, p1, p2, color):
    """Dibuja un triángulo usando líneas de Bresenham"""
    # p0, p1, p2 son los vértices del triángulo
    # Dibuja las tres líneas que forman el triángulo
    draw_line_bresenham(p0[0], p0[1], p1[0], p1[1], color)
    draw_line_bresenham(p1[0], p1[1], p2[0], p2[1], color)
    draw_line_bresenham(p2[0], p2[1], p0[0], p0[1], color)

def draw_rectangle(x0, y0, x1, y1, color):
    """Dibuja un rectángulo usando el algoritmo de Bresenham"""
    # x0, y0 son las coordenadas de la esquina superior izquierda
    # x1, y1 son las coordenadas de la esquina inferior derecha
    # Dibuja las cuatro líneas que forman el rectángulo
    draw_line_bresenham(x0, y0, x1, y0, color)
    draw_line_bresenham(x1, y0, x1, y1, color)
    draw_line_bresenham(x1, y1, x0, y1, color)
    draw_line_bresenham(x0, y1, x0, y0, color)

def draw_polygon(puntos, color):
    """Dibuja un polígono conectando puntos consecutivos"""
    # puntos es una lista de tuplas (x, y) que representan los vértices del polígono
    # Dibuja líneas entre cada par de puntos consecutivos
    print(puntos)
    for i in range(len(puntos)):
        p1 = puntos[i]
        p2 = puntos[(i + 1) % len(puntos)]
        draw_line_bresenham(p1[0], p1[1], p2[0], p2[1], color)

def draw_ellipse(xc, yc, a, b, color):
    """Dibuja una elipse usando ecuaciones paramétricas"""
    # xc, yc son las coordenadas del centro de la elipse
    for theta in range(0, 360):
        # Ecuaciones paramétricas de la elipse
        x = xc + a * math.cos(math.radians(theta))
        y = yc + b * math.sin(math.radians(theta))
        # Dibuja el pixel en la posición calculada
        poner_pixel(int(x), int(y), color)