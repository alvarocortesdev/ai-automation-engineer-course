# Ejercicio 4.1 — Landing semántica y responsive (sin frameworks)

> **Modalidad: código (HTML + CSS a mano), Primero-Sin-IA.** Sin Tailwind, sin librerías, sin IA para generar. Construyes la interfaz con las herramientas crudas para *entenderlas* antes de que un framework te las esconda.

**Fase:** Fase 4 — Frontend + UI/UX · **Lección:** `4.1` HTML semántico + CSS
**Ruta:** crítica · **Timebox:** 40–50 min

## 🎯 Objetivo

Construir la landing de una app de IA ficticia (**NeuralNotes**, un "segundo cerebro" con IA) con **HTML semántico** y un **layout responsive mobile-first**, usando Flexbox y Grid, unidades `rem` y una `media query`. Al terminar sabrás estructurar una página accesible y que se adapta a cualquier pantalla, sin depender de un framework.

## 📋 Contexto

Es el primer ladrillo del [Capstone F4 — Frontend de una app de IA]. Antes de que React genere el HTML por ti, necesitas saber qué HTML es *correcto*: si tu estructura es semántica y responsive a mano, lo será también cuando lo automatices. La accesibilidad (WCAG 2.2) será un **gate** del capstone, y empieza aquí.

## 📏 Primero-Sin-IA

1. **Empieza por una mini-spec** (3–5 líneas, en `spec.md`): qué secciones tiene la página y cómo se reacomodan en móvil vs. desktop. Diseñar antes de codear es el hábito (spec-driven).
2. Resuélvelo **a mano** (timebox arriba). Está bien que sea feo y lento.
3. Solo entonces, consulta **documentación oficial** (MDN, web.dev — ver lección).
4. **Solo al final**, usa IA para *revisar y explicar* — no para *generar* el HTML/CSS.
5. Mañana, **reescribe de memoria** el esqueleto semántico. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `index.html` y `styles.css`. Completa lo que marcan los `TODO` (no borres el `<head>` ni el reset de `box-sizing`).
2. La página debe tener, como mínimo:
   - un `<header>` con **un solo `<h1>`** (nombre del producto) y un `<nav>` con 3 enlaces;
   - un `<main>` con una sección "hero" (`<h2>` + `<p>` + un enlace de llamada a la acción) y una sección de *features* con un contenedor de **al menos 3 tarjetas**, donde cada tarjeta es un `<article>` con `<h3>`, `<p>` y una `<img>` con `alt`;
   - un `<footer>` con un `<p>`.
3. Estilo **mobile-first**: estilos base para móvil (nav en columna, tarjetas en una sola columna) y **una `@media (min-width: ...)`** que pase la nav a fila y las tarjetas a una rejilla de varias columnas con **Grid**.
4. Corre los tests del esqueleto:

   ```bash
   node --test
   ```

5. Itera hasta que **todos los tests pasen en verde**. Luego **ábrelo en el navegador** y achica/agranda la ventana: el layout debe reacomodarse sin romperse.

> El test verifica que la **estructura** está (landmarks, un `h1`, `alt`, viewport, grid/flex, media query, `rem`). Que se *vea bien* lo juzgan tu ojo y el corrector IA. Las dos cosas importan: pasar el test con un diseño feo no es "hecho".

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Landmarks reales (`header`, `nav`, `main`, `footer`) y **un solo `<h1>`**, con encabezados en orden (`h1` → `h2` → `h3`).
- [ ] Es **mobile-first**: estilos base + al menos una `media query` con `min-width`.
- [ ] **Grid** para la rejilla de tarjetas y **Flexbox** para una fila (la nav); puedes justificar por qué cada uno.
- [ ] Tipografía y espaciado en `rem`; `box-sizing: border-box` aplicado.
- [ ] Toda `<img>` tiene `alt`; `<html>` tiene `lang`; el `<head>` tiene `charset` y `viewport`.
- [ ] La página **se lee bien sin CSS** (prueba: comenta el `<link>` y revisa que el orden del contenido tenga sentido).
- [ ] Todos los tests pasan; entregaste `spec.md` + 1–2 líneas de decisión (por qué Grid aquí, Flexbox allá).
- [ ] Puedes **explicar tu solución sin notas** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Construye **primero el HTML completo sin estilos** y verifica que se lee de corrido (esa es la prueba de que la estructura es buena). El esqueleto: `header` (con `h1` + `nav`), `main` (con una `section` hero y una `section` de tarjetas, cada tarjeta un `article` con `h3`/`p`/`img`), y `footer`.

Recién entonces estila, en este orden: (1) el reset `box-sizing: border-box` ya está; (2) estilos **móviles** base —todo en columna, tamaños en `rem`—; (3) una `@media (min-width: 700px)` que ponga la `nav` con `display: flex; flex-direction: row` y el contenedor de tarjetas con `display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr))`. Para las imágenes de relleno puedes usar `https://placehold.co/600x400` con un `alt` descriptivo. Esto es una pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio, incluido `spec.md`),
- la **rúbrica**: `.ai/rubricas/fase-4/landing-semantica-responsive.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-4/landing-semantica-responsive/` — no la mires antes de intentarlo de verdad.
