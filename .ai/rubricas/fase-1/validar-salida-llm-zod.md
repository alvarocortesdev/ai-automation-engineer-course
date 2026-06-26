---
ejercicio_id: fase-1/validar-salida-llm-zod
fase: fase-1
sub_unidad: "1.8"
version: 1
---

# Rúbrica — Validar la salida de un LLM con zod

> Rúbrica **analítica** atada a los `objetivos` del contrato. Es el espejo TypeScript del ejercicio de pydantic (`1.4`): se evalúa si el alumno **valida en la frontera** un dato no confiable (la salida de un LLM) con un schema correcto, infiere el tipo desde el schema, y entiende por qué `z.strictObject` y la coacción importan. Tests verdes es el piso; el techo es defender las decisiones.

## Objetivos evaluados
- **O1** — Diseñar un schema zod v4 (`z.strictObject` + constraints) que tipe y valide datos externos.
- **O2** — Validar en la frontera la salida de un LLM: coacción (`z.coerce`), rechazo de campos alucinados (`strictObject`), `enum` de moneda y manejo de error.
- **O3** — Inferir el tipo `Compra` con `z.infer` en vez de duplicarlo a mano.

## Criterios y niveles

### C1 — Corrección del schema (¿valida y rechaza lo correcto?) · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | El schema no compila o casi nada pasa/rechaza; faltan campos; los tests fallan. |
| **en-progreso** | Valida el caso feliz y algunos rechazos, pero **uno o más** fallan: típicamente no rechaza campos extra (usó `z.object`) o no rechaza strings de solo espacios. |
| **competente** | Pasan los 8 tests: coacciona `monto`, rechaza monto ≤ 0, espacios, `items` vacío, moneda desconocida, fecha no-ISO y **campos alucinados** (`z.strictObject`). |
| **excelente** | Además modela `categoria` o `moneda` de forma más estricta justificada, o usa `z.iso.date()` y explica por qué un `z.string()` suelto no bastaba. |

### C2 — Inferencia de tipo y manejo de error · mapea: O3, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Escribe el tipo `Compra` a mano (`interface`/`type` duplicado) en vez de `z.infer`. |
| **en-progreso** | Usa `z.infer`, pero `parsearCompra` valida en dos pasos descoordinados o silencia el error (try/catch que devuelve algo). |
| **competente** | `type Compra = z.infer<typeof CompraSchema>`; `parsearCompra` hace `CompraSchema.parse(JSON.parse(raw))` y **deja propagar** el error en caso inválido. |
| **excelente** | Comenta la diferencia `parse` (lanza) vs `safeParse` (devuelve unión discriminada) y por qué eligió `parse` aquí. |

### C3 — Comprensión de seguridad de IA (hilo transversal) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No agregó test propio; no distingue "validar en la frontera" de "tipar". |
| **en-progreso** | Test propio trivial; entiende la coacción pero no por qué `strictObject` es de seguridad. |
| **competente** | Test propio realista (p. ej. monto `"12.990"` con separador, o item vacío en la lista); explica que confiar en la salida del LLM sin validar es el riesgo. |
| **excelente** | Nombra el principio (OWASP LLM05, *Improper Output Handling*) y explica por qué `as Compra` no habría servido (no comprueba en runtime). |

## Errores típicos a marcar
- **`z.object` en vez de `z.strictObject`**: pasa todo menos el test de campos alucinados; el LLM puede colar `"confianza": 0.99` en silencio. Es el corazón del hilo de seguridad.
- **Creer que `.min(1)` cubre los espacios**: `"   "` tiene largo 3 y pasa `min(1)`. Falta `.trim()` antes del `.min(1)`.
- **Sintaxis zod v3**: `.strict()`, `z.string().email()`, `z.string().date()`, `z.nativeEnum`. Deprecadas/movidas en v4 (`z.strictObject`, `z.email()`, `z.iso.date()`, `z.enum`). Mucho tutorial e IA están en v3.
- **Tipo `Compra` escrito a mano** en vez de `z.infer`: duplica la fuente de verdad; si el schema cambia, el tipo miente.
- **No coaccionar `monto`**: usar `z.number()` (rechaza el string `"12990"`) en vez de `z.coerce.number()`.
- **`parsearCompra` que captura y silencia el `ZodError`**: devolver `null`/`{}` esconde el fallo; el ejercicio pide que un dato inválido **reviente** (o se maneje explícito).
- **`monto: z.coerce.number()` sin `.int()`**: deja pasar `12.99`; el caso borde del separador de miles lo expone.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Schema correcto pero con APIs mezcladas v3/v4 que el alumno no puede explicar (señal de copia de respuesta de IA desactualizada).
- Usa `safeParse` con un manejo elaborado que no calza con la firma `parsearCompra(): Compra` (sobre-ingeniería sin entender el contrato).
- No sabe responder por qué `z.object` dejaría pasar el campo alucinado.
- **Verificación sugerida:** pídele que, sin ejecutar, prediga qué hace su schema con `{ ...valido, monto: "12.990" }` y con `{ ...valido, extra: 1 }`. Si diseñó de verdad, lo sabe; si dependió de la IA, duda.

## Feedback sugerido (graduado)
> Nunca pegar la solución. Pistas de menos a más directas.
- **Pista (nivel 1):** "Tu schema valida bien casi todo, pero deja pasar un campo que el LLM inventó. ¿Qué hace `z.object` por defecto con las claves que no declaraste?"
- **Pregunta socrática (nivel 2):** "Si el modelo te devuelve `comercio: '   '`, ¿tu `min(1)` lo rechaza? ¿Cuántos caracteres tiene esa cadena? ¿Qué necesitarías correr **antes** de medir el largo?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Dos cambios: (1) usa `z.strictObject({...})` en vez de `z.object` para que un campo extra sea un error —ese es el patrón de seguridad con salidas de LLM—; (2) `z.string().trim().min(1)` para que `'   '` se recorte a `''` y falle. No toques los demás campos."

## Conexión con el proyecto / capstone
- Validar la salida del LLM con zod es el lado TypeScript del **Capstone F1**: la misma frontera que en Python defiendes con pydantic. Es la base directa de `6.4` (structured outputs) y del capstone de IA de F6, donde "validar antes de usar" es ship-gate, no opción.
