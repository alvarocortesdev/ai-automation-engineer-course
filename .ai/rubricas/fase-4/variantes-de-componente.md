---
ejercicio_id: fase-4/variantes-de-componente
fase: fase-4
sub_unidad: "4.9"
version: 1
---

# Rúbrica — Motor de variantes (mini-cva)

> Rúbrica analítica para un ejercicio de **código** con tests. El corrector verifica que los tests
> pasen, lee `variants.ts`, y sobre todo evalúa que el alumno **entienda** qué construyó y qué añade
> el `cva` real. No es la nota: es un mapa de qué observar.

## Objetivos evaluados
- **O1** — Implementar el mapeo de props a clases (base + variants + defaultVariants) con orden, fallback y limpieza correctos.
- **O2** — Explicar cómo este motor hace consistente un componente y qué añade el `cva` real sobre la versión mínima.

## Criterios y niveles

### C1 — Corrección del motor (¿hace lo que el objetivo pide?) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Tests en rojo; falta la base, ignora `defaultVariants`, o no devuelve una función (no es factory). |
| **en-progreso** | Pasa los casos simples pero falla alguno: no respeta el orden de ejes, no hace fallback ante opción inexistente, o deja espacios dobles/`undefined`. |
| **competente** | Todos los tests verdes: base primero, defaults aplicados, override por props, orden de declaración, fallback robusto y string limpio. |
| **excelente** | Además tipa con generics (deriva claves de ejes) o implementa `compoundVariants` bien, sin romper lo mínimo; código claro y sin ramas muertas. |

### C2 — Calidad de ingeniería (tests reales, clean code) · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No agregó test propio, o el test propio no asegura nada (no tiene aserción real). |
| **en-progreso** | Agregó un test pero trivial (repite un caso ya cubierto). |
| **competente** | Test propio que cubre un caso borde nuevo (tres ejes, default a opción inexistente, clave que no es eje); código legible. |
| **excelente** | Test que documenta una decisión de diseño (p. ej. qué pasa con un eje sin default) y nombres/estructura que se explican solos. |

### C3 — Comprensión demostrada (el write-up/explicación calza con el código) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No puede explicar por qué su motor hace consistente al componente, o su explicación no calza con el código. |
| **en-progreso** | Explica el "qué" (concatena clases) pero no el "por qué" (consistencia vía props tipadas → clases-token fijas). |
| **competente** | Explica que el motor reemplaza clases improvisadas por una fuente única, y nombra al menos una cosa que añade el `cva` real. |
| **excelente** | Distingue con precisión su motor del `cva` real: `compoundVariants`, `VariantProps`, y `tailwind-merge` (vía `cn`) para resolver conflictos de clases. |

## Errores típicos a marcar
- `join(" ")` sin `filter(Boolean)` → doble espacio o `undefined` colado (lo atrapan los tests de limpieza y `ghost`).
- Fallback solo para `undefined` con `??`, pero no para una opción inexistente (`size: "xl"` no cae a default).
- Ordenar los ejes alfabéticamente en vez de respetar el orden de declaración.
- Olvidar la base o ponerla al final.
- Sobre-ingeniería prematura (intentar `tailwind-merge` o `compoundVariants` y romper lo mínimo).
- (transversal) test propio sin aserción real o que persigue "cubrir líneas" en vez de un comportamiento.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Implementación con `compoundVariants`, generics avanzados y `tailwind-merge` "de una", impecable, pero no sabe explicar el fallback simple ni por qué `filter(Boolean)`.
- Comentarios que describen una API distinta a la que el código implementa (señal de copy-paste de cva real).
- **Verificación sugerida:** pídele que prediga la salida de un caso nuevo (un eje con default que apunta a una opción inexistente) y que explique línea por línea su `for`. Si entiende, responde con el string exacto; si copió, titubea.

## Feedback sugerido (graduado)
> Nunca pegar la solución de referencia.
- **Pista (nivel 1):** "¿Tu función devuelve una función? `variants(config)` se llama una vez; lo que retorna se llama en cada render. Y mira qué pasa cuando una clase es `''` o `undefined` antes de unir."
- **Pregunta socrática (nivel 2):** "Si paso `size: 'xl'` y `xl` no existe en el eje, ¿qué debería pasar según el enunciado? ¿Tu código distingue 'no me pasaron la prop' de 'me pasaron algo que no existe'?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Construye un arreglo que arranque con la base, recorre `Object.keys(config.variants)` en orden, por cada eje elige `props[eje]` y si no sirve usa `defaultVariants[eje]`, empuja la clase si existe, y cierra con `filter(Boolean).join(' ')`."

## Conexión con el proyecto / capstone
- Este motor es lo que hay debajo del `Button` de shadcn que usarías en el [Capstone F4](/fase-4-frontend/proyecto/). Entenderlo evita el cargo cult de `npx shadcn add` y te permite editar/extender tus componentes con criterio.
