# Ejercicio 4.3 — Rediseña una tarjeta de IA: jerarquía, escala y contraste AA

> **Modalidad: mixto (código + criterio).** El contraste de color se verifica con un test
> automatizado (parte objetiva). La jerarquía, el espaciado y la tipografía se evalúan con la
> rúbrica y el *squint test* (parte de criterio). Resuélvelo **Primero-Sin-IA**.

**Fase:** Fase 4 — Frontend + UI/UX · **Lección:** `4.3` Fundamentos de diseño visual
**Ruta:** crítica · **Timebox:** 40–45 min

## 🎯 Objetivo

- **O1** — Rediseñar el componente con **jerarquía visual** (tamaño + peso + contraste): tres niveles
  distinguibles con el squint test.
- **O2** — Aplicar una **escala de espaciado** consistente y una **escala tipográfica**, agrupando por
  proximidad (menos espacio intra-grupo, más inter-grupo).
- **O3** — Dejar una **paleta con roles** (`--color-*`) que cumpla **WCAG 2.2 AA** (texto 4.5:1, UI 3:1),
  verificada con el test.

## 📋 Contexto

Esta es una tarjeta de "acción detectada por IA": el tipo de componente que vas a construir en el
**Capstone F4**. Funciona, pero se ve amateur (sin jerarquía, espacios arbitrarios, paleta que no pasa
contraste). El test arranca en **rojo** a propósito: tu trabajo es dejarlo en verde *y* que la tarjeta
se lea como un producto. El contraste que arregles aquí es, literalmente, un criterio del gate de
accesibilidad de la lección 4.4 (Accesibilidad WCAG 2.2).

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Documentación oficial permitida (MDN, WCAG, WebAIM).
2. Para el contraste, **no adivines**: usa una herramienta (WebAIM Contrast Checker o el panel de
   DevTools) para verificar tus pares de color.
3. **Solo al final**, usa IA para *revisar y explicar* tus decisiones — no para *generar* el diseño.
4. Mañana, **reescribe el CSS de memoria** partiendo de tus escalas. Si no te sale, no lo aprendiste.

## 🛠️ Instrucciones

1. Edita `index.html` y `estilos.css`. Puedes cambiar el HTML y el CSS como necesites, pero mantén la
   paleta en **custom properties `--color-*` dentro de `:root`** en `estilos.css` (es la fuente de
   verdad que lee el test).
2. Define los **cinco tokens de color** con estos nombres exactos (el test los busca):
   - `--color-fondo` — fondo de la tarjeta.
   - `--color-texto` — texto de cuerpo principal.
   - `--color-texto-tenue` — metadata secundaria.
   - `--color-acento` — color de la acción principal (fondo del botón).
   - `--color-texto-sobre-acento` — texto encima del acento (label del botón).
3. Corre el test de contraste:

   ```bash
   pnpm install   # solo la primera vez
   pnpm test
   ```

4. Itera hasta que **todos los tests pasen en verde**.
5. Abre `index.html` en el navegador y aplica el *squint test*: ¿se distinguen tres niveles de jerarquía?
6. Escribe un `decisiones.md` corto (4–6 líneas) justificando tus escalas y tu paleta.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] El **test de contraste pasa en verde** (los cuatro pares cumplen su umbral AA).
- [ ] Hay **tres niveles de jerarquía** distinguibles con el squint test (título / cuerpo / metadata),
      construidos con tamaño + peso + contraste.
- [ ] El espaciado usa una **escala consistente** (no números arbitrarios como 10px o 7px) y agrupa por
      proximidad.
- [ ] La tipografía usa una **escala de máximo tres tamaños** con `line-height` adecuado (cuerpo ~1.5) y
      longitud de línea controlada (`max-width` en `ch`).
- [ ] `decisiones.md` justifica **por qué** elegiste tus tamaños, tu base de espaciado y tus colores
      (incluyendo cómo verificaste el contraste).
- [ ] Puedes **explicar tu solución sin notas** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Trabaja una palanca a la vez: (1) define la escala de espaciado base-4 y la tipográfica como custom
properties **antes** de tocar el layout; (2) decide qué es lo más importante y asígnale el tamaño mayor +
bold; baja deliberadamente el volumen de la metadata (pequeña + tenue). (3) Para el contraste, empieza por
un texto casi-negro sobre fondo casi-blanco (pasa siempre); luego **oscurece el acento** hasta que el
texto blanco encima dé ≥ 4.5:1. El gris "tenue" bájalo solo hasta que siga pasando 4.5:1 (alrededor de
`#767676` sobre blanco es el límite). Revisa la sección 4 de la lección antes de mirar la solución de
referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio, con el test en verde y `decisiones.md`),
- la **rúbrica**: `.ai/rubricas/fase-4/jerarquia-y-contraste-tarjeta.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-4/jerarquia-y-contraste-tarjeta.md` — no la
mires antes de intentarlo de verdad.
