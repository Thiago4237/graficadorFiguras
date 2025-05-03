import pygame
import time
from ui import botones_derecha, clear_button, reset_button, actualizar_textos_debug
from utils import limpiar_zona, reinciar_app, get_draw_color
from config import (
    pantalla, NEGRO, ROJO, BLANCO, GRIS, BUTTON_ANCHO, AZUL,
    ANCHO, debug_font
)
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
ultimo_click_tiempo = None # momento del ultimo click (uso poligonos)

# Datos selección activa
modo_dibujo_activo = debug_font.render("Modo: Ninguno", True, NEGRO)
color_aplicado = debug_font.render("Color: Ninguno", True, NEGRO)
puntos_seleccionados = debug_font.render("Puntos: 0", True, NEGRO)

def limpiar_area_debug():
    """
        esta funcion se encarga de realizar la limpieza del area de 
        dibujo, colocando los textos indicativos por defecto 
    """
    pantalla.fill(BLANCO, (0, 0, 180, 70))
    actualizar_textos_debug()
    pygame.display.flip()

def update_loop():
    """
    Bucle principal de actualización para manejar eventos y dibujar figuras en la interfaz.

    Esta función gestiona:
    - Eventos de mouse y teclado.
    - Selección de figuras o colores desde botones.
    - Registro de clics sobre el lienzo.
    - Previsualización de figuras mientras el usuario selecciona puntos.
    - Dibujo final de figuras cuando se completan los puntos necesarios.

    Retorna:
        False si se cierra la ventana (evento QUIT), True en otro caso implícito (sin retorno).
    """
    
    global modo_actual, puntos, dibujado, puntos_poligono, modo_dibujo_activo, mensaje_temporal
    global puntos_seleccionados, color_aplicado, color_activo, ultimo_click_tiempo

    # ---------- Manejo de eventos ----------
    for event in pygame.event.get():
        # Cierre de la ventana: terminar el programa
        if event.type == pygame.QUIT:
            pygame.quit()
            return False 
        
        # Eventos de mouse
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            # Obtener la posición del mouse
            x, y = event.pos
            
            # Clics en el panel derecho (figuras, colores, limpiar, reiniciar)
            if x >= ANCHO - BUTTON_ANCHO:
                
                # Comprobar si el mouse está sobre un botón
                for button in botones_derecha:
                    
                    # Comprobar si el mouse está sobre el botón
                    if button["rect"].collidepoint(x, y):
                        
                        # Cambiar color activo
                        if button["tipo"] == "color":
                            color_activo = button["color"]
                            color_aplicado = debug_font.render(f"Color: {button['name']}", True, NEGRO)
                        
                        # Cambiar modo de dibujo y reiniciar estado
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
                            
                            # Mostrar u ocultar mensaje según la figura seleccionada
                            if modo_actual == "Poligono":
                                mensaje_temporal = debug_font.render("Se graficará 1 segundo luego del último click.", True, ROJO)
                            
                            # Limpia el área donde aparece el mensaje
                            else:
                                mensaje_temporal = None
                                pantalla.fill(BLANCO, (100, 12, 500, 18))
                                                       
                        # Limpiar área de debug
                        limpiar_area_debug()
                        break
                    
                # Botón de limpiar lienzo
                if clear_button["rect"].collidepoint(x, y):
                    limpiar_zona()
                    puntos = []
                    puntos_poligono = []
                    dibujado = False
                    puntos_seleccionados = debug_font.render(f"Puntos: 0", True, NEGRO)
                    # Limpiar área de debug
                    limpiar_area_debug()
                
                # Botón de reinicio completo
                elif reset_button["rect"].collidepoint(x, y):
                    reinciar_app()
                    
            # Clic sobre el área de dibujo (lienzo)
            elif x < ANCHO - BUTTON_ANCHO and modo_actual:
                
                puntos.append((x, y))
                draw_point(x, y, ROJO)
                puntos_seleccionados = debug_font.render(f"Puntos: {len(puntos)}", True, NEGRO)
                
                if modo_actual == "Poligono":
                    puntos_poligono.append((x, y))
                    ultimo_click_tiempo = time.time()
                    
                dibujado = True
                # Limpiar área de debug
                limpiar_area_debug()

        # Eventos de teclado
        elif event.type == pygame.KEYDOWN:
            
            # Limpiar zona con tecla C
            if event.key == pygame.K_c:
                limpiar_zona()
                puntos = []
                puntos_poligono = []
                dibujado = False
                puntos_seleccionados = debug_font.render(f"Puntos: 0", True, NEGRO)
                # Limpiar área de debug
                limpiar_area_debug()
                
            # Reiniciar aplicación con tecla R
            elif event.key == pygame.K_r:
                reinciar_app()

    # ---------- Dibujo final con color seleccionado ----------
    if dibujado and modo_actual:
        
        color, nombre_color = get_draw_color()
        
        # dibuja linea dda
        if modo_actual == "Linea (DDA)" and len(puntos) == 2:
            draw_line_dda(puntos[0][0], puntos[0][1], puntos[1][0], puntos[1][1], color)
            puntos = []
            dibujado = False
            puntos_seleccionados = debug_font.render(f"Puntos: 0", True, NEGRO)
        
        # dibuja lina de bresenham
        elif modo_actual == "Linea (Bresenham)" and len(puntos) == 2:
            draw_line_bresenham(puntos[0][0], puntos[0][1], puntos[1][0], puntos[1][1], color)
            puntos = []
            dibujado = False
            puntos_seleccionados = debug_font.render(f"Puntos: 0", True, NEGRO)
            
        # dibuja circulo
        elif modo_actual == "Circulo (Bresenham)" and len(puntos) == 2:
            xc, yc = puntos[0]
            x1, y1 = puntos[1]
            r = int(((xc - x1) ** 2 + (yc - y1) ** 2) ** 0.5)
            draw_circle_bresenham(xc, yc, r, color)
            puntos = []
            dibujado = False
            puntos_seleccionados = debug_font.render(f"Puntos: 0", True, NEGRO)
            
        # dibuja curva
        elif modo_actual == "Curva (Bézier)" and len(puntos) == 4:
            draw_bezier_cubic(puntos[0], puntos[1], puntos[2], puntos[3], color)
            puntos = []
            dibujado = False
            puntos_seleccionados = debug_font.render(f"Puntos: 0", True, NEGRO)
            
        # dibuja triangulo
        elif modo_actual == "Triangulo" and len(puntos) == 3:
            draw_triangle(puntos[0], puntos[1], puntos[2], color)
            puntos = []
            dibujado = False
            puntos_seleccionados = debug_font.render(f"Puntos: 0", True, NEGRO)
            
        # dibuja rectangulo
        elif modo_actual == "Rectangulo" and len(puntos) == 2:
            draw_rectangle(puntos[0][0], puntos[0][1], puntos[1][0], puntos[1][1], color)
            puntos = []
            dibujado = False
            puntos_seleccionados = debug_font.render(f"Puntos: 0", True, NEGRO)
        
        # dibuja elipse
        elif modo_actual == "Ellipse" and len(puntos) == 2:
            xc = (puntos[0][0] + puntos[1][0]) // 2
            yc = (puntos[0][1] + puntos[1][1]) // 2
            a = abs(puntos[1][0] - puntos[0][0]) // 2
            b = abs(puntos[1][1] - puntos[0][1]) // 2
            draw_ellipse(xc, yc, a, b, color)
            puntos = []
            dibujado = False
            puntos_seleccionados = debug_font.render(f"Puntos: 0", True, NEGRO)

        # Detectar inactividad y dibujar polígono
        elif modo_actual == "Poligono" and len(puntos) >= 3 and ultimo_click_tiempo:
            
            # tiempo de inactividad
            if time.time() - ultimo_click_tiempo >= 1:
                draw_polygon(puntos, color)
                puntos = []
                dibujado = False
                puntos_seleccionados = debug_font.render(f"Puntos: 0", True, NEGRO)
                ultimo_click_tiempo = None  # Reinicia el temporizador
                limpiar_area_debug()

        # coloca en pantalla el mensaje temporal 
        if mensaje_temporal:
            pantalla.blit(mensaje_temporal, (250, 10))

        if not dibujado:
            # Limpiar área de debug
            limpiar_area_debug()
