import pygame
from config import (
    pantalla, BLANCO, NEGRO, BUTTON_ANCHO, ANCHO, LARGO,
    MODOS, COLORES, PANEL_COLOR, font
)
from utils import cargar_iconos

# Configuración de botones
botones_derecha = []
iconos = {}  # Almacenará los iconos cargados

# Botones de limpiar y reiniciar (panel derecho)
clear_button = {"rect": pygame.Rect(ANCHO - BUTTON_ANCHO + 10, 510, 130, 30), "text": font.render("Limpiar (C)", True, NEGRO)}
reset_button = {"rect": pygame.Rect(ANCHO - BUTTON_ANCHO + 10, 550, 130, 30), "text": font.render("Reiniciar (R)", True, NEGRO)}

def setup_botones():
    """Configura los botones de la interfaz"""
    global iconos
    # Cargar los iconos
    iconos = cargar_iconos()
    
    # Creación de botones para cada modo de dibujo (panel derecho, sección figuras)
    y_inicio_figuras = 45  # Posición inicial después del título "Figuras"
    for i, mode in enumerate(MODOS):
        # Calcular fila y columna
        fila = i // 2  # División entera para obtener la fila
        columna = i % 2  # Módulo para obtener la columna (0 o 1)
        
        # Calcular posición x e y
        x = ANCHO - BUTTON_ANCHO + 20 + (columna * 60)  # Primera columna y segunda columna
        y = y_inicio_figuras + (fila * 45)  # 45 = alto del botón (35) + espacio (10)
        
        botones_derecha.append({
            "rect": pygame.Rect(x, y, 45, 35),
            "text": font.render(f"{i+1}: {mode}", True, NEGRO),
            "mode": mode,
            "icon": iconos.get(mode),
            "tipo": "figura"
        })

    # Botones de colores
    y_inicio_colores = y_inicio_figuras + ((len(MODOS) // 2 + 1) * 43) + 10  # Espacio después de figuras + título
    for i, (name, color) in enumerate(COLORES.items()):
        fila = i // 2
        columna = i % 2
        
        x = ANCHO - BUTTON_ANCHO + 20 + (columna * 60)
        y = y_inicio_colores + (fila * 45)
        
        botones_derecha.append({
            "rect": pygame.Rect(x, y, 45, 35),
            "text": font.render(name, True, BLANCO),
            "color": color,
            "name": name,
            "tipo": "color"
        })

def actualizar_textos_debug():
    """Actualiza y muestra los textos de debug en pantalla"""
    import event
    
    pantalla.blit(event.modo_dibujo_activo, (10, 10))
    pantalla.blit(event.puntos_seleccionados, (10, 30))
    pantalla.blit(event.color_aplicado, (10, 50))

def setup():
    """Inicializa la interfaz de usuario"""
    setup_botones()
    pantalla.fill(BLANCO)
    
    # Dibuja los paneles de botones (izquierdo y derecho)
    pygame.draw.rect(pantalla, PANEL_COLOR, (ANCHO - BUTTON_ANCHO, 0, BUTTON_ANCHO, LARGO))  # Panel derecho

    # Dibujar títulos de secciones
    titulo_figuras = font.render("FIGURAS", True, NEGRO)
    titulo_colores = font.render("COLORES", True, NEGRO)
    pantalla.blit(titulo_figuras, (ANCHO - BUTTON_ANCHO + 10, 15))
    y_titulo_colores = 80 + ((len(MODOS) // 2 + 1) * 31.5)  # Después de la sección de figuras
    pantalla.blit(titulo_colores, (ANCHO - BUTTON_ANCHO + 10, y_titulo_colores))

    # Dibuja botones del panel derecho
    for button in botones_derecha:
        if button["tipo"] == "figura":
            pygame.draw.rect(pantalla, BLANCO, button["rect"], border_radius=7)
            if button["icon"]:
                # Escala el icono para que quepa bien en el botón
                icono_ajustado = pygame.transform.smoothscale(button["icon"], (28, 28))
                icon_rect = icono_ajustado.get_rect(center=button["rect"].center)
                pantalla.blit(icono_ajustado, icon_rect)
        else:  # botones de color
            pygame.draw.rect(pantalla, button["color"], button["rect"], border_radius=7)

    # Dibujar botones de control
    pygame.draw.rect(pantalla, BLANCO, clear_button["rect"], border_radius=7)
    text_rect = clear_button["text"].get_rect(center=clear_button["rect"].center)
    pantalla.blit(clear_button["text"], text_rect)
    
    pygame.draw.rect(pantalla, BLANCO, reset_button["rect"], border_radius=7)
    text_rect = reset_button["text"].get_rect(center=reset_button["rect"].center)
    pantalla.blit(reset_button["text"], text_rect)

    # Dibuja los textos de debug iniciales
    actualizar_textos_debug()

    pygame.display.flip()