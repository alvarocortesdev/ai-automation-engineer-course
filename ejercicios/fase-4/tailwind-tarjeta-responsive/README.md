# Ejercicio 4.2 — Tarjeta responsive con estados y dark mode (utility-first)

**Fase:** Fase 4 — Frontend + UI/UX · **Lección:** `4.2` Tailwind CSS
**Ruta:** crítica · **Modalidad:** código · **Timebox:** 30–40 min

## 🎯 Objetivo

Construir una **tarjeta de producto** usando **únicamente clases de utilidad de Tailwind** —sin CSS propio, sin `style=` inline, sin `@apply`—, con layout flex/grid, espaciado desde la escala, un estado `hover:`, responsive (`sm:`/`md:`/`lg:`) y dark mode (`dark:`).

## 📋 Contexto

Esta tarjeta es el patrón base de cada panel y cada burbuja de mensaje del **Capstone F4** (frontend de una app de IA). Si la dominas con utilidades —sin caer en estilos inline ni en CSS suelto— tienes el músculo central de la capa visual de tu portafolio.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea feo y lento.
2. Solo entonces, consulta la **documentación oficial** de Tailwind (responsive, states, dark mode). No adivines nombres de clases: búscalos.
3. **Solo al final**, usa IA para *revisar y explicar* —no para *generar* el marcado.
4. Mañana, **reconstruye la tarjeta de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `tarjeta.html`. El Tailwind de navegador (CDN) y un **toggle de tema** ya vienen listos: tú solo escribes el marcado y las clases.
2. Escribe tu tarjeta **entre los comentarios marcadores** `TU TARJETA: empieza` y `TU TARJETA: termina` (no los borres: el test los usa para encontrar tu código).
3. **Ábrela en el navegador** (doble clic en el archivo) para verla. El CDN compila en vivo: no necesitas instalar nada para ver el resultado. Usa el botón "Cambiar tema" para probar el dark mode.
4. La tarjeta debe incluir: un bloque de imagen o color arriba, un **título**, una **descripción**, un **precio** y un **botón**.
5. Para **validar el método** (que de verdad usaste utility-first), corre el test:

   ```bash
   pnpm install
   pnpm test
   ```

6. Itera hasta que **todos los tests pasen en verde**.

> El test **no** mide que se vea bonita (eso lo trabajas en [4.3 Diseño visual](/fase-4-frontend/4-3-diseno-visual/)): mide que el **método** sea correcto —utilidades, escala, variantes responsive/estado/dark, y cero CSS propio—.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Layout con **flex o grid** y espaciado **desde la escala** (`gap-*`, `p-*`, `m-*`); nada de números mágicos.
- [ ] **Responsive**: al menos un prefijo `sm:`/`md:`/`lg:` cambia disposición o tamaños (mobile-first: el base es móvil).
- [ ] **Estado**: el botón (o la tarjeta) reacciona con `hover:`.
- [ ] **Dark mode**: al menos el fondo y el texto se adaptan con `dark:`.
- [ ] **Cero CSS propio**: ningún `style="..."` inline y ningún `@apply`.
- [ ] Todos los tests pasan y puedes **explicar sin notas** por qué `md:p-8` no afecta al móvil.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Empieza por el contenedor: `<article class="flex flex-col gap-4 rounded-lg bg-white p-6 shadow-sm ...">`. Cada hijo con sus utilidades de texto (`text-lg`, `font-semibold`, `text-gray-600`). Para responsive, elige **una** cosa que cambie desde `md:` (de columna a fila con `md:flex-row`, o más padding con `md:p-8`). Para dark mode, por cada color base agrega su gemela `dark:` (`bg-white` → `dark:bg-gray-800`, `text-gray-900` → `dark:text-white`). Para el hover del botón: `hover:bg-indigo-700`. Si dudas de un nombre, búscalo en la documentación oficial. Esto es una pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-4/tailwind-tarjeta-responsive/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-4/tailwind-tarjeta-responsive.md` — no la mires antes de intentarlo de verdad.
