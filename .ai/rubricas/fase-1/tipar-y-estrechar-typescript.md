---
ejercicio_id: fase-1/tipar-y-estrechar-typescript
fase: fase-1
sub_unidad: "1.8"
version: 1
---

# Rúbrica — Tipar y estrechar un módulo TypeScript

> Rúbrica **analítica** atada a los `objetivos` del contrato. No es una nota numérica: es un mapa de qué observar y cómo dar feedback. Lo que se evalúa es si el alumno **piensa en tipos** (modela un dominio, estrecha por el discriminante, deriva tipos) o solo "decora JavaScript" con anotaciones sueltas. Tests verdes + `tsc --strict` limpio es el piso, no el techo.

## Objetivos evaluados
- **O1** — Modelar un dominio con `interface` y una **unión discriminada**, sin `any`.
- **O2** — Estrechar por el discriminante con `switch` + chequeo de exhaustividad (`never`) y escribir un **type guard** (`x is T`).
- **O3** — Aplicar un **utility type** (`Omit`) para derivar tipos sin duplicar, con `tsc --strict` en verde.

## Criterios y niveles

### C1 — Corrección (¿hace lo que el objetivo pide?) · mapea: O1, O3
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Quedan `any`; `EventoStock` no es una unión (es `any` o un solo objeto); los tests no pasan o `typecheck` falla. |
| **en-progreso** | Modela la unión y pasan los tests, pero quedó algún `any` (p. ej. en `crearProducto`), o `crearProducto` re-declara los campos a mano en vez de `Omit`. |
| **competente** | `Producto` (interface) + `EventoStock` (unión discriminada por `kind`) bien modelados, sin `any`; `crearProducto` usa `Omit<Producto, "id">`; tests verdes y `tsc --strict` limpio. |
| **excelente** | Además usa tipos literales para `categoria`, evita repetir las variantes (p. ej. `Extract<EventoStock, ...>` en el guard) y justifica `interface` vs `type` por escrito. |

### C2 — Narrowing y exhaustividad · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No estrecha: usa `if (evento.kind === ...)` con `as` para acceder a los campos, o accede a `cantidad`/`valor` sin discriminar. |
| **en-progreso** | Estrecha por `kind` y funciona, pero **falta** el chequeo de exhaustividad (`const _exhaustivo: never = evento`) en el `default`. |
| **competente** | `switch (evento.kind)` con narrowing real (sin `as`) + el chequeo `never` presente y correcto; el type guard tiene la firma `evento is ...`. |
| **excelente** | Demuestra que entiende el `never`: lo comenta, o agrega un cuarto `kind` de prueba para ver que `tsc` lo obliga a manejarlo, y luego lo quita. |

### C3 — Calidad de ingeniería (tests reales, sin `any`, sin atajos) · mapea: O1–O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No agregó test propio; o "silenció" errores con `any`/`as`/`// @ts-ignore`. |
| **en-progreso** | Test propio trivial (repite un caso existente); sin atajos pero sin caso borde nuevo. |
| **competente** | Test propio que cubre un caso borde real (p. ej. `add` con cantidad 0, o `remove` que llega justo a 0). |
| **excelente** | Tests claros y nombrados por comportamiento; cero `any`/`as`/`@ts-ignore`; el guard se usa o se prueba como predicado. |

## Errores típicos a marcar
- **`any` residual** "para que compile" — apaga justo la red que el ejercicio entrena. Es el error #1.
- **`as` para acceder a campos de la variante** (`(evento as any).cantidad`) en vez de estrechar por `kind`: pasa los tests pero anula el objetivo de narrowing.
- **Falta el chequeo `never`**: el código funciona hoy, pero no protege ante un `kind` nuevo. Marcar siempre.
- **`crearProducto` re-declara los campos** (`{ nombre: string; stock: number; ... }`) en vez de `Omit<Producto, "id">`: duplica la fuente de verdad.
- **Type guard que devuelve `boolean`** en vez de `evento is ...`: filtra en runtime pero no estrecha; el objetivo O2 no se cumple.
- **`enum` de TypeScript** para `kind`/`categoria` en vez de unión de literales: funciona, pero contradice la lección (sección 5); pedir que justifique.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Código sofisticado (conditional types, `infer`, mapped types) impropio del nivel "TypeScript desde cero", que el alumno no puede explicar.
- `never` presente pero el alumno no sabe decir **qué** pasa si se agrega un `kind` sin su `case` (no entiende para qué está).
- Comentarios o nombres en inglés mezclados con un estilo que no calza con el resto del repo.
- **Verificación sugerida:** pídele que agregue en vivo un `{ kind: "scrap"; motivo: string }` a la unión y prediga, **sin compilar**, dónde fallará `tsc`. Si modeló de verdad, dice "en el `never` del default"; si dependió de la IA, se traba.

## Feedback sugerido (graduado)
> Nunca pegar la solución. Pistas de menos a más directas.
- **Pista (nivel 1):** "¿Qué tipo tiene `evento` dentro de `case "set"`? Si necesitas un `as` para leer `valor`, tu unión no está discriminando — revisa que cada variante tenga el campo `kind` con un literal distinto."
- **Pregunta socrática (nivel 2):** "Si mañana agregas un `kind` nuevo y olvidas su `case`, ¿qué quieres que pase: que el bug aparezca en runtime, o que `tsc` te avise? ¿Qué línea haría eso?"
- **Dirección concreta (nivel 3, solo tras intento real):** "El patrón a cerrar es la **exhaustividad**: en el `default`, `const _exhaustivo: never = evento; return _exhaustivo;`. Cuando todos los `kind` están manejados, `evento` es `never` ahí y compila; si falta uno, no lo es y `tsc` falla en esa línea. Sin eso, tu `switch` es frágil."

## Conexión con el proyecto / capstone
- Modelar el dominio con uniones discriminadas y exhaustividad es el lado TypeScript del **Capstone F1 — La misma app, dos lenguajes**: procesar eventos de stock de la despensa sin que un caso nuevo se cuele sin manejar. Es también lo que un live coding (T0.3) usa para distinguir a quien "piensa en tipos" de quien decora JS.
