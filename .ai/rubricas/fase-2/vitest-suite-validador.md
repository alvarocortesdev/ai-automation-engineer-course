---
ejercicio_id: fase-2/vitest-suite-validador
fase: fase-2
sub_unidad: "2.6"
version: 1
---

# Rúbrica — Suite Vitest para un validador

> Rúbrica **analítica** atada a los `objetivos`. Es el espejo del ejercicio de
> pytest en el stack JS/TS: mide si el alumno transfiere la misma disciplina
> (tabla de casos + mock en la frontera) a Vitest, corrido con **pnpm**. El SUT
> (`solucion.ts`) es la verdad; si lo modificó, la evaluación se invalida.

## Objetivos evaluados
- **O1** — Implementar `it.each` con casos válidos e inválidos, incluyendo bordes.
- **O2** — Mockear la frontera (`logger`) con `vi.fn()` y afirmar la interacción, sin mockear la lógica pura.
- **O3** — Correr con pnpm y afirmar el valor de retorno de `registrar`.

## Criterios y niveles

### C1 — Tabla de casos con it.each (incluye bordes) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No usa `it.each` (copia/pega `it` por caso), o cubre <3 válidos/<3 inválidos. |
| **en-progreso** | Usa `it.each` pero sin bordes (no prueba espacios alrededor, mayúsculas, `a@b` sin punto, dominio terminado en punto, parte local vacía). |
| **competente** | `it.each` con ≥3 válidos y ≥3 inválidos, incluyendo al menos tres de los bordes; los `esperado` son correctos (entiende que normaliza antes de validar). |
| **excelente** | Cubre todos los bordes y nombra los casos legiblemente (`"$entrada -> $esperado"`); incluye un caso que demuestra la normalización (`" A@B.COM "` → válido). |

### C2 — Mock en la frontera (logger), no en la lógica · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Mockea `esEmailValido`/`normalizarEmail` (lógica pura), o no testea `registrar`, o no usa `vi.fn()`. |
| **en-progreso** | Usa `vi.fn()` para el logger pero solo cubre un camino (afirma que avisó, pero no el `not.toHaveBeenCalled` del camino válido, o viceversa). |
| **competente** | `registrar` se testea con `{ warn: vi.fn() }`; afirma `toHaveBeenCalled`/`toHaveBeenCalledWith` en el camino inválido y `not.toHaveBeenCalled` en el válido; no mockea la lógica pura. |
| **excelente** | Además afirma el **valor de retorno** en ambos caminos (email normalizado vs. `null`) y entiende por qué el logger es la frontera (escribiría a observabilidad en prod). |

### C3 — Ejecución con pnpm · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No corre, o el alumno usó `npm` en vez de `pnpm`. |
| **en-progreso** | Corre pero con warnings/casos rotos sin resolver. |
| **competente** | `pnpm test` pasa **verde** sobre la suite escrita. |
| **excelente** | Suite verde, rápida y legible; sin tests muertos ni asserts redundantes. |

## Errores típicos a marcar
- **Olvidar la normalización**: marcar `" A@B.com "` como inválido porque "tiene espacios/mayúsculas" — el SUT hace trim + lowercase **antes** de validar.
- **Mockear la lógica pura** (`esEmailValido`): sobre-mockeo; deja sin probar el comportamiento real.
- **No cubrir el camino feliz del logger** (`not.toHaveBeenCalled`): se pierde la garantía de que un email válido NO genera ruido de warning.
- **Usar `npm`** en vez de `pnpm` (regla del curso).
- **Comparar con `toEqual` cuando basta `toBe`** para primitivos (no es error grave, pero delata copy/paste).
- (transversal observabilidad) no entender que `logger.warn` es una salida observable que en prod alimenta logs/trazas: por eso se afirma la interacción.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Suite con `vi.mock('./solucion')` (automock del módulo entero) que el ejercicio no necesita y que delata una receta pegada en vez de mock-en-frontera.
- Casos correctísimos pero el alumno no sabe por qué `" A@B.COM "` es válido (no internalizó la normalización).
- No distingue `it.each` (parametrize) de `vi.fn()` (mock) si se le pregunta el equivalente en pytest.
- **Verificación sugerida:** pedir que prediga el resultado de `registrar(" A@B.com ", logger)` y diga, sin correr, si `logger.warn` se llamó.

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Revisa qué hace `normalizarEmail` ANTES de validar. ¿Sigue siendo inválido un email con espacios y mayúsculas?"
- **Pregunta socrática (nivel 2):** "¿Cuál de las tres funciones del SUT cruza una frontera? Esa es la única que reemplazas por un doble. ¿Por qué las otras dos no?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Usa `it.each` con una lista de objetos `{ entrada, esperado }` y cubre los cinco bordes. Para `registrar`, pasa `{ warn: vi.fn() }` y afirma `toHaveBeenCalled` (inválido) y `not.toHaveBeenCalled` (válido), más el retorno. Repasa la sección 4.5 antes de mirar la referencia."

## Conexión con el proyecto / capstone
- El testing del lado JS/TS que practicas aquí es el que usarás en los capstones de frontend (Fase 4) y en cualquier proyecto fullstack; la regla de mock-en-frontera es idéntica a la del lado Python, así que esto consolida el hilo transversal de testing en ambos stacks.
