# 1.8 A — Tipar y estrechar un módulo TypeScript

> **Modalidad: código (Primero-Sin-IA).** Un módulo de la despensa de HomeHub está escrito con `any` y sin modelar. Vas a tiparlo entero, modelar sus eventos como **unión discriminada**, estrecharlos con narrowing exhaustivo y derivar tipos con un utility type — sin dejar un solo `any`.

**Fase:** Fase 1 — Lenguajes núcleo · **Lección:** `1.8` TypeScript desde cero
**Ruta:** crítica · **Timebox:** 35–45 min

## 🎯 Objetivo

Modelar un dominio con `interface` y una **unión discriminada**, estrechar por el discriminante con `switch` + chequeo de exhaustividad (`never`), escribir un **type guard** (`x is T`) y usar un **utility type** (`Omit`), todo haciendo pasar `tsc --strict` **sin usar `any`**.

## 📋 Contexto

Esto es exactamente el lado TypeScript del **Capstone F1 — La misma app, dos lenguajes**: modelar el dominio de la despensa con tipos sólidos. La unión discriminada con exhaustividad (`never`) es el patrón que el mercado evalúa para ver si "piensas en tipos" o solo decoras JavaScript.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea feo y lento.
2. Solo entonces, consulta **documentación oficial** (TypeScript Handbook → "Narrowing").
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Instala dependencias una vez:

   ```bash
   npm install
   ```

2. Abre `inventario.ts` y completa los `TODO`. **No cambies las firmas** que importan los tests.
3. Verifica los tipos y corre los tests:

   ```bash
   npm run typecheck   # tsc --noEmit (debe reportar 0 errores)
   npm test            # vitest
   ```

4. Itera hasta que **typecheck esté en verde y todos los tests pasen**.
5. Añade al menos **un caso de prueba tuyo** en `inventario.test.ts` (un caso borde: p. ej. `add` con cantidad 0).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `npm run typecheck` reporta **0 errores** y **no queda ningún `any`** en `inventario.ts`.
- [ ] `EventoStock` es una **unión discriminada** por `kind` (`add`/`remove`/`set`).
- [ ] `aplicarEvento` estrecha por `kind` y tiene el chequeo `const _exhaustivo: never = evento` en el `default`.
- [ ] `crearProducto` recibe `Omit<Producto, "id">` (no re-declara los campos a mano).
- [ ] `esEventoSet` es un **type guard** (`evento is ...`), no un `boolean` cualquiera.
- [ ] Todos los tests pasan y agregaste al menos un caso tuyo.
- [ ] Puedes **explicar sin notas** por qué el `never` te obliga a manejar un `kind` nuevo.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

La unión: `type EventoStock = { kind: "add"; cantidad: number } | { kind: "remove"; cantidad: number } | { kind: "set"; valor: number };`. En `aplicarEvento`, un `switch (evento.kind)` con un `case` por variante; en `remove` usa `Math.max(0, stock - evento.cantidad)`; en el `default`, `const _exhaustivo: never = evento; return _exhaustivo;`. El type guard se firma `evento is Extract<EventoStock, { kind: "set" }>` y su cuerpo es `return evento.kind === "set";`. Revisa la sección 4.3–4.6 de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-1/tipar-y-estrechar-typescript.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-1/tipar-y-estrechar-typescript.md` — no la mires antes de intentarlo de verdad.
