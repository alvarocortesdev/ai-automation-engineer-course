# Ejercicio 4.10 A — Los cuatro estados de primera clase

**Fase:** Fase 4 — Frontend + UI/UX · **Lección:** `4.10` Usabilidad + estados de primera clase
**Ruta:** crítica · **Modalidad:** código (React 19 + TypeScript + Vitest) · **Timebox:** 40 min

> El error #1 del junior es programar solo el **happy path**. Este ejercicio te obliga a dibujar los
> **cuatro** estados de una vista que carga datos: **loading**, **error**, **empty** y **success**. La
> carga asíncrona ya está cableada por ti; tu trabajo es el render de las cuatro ramas, distintas y
> accesibles.

## 🎯 Objetivo

Completar el componente `BandejaTareas`, que recibe una prop `cargar: () => Promise<Tarea[]>` y debe
dibujar los cuatro estados de primera clase. Respeta la firma exportada: el corrector y los tests importan
exactamente `BandejaTareas` y el tipo `Tarea`.

## 📋 Reglas del ejercicio

`cargar()` puede terminar de tres formas, y tú debes cubrir las cuatro pantallas que resultan:

- **Mientras la promesa está pendiente → LOADING:** un indicador con `role="status"` (para que un lector
  de pantalla lo anuncie).
- **Si la promesa rechaza → ERROR:** un contenedor con `role="alert"`, un mensaje humano, y un botón
  **Reintentar** que vuelva a disparar la carga (la función `ejecutarCarga` ya está en el starter).
- **Si resuelve con `[]` → EMPTY:** un mensaje que explique que no hay tareas **y un botón (CTA)** que
  invite a crear la primera. **Sin** `<li>` y **sin** `role="alert"`.
- **Si resuelve con tareas → SUCCESS:** un `<ul>`/`<li>` con cada `titulo`, con `key` estable (`id`).

> Pista de diseño (la trampa de la lección): el **empty no es una fase de la carga**. Se chequea
> **dentro** del éxito, cuando `tareas.length === 0`. Si lo tratas como un error, mientes; si lo olvidas,
> renderizas un `<ul>` vacío (una caja en blanco).

## 📏 Primero-Sin-IA

1. Resuélvelo **solo** (timebox 40 min), sin IA. Documentación oficial permitida (React, NN/g, MDN).
2. Apóyate en el ejemplo resuelto de la sección 4.2 de la lección: tu componente tiene la misma forma.
3. **Solo al final**, usa IA para *revisar* tu solución, no para generarla.
4. Mañana, reescribe el componente **de memoria** partiendo del tipo `Estado`.

## 🛠️ Cómo correr

```bash
pnpm install
pnpm test        # corre Vitest una vez (arranca en ROJO a propósito)
pnpm test --watch
pnpm typecheck   # opcional: chequeo de tipos
```

El test verifica el **comportamiento** de los cuatro estados. No puede ver cómo modelaste el estado por
dentro (eso lo revisa el corrector con la rúbrica): el espíritu es una máquina de estados, no tres
booleanos sueltos.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `pnpm test` pasa en **verde**: las cuatro ramas cumplen.
- [ ] Los cuatro estados son **visual y semánticamente distintos** (nadie confunde vacío con error).
- [ ] **Loading anunciado** (`role="status"`) y **error anunciado** (`role="alert"`).
- [ ] **Error con salida**: botón "Reintentar" que vuelve a llamar a la carga.
- [ ] **Empty accionable**: mensaje + CTA (un `<button>`), no una caja en blanco.
- [ ] El empty se chequea **dentro** del éxito (`tareas.length === 0`), no como fase de carga.
- [ ] Puedes **explicar tu solución sin notas** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

El starter ya te da `estado` (unión `cargando | error | listo`) y la función `ejecutarCarga`. Tu render es
un `switch (estado.fase)` (o cadena de `if`):

1. `cargando` → algo con `role="status"` (un texto "Cargando…" o un skeleton).
2. `error` → `<div role="alert">` con `estado.mensaje` + `<button type="button" onClick={ejecutarCarga}>Reintentar</button>`.
3. `listo` → **primero** `if (estado.tareas.length === 0)` devuelve el vacío con un `<button>` de CTA;
   **si no**, el `<ul>` con `.map` y `key={t.id}`.

El error típico es saltarte el `length === 0` y caer en el `<ul>` vacío. Corre el test entre cada rama.
Esto es una pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-4/estados-de-primera-clase/` usando el framework de `.ai/`. Sigue
> `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará si los cuatro estados están y si los modelaste con criterio (máquina de estados,
empty dentro del éxito), no solo si el test pasa. La **solución de referencia** vive en
`.ai/soluciones/fase-4/estados-de-primera-clase.md` — no la mires antes de intentarlo de verdad.
