# Ejercicio 4.1 — Especificidad y box model a mano

> **Modalidad: a mano (sin navegador, sin IA).** Este ejercicio entrena tu modelo mental del motor de CSS: cómo el navegador decide **qué regla gana** (cascada + especificidad) y **cuánto mide una caja** (box model). Si predices el resultado antes de abrir las DevTools, estás pensando como el navegador. Si necesitas abrirlas para saber qué pasa, todavía no.

**Fase:** Fase 4 — Frontend + UI/UX · **Lección:** `4.1` HTML semántico + CSS
**Ruta:** crítica · **Timebox:** 25–35 min

## Objetivos

- **O1** — Predecir el **color final** de cada elemento aplicando especificidad `(a,b,c)` y, solo ante empate, el orden de origen.
- **O2** — Calcular el **ancho total** de una caja bajo `content-box` y bajo `border-box`.
- **O3** — Diagnosticar tu propio error contrastando predicción vs. lo que muestran las DevTools.

## El código a trazar

```html
<main id="contenido">
  <article class="post">
    <h2 class="titulo">Embeddings</h2>
    <p class="intro">Primer párrafo, con clase intro.</p>
    <p>Segundo párrafo, sin clase.</p>
  </article>
</main>
```

```css
*, *::before, *::after { box-sizing: border-box; }

p            { color: black; }
article p    { color: navy; }
.intro       { color: teal; }
.post p      { color: orange; }
main .intro  { color: green; }

.post {
  width: 600px;
  padding: 24px;
  border: 2px solid gray;
  margin: 0 auto;
}
```

## Tu tarea (en este orden — Primero-Sin-IA, sin abrir el navegador)

1. **Tabla de especificidad.** Para cada uno de los cinco selectores de `color`, escribe su terna `(a, b, c)` (a = ids, b = clases/atributos/pseudo-clases, c = tipos/pseudo-elementos).
2. **Predice el color** del **primer** `<p>` (el de clase `intro`) y del **segundo** `<p>` (sin clase). Justifica cuál regla gana y por qué. Ojo: en uno de los dos hay un **empate de especificidad** que se resuelve por orden — detéctalo.
3. **Box model.** El `.post` tiene `width: 600px`. Con el `box-sizing: border-box` de arriba, ¿cuánto mide su **ancho total** en pantalla? ¿Y si **borraras** esa línea de `box-sizing` (volviendo al `content-box` por defecto)?
4. **Solo después**, pega el código en un archivo `.html`, ábrelo y usa las DevTools (inspecciona el elemento → pestaña *Computed* / el diagrama del box model) para **verificar**.
5. **Reflexiona**: si fallaste, escribe en 2–3 frases *qué idea* tenías equivocada (no "me equivoqué en un color" — la idea de fondo: ¿pensaste que ganaba el último?, ¿olvidaste sumar el border?).

## Qué entregar (deja estos archivos en esta carpeta)

- `prediccion.md` — la tabla de especificidad, los dos colores predichos con su justificación, y los dos anchos (border-box y content-box). **Antes** de abrir el navegador.
- `verificacion.md` — lo que mostraron las DevTools y si coincidió con tu predicción.
- `reflexion.md` — qué idea equivocada tenías (si la hubo), o por qué acertaste.

> No abras el navegador antes de predecir. El valor del ejercicio está en **predecir primero**; si verificas antes, no entrena nada.

## Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-4/especificidad-cascada-a-mano/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará tu **proceso** (la tabla de especificidad y el cálculo del box model), no solo si acertaste los colores.
