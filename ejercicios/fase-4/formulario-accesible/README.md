# Ejercicio 4.4 — Haz accesible un formulario y deja el test de a11y en verde

> **Modalidad: mixto (código + criterio).** Una parte se verifica con un test automatizado
> (un *linter de a11y* con jsdom: la parte objetiva). El foco visible y la prueba con lector de
> pantalla se evalúan con la rúbrica (la parte de criterio). Resuélvelo **Primero-Sin-IA**.

**Fase:** Fase 4 — Frontend + UI/UX · **Lección:** `4.4` Accesibilidad WCAG 2.2
**Ruta:** crítica · **Timebox:** 40–45 min

## 🎯 Objetivo

- **O1** — Hacer la tarjeta **operable solo con teclado** (orden de foco lógico, foco visible, sin
  trampas) usando HTML semántico.
- **O2** — Usar **ARIA solo donde el HTML no llega** (error con `role="alert"` + `aria-describedby`),
  aplicando la Primera Regla de ARIA.
- **O3** — Hacer accesible el **formulario** (labels asociados, error anunciado, contraste AA, `alt`
  correcto) y mapear cada arreglo a su **SC de WCAG 2.2**.

## 📋 Contexto

Esta es una tarjeta de "aprobar acción detectada por IA": el tipo de componente que vas a construir en el
**Capstone F4**. Funciona con mouse, pero es **inaccesible**: `<div>` que deberían ser landmarks y
encabezados, un "botón" que es un `<div onclick>` con `tabindex` positivo, campos sin `<label>`, una
imagen sin `alt`, y un error suelto que no se anuncia. El test arranca en **rojo** a propósito. Lo que
arregles aquí es, literalmente, el **a11y gate** del Definition of Done de todo capstone con UI.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Documentación oficial permitida (WCAG 2.2, MDN, WAI-ARIA).
2. **Prueba de verdad con teclado**: abre `formulario.html` en el navegador, guarda el mouse y navega con
   `Tab` / `Shift+Tab` / `Enter` / `Space`. Si no llegas al botón y lo activas, todavía falta.
3. **Solo al final**, usa IA para *revisar y explicar* tus decisiones — no para *generar* el HTML.
4. Mañana, **reescribe el formulario de memoria** partiendo de HTML semántico. Si no recuerdas qué llevaba
   ARIA y qué no, no internalizaste la Primera Regla.

## 🛠️ Instrucciones

1. Edita `formulario.html` y `estilos.css`. **No** renombres los archivos (el test lee `formulario.html`).
2. Arregla por **capas**, no en desorden:
   - **Semántica:** `<div>` → `<main>`, `<h1>`, `<button>`, `<label>`. La mitad del test pasa solo con esto.
   - **Teclado:** quita el `tabindex` positivo; añade `:focus-visible` en el CSS (nunca `outline: none` a secas).
   - **ARIA quirúrgica:** el error con `id` + `role="alert"`, y el campo apuntándolo con `aria-describedby`.
   - **Formulario y alt:** label asociado por `for`/`id` en cada campo; `alt` correcto en la imagen
     (decorativa → `alt=""`).
3. Corre el test:

   ```bash
   pnpm install   # solo la primera vez (instala vitest + jsdom)
   pnpm test
   ```

4. Itera hasta que **los siete chequeos pasen en verde**.
5. Escribe un `decisiones.md` corto (5–8 líneas) que **mapee cada arreglo a su SC de WCAG 2.2**.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] El **test de a11y pasa en verde** (los siete chequeos cumplen).
- [ ] La interfaz es **operable solo con teclado**: orden de foco lógico hasta el botón, activable con
      `Enter`/`Space`, sin trampas de foco.
- [ ] El **foco es visible** (`:focus-visible` con contraste ≥ 3:1), no `outline: none` sin reemplazo.
- [ ] **ARIA solo donde el HTML no llega** (`role="alert"` + `aria-describedby`); el `<button>` y los
      landmarks **sin** ARIA redundante.
- [ ] `decisiones.md` **mapea cada arreglo a su SC** (p. ej. "label asociado → SC 1.3.1; foco visible →
      SC 2.4.7; error anunciado → SC 4.1.3").
- [ ] Puedes **explicar tu solución sin notas** (check de dominio): por qué un `<div onclick>` no basta y
      cuándo ARIA sí hace falta.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Empieza por la **semántica**: cambia los `<div>` por `<main>`, `<h1>`, `<button>` y `<label>`. Verás que
varios chequeos pasan solos, porque el HTML correcto **ya es accesible** (rol + nombre + teclado gratis).
Para el error: ponle un `id`, un `role="alert"`, y conéctalo desde el campo con `aria-describedby="ese-id"`.
La imagen del check es decorativa (el texto ya lo dice) → `alt=""`. En el CSS, reemplaza cualquier
`outline: none` por `:focus-visible` con un anillo que contraste. Corre el test entre capa y capa para ver
qué falta. Revisa la sección 4 de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio, con el test en verde y `decisiones.md`),
- la **rúbrica**: `.ai/rubricas/fase-4/formulario-accesible.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-4/formulario-accesible.md` — no la mires antes
de intentarlo de verdad.
