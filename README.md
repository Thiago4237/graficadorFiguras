# 🖌️ graficadorFiguras

Aplicación interactiva construida con **Pygame** para graficar figuras geométricas usando algoritmos clásicos de dibujo. Permite seleccionar modos de dibujo, colores, y utilizar funciones de limpieza y reinicio desde botones o atajos de teclado.

---

## 🚀 Funcionalidades

- Dibujo de figuras geométricas:
  - Línea (DDA)
  - Línea (Bresenham)
  - Círculo (Bresenham)
  - Curva (Bézier cúbica)
  - Triángulo
  - Rectángulo
  - Elipse
  - Polígono (dibujo automático tras inactividad)

- Selección de color y figura mediante botones.
- Área de depuración con información del modo actual, color activo y cantidad de puntos seleccionados.
- Gestión del lienzo (limpieza parcial o reinicio total).
- Soporte para plataformas web (Emscripten/WebAssembly).

---

## ⌨️ Atajos de Teclado

- `C` → Limpia el área de dibujo.
- `R` → Reinicia completamente la aplicación (como si se recargara).

---

## 📌 Detalles Especiales

- **Polígono**: Se genera automáticamente **1 segundo después del último clic**, permitiendo añadir múltiples vértices sin confirmar manualmente.

---

## 🛠️ Requisitos

- Python 3.8+
- Pygame
- (Opcional) Emscripten para exportación a WebAssembly

---

## ▶️ Ejecución

```bash
python main.py
