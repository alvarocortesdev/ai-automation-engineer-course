# 1.8 B — Validar la salida de un LLM con zod

> **Modalidad: código (Primero-Sin-IA).** Un LLM extrajo una compra desde el texto de un correo y devolvió un JSON. **No confíes en él.** Vas a diseñar el schema zod que lo valide en la frontera — el espejo TypeScript del ejercicio de pydantic de la lección `1.4`.

**Fase:** Fase 1 — Lenguajes núcleo · **Lección:** `1.8` TypeScript desde cero
**Ruta:** crítica · **Timebox:** 35–45 min

## 🎯 Objetivo

Diseñar un schema **zod v4** que valide datos no confiables (la salida de un LLM): tipos correctos, coacción de `monto`, moneda restringida, sin strings de solo espacios, **sin campos alucinados**, y con error claro cuando algo no cuadre. Inferir el tipo `Compra` con `z.infer` (no escribirlo a mano).

## 📋 Contexto

zod es el **pydantic de JavaScript**. Validar la salida de un LLM antes de usarla es el primer punto de la lista de seguridad de IA (OWASP LLM05, *Improper Output Handling*). Este es el lado TypeScript del **Capstone F1**: la misma validación de frontera que ya hiciste con pydantic, ahora en el otro idioma de tu stack.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Piensa el contrato (los seis campos) antes de codear.
2. Solo entonces, consulta **documentación oficial** ([zod.dev](https://zod.dev/), v4).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Instala dependencias una vez:

   ```bash
   npm install
   ```

2. Abre `compra.ts` y completa los `TODO` (`CompraSchema` y `parsearCompra`). **No cambies las firmas.**
3. Corre los tests (y, opcional, el typecheck):

   ```bash
   npm test            # vitest
   npm run typecheck   # tsc --noEmit (opcional, pero recomendado)
   ```

4. Itera hasta que **todos los tests pasen**.
5. Añade al menos **un caso de prueba tuyo** en `compra.test.ts` (un caso borde realista que un LLM podría producir).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `CompraSchema` valida un JSON correcto y **coacciona** `monto` de `"12990"` a `12990` (number).
- [ ] Rechaza: `monto` ≤ 0, `comercio`/`categoria` de solo espacios, `items` vacío, `moneda` desconocida, `fecha` no-ISO, y **campos alucinados** (extra).
- [ ] El tipo `Compra` se obtiene con `z.infer<typeof CompraSchema>`, **no** escrito a mano.
- [ ] `parsearCompra` hace `JSON.parse` + validación zod en una función.
- [ ] Agregaste al menos un test propio de un caso borde realista de un LLM.
- [ ] Puedes **explicar sin notas** por qué `z.strictObject` importa con salidas de modelos y por qué `as` no habría servido.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Usa `z.strictObject({ ... })` (no `z.object`, que ignora los campos extra). Por campo: `comercio: z.string().trim().min(1)`; `monto: z.coerce.number().int().positive()`; `moneda: z.enum(["CLP", "USD"])`; `categoria: z.string().trim().min(1)`; `fecha: z.iso.date()`; `items: z.array(z.string().trim().min(1)).min(1)`. El `.trim()` recorta espacios y `.min(1)` rechaza el vacío resultante (por eso `"   "` falla). Para parsear+validar: `return CompraSchema.parse(JSON.parse(rawJson));`. Revisa la sección 4.8 de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-1/validar-salida-llm-zod.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-1/validar-salida-llm-zod.md` — no la mires antes de intentarlo de verdad.
