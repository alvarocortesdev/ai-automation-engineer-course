---
ejercicio_id: fase-4/landing-semantica-responsive
fase: fase-4
sub_unidad: "4.1"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Landing semántica y responsive

Los archivos completos están junto a este documento:
- `index.html` — la estructura semántica.
- `styles.css` — el CSS mobile-first.

Ambos **pasan los 11 tests** de `node --test`. A continuación, qué hace correcto a esta solución (lo que el corrector debe buscar en la entrega del alumno).

## Decisiones clave (lo que se evalúa)

### HTML semántico
- `<html lang="es">` + `<head>` con `charset` y `viewport` (sin viewport, el responsive no funciona en móvil real).
- Un solo `<h1>` (el nombre del producto, en el `header`). El resto baja en orden: `h2` por sección, `h3` por tarjeta. La jerarquía de encabezados **es** el índice del documento.
- Landmarks reales: `header`, `nav` (con `aria-label="Principal"`), `main` (único), `footer`. Nada de `div` con clase `.header`.
- Cada tarjeta es un `<article>` (contenido autocontenido) con su `<h3>`; las imágenes llevan `alt` **descriptivo** (no "imagen").
- **Prueba de fuego:** la página se lee de corrido sin CSS, en orden lógico. Eso confirma que la estructura no depende del estilo.

### CSS mobile-first
- `box-sizing: border-box` global: la caja mide lo que dice su `width`.
- **Base = móvil:** `header` y `nav` en `flex-direction: column`; `.tarjetas` en una sola columna (`grid-template-columns: 1fr`).
- **`@media (min-width: 700px)`** que *añade* la complejidad de escritorio: nav en fila (`flex-direction: row` + `justify-content: space-between`) y tarjetas en `repeat(auto-fill, minmax(220px, 1fr))`.
- **Flexbox (1D)** para la nav y el header (una fila/columna); **Grid (2D)** para la rejilla de tarjetas. Es el criterio del objetivo O3.
- Tipografía y espaciado en `rem` (escalan con la preferencia de fuente del usuario); `img { max-width: 100%; height: auto; }` para que las imágenes no desborden.

## Rango de soluciones aceptables
- El breakpoint no tiene que ser 700px: cualquier `min-width` razonable (600–900px) es válido si el resultado se adapta bien.
- La rejilla puede resolverse con `auto-fill` o `auto-fit`, o incluso con columnas explícitas dentro de la media query; lo que importa es que use Grid y se adapte.
- Los colores, fuentes y textos son libres. La estructura semántica y el comportamiento responsive son lo evaluable.
- Es válido (y `excelente`) que el alumno agregue un `<aside>`, variables CSS o un grid sin breakpoints — siempre que pueda **explicarlo** y la base siga siendo mobile-first.

## Banderas
- Si la entrega es visualmente impecable pero el alumno no puede explicar por qué Grid en un lado y Flexbox en otro, o no entregó `spec.md`, mirar las **señales de dependencia-IA** de la rúbrica antes de calificar como `excelente`.
- Pasar los tests con *div-soup* es imposible (el test exige landmarks), pero sí es posible pasar con encabezados desordenados o `alt` pobres: eso lo atrapa el ojo del corrector, no el test.
