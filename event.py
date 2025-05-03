import pygame
from config import (
    pantalla, NEGRO, ROJO, BLANCO, GRIS, BUTTON_ANCHO,
    ANCHO, debug_font
)
from ui import botones_derecha, clear_button, reset_button, actualizar_textos_debug
from utils import limpiar_zona, reinciar_app, get_draw_color
from drawing_algorithms import (
    draw_point, draw_line_dda, draw_line_bresenham, draw_circle_bresenham,
    draw_bezier_cubic, draw_triangle, draw_rectangle, draw_polygon, draw_ellipse
)

# Variables de estado
modo_actual = None  # Modo de dibujo actual
color_activo = None  # Color seleccionado por el usuario
puntos = []  # Lista de puntos para el dibujo actual
puntos_poligono = []  # Puntos específicos para polígonos
dibujado = False  # Estado de dibujo

# Datos selección activa
modo_dibujo_activo = debug_font.render("Modo: Ninguno", True, NEGRO)
color_aplicado = debug_font.render("Color: Ninguno", True, NEGRO)
puntos_seleccionados = debug_font.render("Puntos: 0", True, NEGRO)

def limpiar_area_debug():
    pantalla.fill(BLANCO, (0, 0, 180, 70))
    actualizar_textos_debug()
    pygame.display.flip()

def update_loop():
    global modo_actual, puntos, dibujado, puntos_poligono, modo_dibujo_activo, puntos_seleccionados, color_aplicado, color_activo

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return False  # Indica que debemos salir del bucle principal
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            # Clics en el panel derecho (figuras, colores, limpiar, reiniciar)
            if x >= ANCHO - BUTTON_ANCHO:
                for button in botones_derecha:
                    if button["rect"].collidepoint(x, y):
                        if button["tipo"] == "color":
                            color_activo = button["color"]
                            color_aplicado = debug_font.render(f"Color: {button['name']}", True, NEGRO)
                        elif button["tipo"] == "figura":
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
                        limpiar_area_debug()
                        break
                if clear_button["rect"].collidepoint(x, y):
                    limpiar_zona()
                    puntos = []
                    puntos_poligono = []
                    dibujado = False
                    puntos_seleccionados = debug_font.render(f"Puntos: 0", True, NEGRO)
                    # Limpiar área de debug
                    limpiar_area_debug()
                elif reset_button["rect"].collidepoint(x, y):
                    reinciar_app()
            # Clics en el lienzo
            elif x < ANCHO - BUTTON_ANCHO and modo_actual:
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
                limpiar_area_debug()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                limpiar_zona()
                puntos = []
                puntos_poligono = []
                dibujado = False
                puntos_seleccionados = debug_font.render(f"Puntos: 0", True, NEGRO)
                # Limpiar área de debug
                limpiar_area_debug()
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
                limpiar_area_debug()

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
        limpiar_area_debug()

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
            limpiar_area_debug()
