# 2.6 — Suite Vitest para un validador (it.each + vi.fn) con pnpm

**Fase:** Fase 2 — Ingeniería de software · **Lección:** `2.6` Testing: fundamentos
**Ruta:** crítica · **Timebox:** 30 min · **Modalidad:** código

## 🎯 Objetivo

Escribir una **suite Vitest** para un validador/normalizador de emails en
TypeScript, usando `it.each` (la versión Vitest de `parametrize`) para una tabla
de casos válidos e inválidos, y `vi.fn()` para mockear la **frontera** (el
`logger` inyectado en `registrar`). Demostrar que mockeas la frontera, no la
lógica pura. Es el mismo músculo del ejercicio de pytest, en el stack JS/TS.

## 📋 Contexto

`solucion.ts` es el **SUT** y está correcto. `normalizarEmail` y `esEmailValido`
son lógica pura; `registrar` usa un `logger` inyectado que en producción escribiría
a un servicio de observabilidad: esa es la **frontera**. Aprender a testear el lado
JS con Vitest es indispensable para los capstones de frontend (Fase 4) y para
cualquier proyecto fullstack.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Decide cada `esperado` **leyendo
   el SUT** (recuerda: normaliza con trim + lowercase **antes** de validar).
2. Solo entonces, consulta la [guía oficial de Vitest](https://vitest.dev/guide/).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescríbela de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

> ⚠️ **Usa pnpm, nunca npm.** Es la regla del curso para todo proyecto JS/TS.

1. Instala dependencias (una sola vez) y corre la suite:

   ```bash
   pnpm install
   pnpm test
   ```

2. Abre `solucion.test.ts` y completa los `TODO`. **No modifiques `solucion.ts`.**
3. Itera hasta tener **verde**. Vitest descubre `*.test.ts` solo; no necesitas
   configuración extra.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `pnpm test` pasa **verde** (no modificaste el SUT).
- [ ] El `it.each` cubre **≥3 válidos y ≥3 inválidos**, con bordes (espacios,
      mayúsculas, `a@b` sin punto, dominio que termina en punto, parte local vacía).
- [ ] Hay una aserción `toHaveBeenCalled` (o `toHaveBeenCalledWith`) y otra
      `not.toHaveBeenCalled` sobre el `logger` mockeado.
- [ ] No mockeaste `esEmailValido` ni `normalizarEmail` (lógica pura).
- [ ] Puedes explicar **sin notas** cuál es la frontera y por qué el `logger` se
      mockea pero el validador no.

## 📦 Qué entregar (deja estos archivos en esta carpeta)

- `solucion.test.ts` — tu suite, verde con `pnpm test`.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

El validador normaliza (trim + lowercase) **antes** de validar, así que
`" A@B.COM "` es válido y `registrar` debe devolver `"a@b.com"`. Inválidos típicos:
`"sin-arroba"` (no hay `@`), `"@dominio.com"` (parte local vacía), `"a@b"` (dominio
sin punto), `"a@b."` (dominio termina en punto). Para `it.each` con objetos:

```ts
it.each([{ entrada: " A@B.com ", esperado: true }])(
  "$entrada -> $esperado",
  ({ entrada, esperado }) => expect(esEmailValido(entrada)).toBe(esperado),
);
```

El `logger` es la frontera: `const logger = { warn: vi.fn() }` y luego
`expect(logger.warn).not.toHaveBeenCalled()` (caso válido) o
`expect(logger.warn).toHaveBeenCalled()` (caso inválido). Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio, **incluido `solucion.test.ts`**),
- la **rúbrica**: `.ai/rubricas/fase-2/vitest-suite-validador.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-2/vitest-suite-validador.md`
— no la mires antes de intentarlo de verdad.
