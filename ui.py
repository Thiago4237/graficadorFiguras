import pygame
from config import (
    pantalla, BLANCO, GRIS, NEGRO, BUTTON_ANCHO, ANCHO, LARGO,
    MODOS, COLORES, font, debug_font
)

# Configuración de botones
botones_izquierda = []
botones_derecha = []

# Botones de limpiar y reiniciar (panel derecho)
clear_button = {"rect": pygame.Rect(ANCHO - BUTTON_ANCHO + 10, 530, 130, 30), "text": font.render("Limpiar (C)", True, NEGRO)}
reset_button = {"rect": pygame.Rect(ANCHO - BUTTON_ANCHO + 10, 570, 130, 30), "text": font.render("Reiniciar (R)", True, NEGRO)}

def setup_botones():
    """Configura los botones de la interfaz"""
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

def actualizar_textos_debug():
    """Actualiza y muestra los textos de debug en pantalla"""
    import event
    
    pantalla.blit(event.modo_dibujo_activo, (BUTTON_ANCHO + 10, 10))
    pantalla.blit(event.puntos_seleccionados, (BUTTON_ANCHO + 10, 30))
    pantalla.blit(event.color_aplicado, (BUTTON_ANCHO + 10, 50))

def setup():
    """Inicializa la interfaz de usuario"""
    # import event
    
    setup_botones()
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
    actualizar_textos_debug()

    pygame.display.flip()