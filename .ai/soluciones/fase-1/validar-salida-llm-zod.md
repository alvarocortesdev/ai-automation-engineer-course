---
ejercicio_id: fase-1/validar-salida-llm-zod
fase: fase-1
sub_unidad: "1.8"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Validar la salida de un LLM con zod

## Respuesta canónica

```ts
import { z } from "zod";

export const CompraSchema = z.strictObject({
  comercio: z.string().trim().min(1),
  monto: z.coerce.number().int().positive(),   // coacciona "12990" -> 12990
  moneda: z.enum(["CLP", "USD"]),
  categoria: z.string().trim().min(1),
  fecha: z.iso.date(),                          // valida "YYYY-MM-DD"
  items: z.array(z.string().trim().min(1)).min(1),
});

export type Compra = z.infer<typeof CompraSchema>;

export function parsearCompra(rawJson: string): Compra {
  return CompraSchema.parse(JSON.parse(rawJson)); // parsea JSON y valida; lanza si es inválido
}
```

Con esto pasan los 8 tests.

## Razonamiento paso a paso

1. **`z.strictObject` (no `z.object`).** Por defecto `z.object` **ignora** los campos no declarados; un LLM puede colar `"confianza": 0.99` y se cuela en silencio. `z.strictObject` convierte un campo extra en un error de validación. Es el equivalente de `ConfigDict(extra="forbid")` de pydantic y el corazón del hilo de seguridad de IA (OWASP LLM05, *Improper Output Handling*).
2. **Coacción de `monto`.** El LLM devolvió `"12990"` (string). `z.coerce.number()` lo convierte a `12990`; `.int().positive()` rechaza decimales y valores ≤ 0. `z.number()` (sin `coerce`) habría rechazado el string del caso feliz.
3. **`moneda` como `z.enum(["CLP", "USD"])`.** Restringe a dos literales; `"EUR"` falla. Es el paralelo de un `Literal` en pydantic.
4. **`fecha` como `z.iso.date()`.** API de zod v4 para validar una fecha ISO `YYYY-MM-DD`; `"ayer"` falla. (En v3 era `z.string().date()`.)
5. **Strings no vacíos ni de solo espacios.** `z.string().trim().min(1)`: `.trim()` recorta y `.min(1)` rechaza el vacío resultante, así `"   "` falla. `min(1)` solo no basta (tres espacios tienen largo 3). Mismo patrón para cada item de `items`, y `.min(1)` sobre el array exige al menos un elemento.
6. **Tipo inferido.** `z.infer<typeof CompraSchema>` deriva el tipo `Compra` del schema: una sola fuente de verdad para runtime y tipos. Escribirlo a mano lo haría mentir si el schema cambia.
7. **`parsearCompra` en un paso.** `CompraSchema.parse(JSON.parse(rawJson))`: `JSON.parse` convierte el string a un valor JS, `parse` valida y **lanza** `ZodError` si algo no cuadra. No se captura ni silencia el error: un dato inválido debe reventar (o manejarse explícito con `safeParse`, fuera del alcance de esta firma).

## Puntos resbalosos (donde el corrector debe mirar)
1. **`z.object` en lugar de `z.strictObject`** → `test "rechaza campos alucinados"` falla. Es el error #1 y el más importante de nombrar (seguridad).
2. **`.min(1)` sin `.trim()`** → `test "comercio de solo espacios"` falla.
3. **`z.number()` sin `coerce`** → el caso feliz falla (no acepta el string `"12990"`).
4. **APIs v3**: `.strict()`, `z.string().date()`, `z.string().email()`, `z.nativeEnum`. Funcionan a medias o ya no existen en v4. La v4 es la de arriba.
5. **`monto` sin `.int()`** → un test propio con `"12.990"` (separador de miles, `Number("12.990") === 12.99`) lo dejaría pasar; con `.int()` se rechaza.
6. **Tipo `Compra` escrito a mano** en vez de `z.infer`.
7. **`parsearCompra` con `try/catch` que devuelve `null`/`{}`**: esconde el fallo; rompe el contrato (debe propagar o usar `safeParse` explícito).

## Rango de soluciones aceptables
- **`monto`**: aceptar `z.coerce.number().int().positive()` o `.gt(0)`; equivalentes. `z.number().int().positive()` **no** es aceptable (rechaza el string del caso feliz).
- **Strings no vacíos**: aceptar `z.string().trim().min(1)` o un `.refine((s) => s.trim().length > 0, { error: "..." })`. Lo esencial es que `"   "` se rechace.
- **`fecha`**: aceptar `z.iso.date()` (preferido) o un `z.string().regex(/^\d{4}-\d{2}-\d{2}$/)` justificado. No aceptable: `z.string()` suelto (no rechaza `"ayer"`).
- **`moneda`**: `z.enum(["CLP", "USD"])`; aceptar `z.literal("CLP").or(z.literal("USD"))` como equivalente.
- **Rechazo de extra**: debe ser `z.strictObject` (o `z.object({...}).strict()` en v3, pero señalar que está deprecado). No aceptable resolverlo con un `.refine` que cuenta claves a mano si existe la API directa.
- **`parsearCompra`**: aceptar también `CompraSchema.parse(JSON.parse(rawJson))` partido en dos líneas, o una versión con `safeParse` que **lanza** explícitamente al fallar. No aceptable: capturar y silenciar el error.
- **Test propio**: monto con separador de miles, item vacío en la lista, campo faltante, o `monto` negativo como number — cualquiera realista cuenta para `excelente`.
