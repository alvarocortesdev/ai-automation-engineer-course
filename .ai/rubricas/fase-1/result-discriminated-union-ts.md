---
ejercicio_id: fase-1/result-discriminated-union-ts
fase: fase-1
sub_unidad: "1.9"
version: 1
---

# Rúbrica — El patrón Result con discriminated unions en TypeScript

> Rúbrica **analítica** atada a los `objetivos` del contrato. Lo que se evalúa es que el alumno haya
> hecho del **error parte del tipo** (no un `throw` escondido) y que entienda el narrowing y el
> `catch (e: unknown)`. No basta "que los tests pasen": debe poder defender por qué `Result` cambia el
> contrato y por qué `e` no es un `Error`.

## Objetivos evaluados
- **O1** — Implementar `Result<T, E>` con una discriminated union (campo `ok`) y los helpers `ok`/`err`.
- **O2** — Devolver el error como valor (no lanzar) para que el fallo sea parte del contrato/tipo de retorno.
- **O3** — Domar una API que lanza (`JSON.parse`) envolviéndola en un `Result`, con narrowing de `catch (e: unknown)`.

## Criterios y niveles

### C1 — Corrección del Result y parseGasto · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `parseGasto` lanza en algún caso, o `ok`/`err` mal formados; varios tests fallan. |
| **en-progreso** | Devuelve `Result` pero confunde los `tipo` (`formato` vs `monto`), o acepta montos decimales/≤ 0. |
| **competente** | Pasan todos los tests: `ok`/`err` correctos, `parseGasto` nunca lanza y asigna el `tipo` correcto a cada fallo. |
| **excelente** | Agregó un test propio y escribió el llamador con `switch (error.tipo)` + chequeo de exhaustividad (`const _: never`). |

### C2 — Domar el throw (safeJsonParse + unknown) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `safeJsonParse` no atrapa el throw, o lo deja propagar; el test del JSON roto falla. |
| **en-progreso** | Atrapa el error pero asume `e: Error` sin estrechar (`e.message` directo) — bug latente si se lanza algo que no es Error. |
| **competente** | `try/catch` que estrecha `e: unknown` (`e instanceof Error`) y devuelve un `Result`; nunca propaga el throw. |
| **excelente** | Normaliza el caso no-Error (`new Error(String(e))`) y explica por qué en JS se puede lanzar cualquier valor. |

### C3 — Comprensión: el error como contrato · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No distingue `Result` de un `throw`; cree que son lo mismo con otra sintaxis. |
| **en-progreso** | Entiende que `Result` devuelve el error pero no por qué eso "obliga" al llamador. |
| **competente** | Explica que el fallo está en el tipo de retorno, así que el llamador debe discriminar `ok` antes de usar `value`. |
| **excelente** | Articula el trade-off completo (cuándo `Result` vs `throw`) y por qué un `throw` es invisible en la firma en TS (y en Python). |

## Errores típicos a marcar
- **`parseGasto` que lanza** en algún rama (rompe la promesa "nunca lanza"; el punto entero del patrón).
- **`catch (e)` asumiendo `e: Error`** (`e.message` sin `instanceof`): en strict, `e` es `unknown`.
- **Usar `value`/`error` sin narrowing** (`r.value` sin `if (r.ok)`): TS lo marca; si el alumno lo "arregla" con `as`/`!`, está apagando la red de seguridad.
- **`isNaN`/`parseInt` flojos:** `parseInt("12abc")` da `12` (acepta basura); `Number("")` da `0`. La validación correcta usa `Number(...)` + `Number.isInteger` + `> 0`.
- **Helpers sin `never`** (`ok<T>(v): Result<T, unknown>`) → fricción de tipos al asignar.
- (transversal) no agregar test propio; perseguir verde sin el chequeo de exhaustividad.

## Señales de dependencia-IA
> Describir sin acusar; proponer una verificación.
- `Result` correcto pero **incapacidad de explicar** por qué `catch` da `unknown` o qué hace el `never` en `ok`/`err`.
- Uso de una librería (`neverthrow`, `Effect`) o de `Annotated`/branding avanzado sin defensa, mientras falla el narrowing básico.
- Mezcla de `throw` y `Result` en la misma función sin criterio.
- **Verificación sugerida:** pídele que, sin ejecutar, diga qué tipo tiene `r.value` justo después de `if (r.ok)` y por qué; y qué pasa si agrega un tercer `tipo` a `ParseError` y olvida su `case`. Si lo diseñó, lo explica; si lo copió, titubea.

## Feedback sugerido (graduado)
> Nunca dar la solución completa. Primero pista, luego pregunta, luego dirección.
- **Pista (nivel 1):** "Tu `safeJsonParse` hace `e.message`, pero TS marca `e` en rojo. ¿De qué tipo es `e` dentro de un `catch` en strict? ¿Puedes usarlo sin chequear antes?"
- **Pregunta socrática (nivel 2):** "Si `parseGasto` devolviera `Gasto` y lanzara en los casos malos, ¿el compilador obligaría al llamador a manejar el fallo? ¿Y si devuelve `Result<Gasto, ParseError>`? ¿Dónde quedó el error en cada caso?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Tres piezas: (1) `ok`/`err` son objetos literales `{ ok: true, value }` / `{ ok: false, error }`; (2) en `parseGasto`, valida con `return err({ tipo, mensaje })` temprano y `return ok({...})` al final — nada de `throw`; (3) en `safeJsonParse`, `try { return ok(JSON.parse(raw)); } catch (e) { return err(e instanceof Error ? e : new Error(String(e))); }`. El `instanceof` es obligatorio porque `e` es `unknown`."

## Conexión con el proyecto / capstone
- En el **Capstone F1** (lado TypeScript) la capa de dominio devuelve `Result<T, E>` para los fallos esperados; el handler de la ruta debe discriminar antes de responder, de modo que un fallo nunca se cuele como `200 OK`. El mismo patrón (error como tipo) reaparece en zod (`safeParse` devuelve un `Result`-like) y en el frontend de la Fase 4 (estados error como ciudadanos de primera). Aquí se siembra el hábito.
