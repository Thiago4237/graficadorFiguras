import pygame
from config import pantalla, BLANCO, BUTTON_ANCHO, LARGO, CANVAS_ANCHO, COLORES_FORMA, COLORES_INVERSO

def limpiar_zona():
    """Limpia el área de dibujo"""
    from ui import actualizar_textos_debug
    
    pantalla.fill(BLANCO, (BUTTON_ANCHO, 0, CANVAS_ANCHO, LARGO))
    # Limpia el área de los textos de debug
    pantalla.fill(BLANCO, (BUTTON_ANCHO + 10, 0, 240, 70))
    # Actualiza los textos de debug
    actualizar_textos_debug()
    pygame.display.flip()

def reinciar_app():
    """Retorna todas las variables a su estado original"""
    import event
    
    event.modo_actual = None
    event.puntos = []
    event.puntos_poligono = []
    event.dibujado = False
    event.color_activo = None
    event.modo_dibujo_activo = event.debug_font.render("Modo: Ninguno", True, event.NEGRO)
    event.color_aplicado = event.debug_font.render("Color: Ninguno", True, event.NEGRO)
    event.puntos_seleccionados = event.debug_font.render("Puntos: 0", True, event.NEGRO)
    limpiar_zona()

def get_draw_color():
    """Devuelve el color activo o el predeterminado para el modo actual, junto con su nombre"""
    import event
    
    if event.color_activo:
        color = event.color_activo
        nombre = COLORES_INVERSO.get(color, "Desconocido")
    else:
        color = COLORES_FORMA.get(event.modo_actual, event.AZUL)
        nombre = COLORES_INVERSO.get(color, "AZUL")
    return color, nombre