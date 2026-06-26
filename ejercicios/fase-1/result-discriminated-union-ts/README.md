# result-discriminated-union-ts — El patrón Result con discriminated unions en TypeScript

**Fase:** Fase 1 — Lenguajes núcleo · **Lección:** `1.9` Manejo de errores idiomático comparado
**Ruta:** opcional/profundización · **Modalidad:** código · **Timebox:** 35–45 min

## 🎯 Objetivo

Implementar el patrón `Result<T, E>` con una **discriminated union** y consumirlo con **narrowing**,
de modo que el fallo quede **en el tipo de retorno** —parte del contrato— en vez de escondido en un
`throw`. Además, **domar** una API que lanza (`JSON.parse`) envolviéndola en un `Result`.

## 📋 Contexto

Es el mismo parser de gastos del ejercicio de Python, en el idioma opuesto. En TS, lo que una función
lanza **no aparece en su firma**: `parseGasto(s): Gasto` mentiría. El patrón `Result` arregla eso:
devuelves el error como valor, la firma lo declara, y el compilador obliga al llamador a discriminar
antes de tocar el `Gasto`. Es así como se escribe TS profesional para fallos esperados, y conecta con
el lado TypeScript del Capstone F1 (los handlers devuelven `Result`, nunca un `200 OK` con basura).

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, sin IA (timebox arriba). Diseña los modos de fallo **antes** de codear.
2. Solo entonces consulta el **TypeScript Handbook** (narrowing, discriminated unions) si lo necesitas.
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, reescribe `Result`, `ok`/`err` y `parseGasto` **de memoria**.

## 🛠️ Instrucciones

Los tipos (`Result`, `Gasto`, `ParseError`) ya están dados en `result.ts`: ese es el contrato.
Tu trabajo es implementar las cuatro piezas marcadas con `TODO`:

1. `ok` / `err`: los constructores del `Result` (una línea cada uno).
2. `parseGasto(linea)`: valida **sin lanzar**; devuelve `err({ tipo, mensaje })` temprano por cada
   modo de fallo (`formato` vs `monto`), o `ok({...})` al final.
3. `safeJsonParse(raw)`: envuelve `JSON.parse` en `try/catch`, estrecha `e: unknown`
   (`e instanceof Error`) y devuelve un `Result` —nunca propaga el throw—.
4. Corre los tests (sin instalar nada permanente):

   ```bash
   pnpm dlx vitest run        # o:  npx vitest run
   ```

5. **Cierra el loop.** Agrega en `result.test.ts` **un test tuyo** para un caso borde.

> Bonus de dominio (no lo piden los tests, pero hazlo): escribe un llamador que haga
> `if (r.ok) { ... } else { switch (r.error.tipo) { ... } }` con un `const _: never = r.error` en el
> `default`. Si agregas un tercer `tipo` a `ParseError` y olvidas su `case`, **no compila**.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `parseGasto` **nunca lanza**: siempre devuelve `{ ok: true, value }` o `{ ok: false, error }`.
- [ ] El `tipo` del `ParseError` es correcto: `formato` (campos/vacíos) vs `monto` (no entero o ≤ 0).
- [ ] `safeJsonParse` atrapa el throw de `JSON.parse`, estrecha `e: unknown` y devuelve un `Result`.
- [ ] Agregaste al menos un test propio.
- [ ] Puedes explicar **sin notas** por qué `Result` pone el error "en el contrato" y por qué
      `catch (e)` tipa `e` como `unknown`.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

`ok`/`err`: `({ ok: true, value })` y `({ ok: false, error })`. En `parseGasto`: `const partes =
linea.split(";").map(p => p.trim())`; si `partes.length !== 3` o algún campo es `""` => `err({ tipo:
"formato", ... })`; `const monto = Number(montoRaw)`; si `!Number.isInteger(monto) || monto <= 0` =>
`err({ tipo: "monto", ... })`; si todo bien => `ok({ comercio, monto, categoria })`. En
`safeJsonParse`: `try { return ok(JSON.parse(raw)); } catch (e) { return err(e instanceof Error ? e :
new Error(String(e))); }`. Esto es una pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio: `result.ts`, `result.test.ts`),
- la **rúbrica**: `.ai/rubricas/fase-1/result-discriminated-union-ts.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-1/result-discriminated-union-ts.md` — no
la mires antes de intentarlo de verdad.
