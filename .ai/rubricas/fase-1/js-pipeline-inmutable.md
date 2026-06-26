---
ejercicio_id: fase-1/js-pipeline-inmutable
fase: fase-1
sub_unidad: "1.7"
version: 1
---

# Rúbrica — Pipeline de pedidos inmutable

> Rúbrica **analítica** atada a los `objetivos`. El corazón del ejercicio NO es "saber que existe `map`",
> sino encadenar `filter`/`map`/`reduce` **sin mutar** la entrada y entender *por qué* eso importa.
> Evaluar la inmutabilidad tanto como la corrección del resultado.

## Objetivos evaluados
- **O1** — Transformar una lista con `filter`/`map`/`reduce` devolviendo datos nuevos.
- **O2** — Mantener la inmutabilidad: no mutar el array de entrada ni sus objetos.
- **O3** — Usar `reduce` con valor inicial para colapsar a un solo valor.
- **O4** — Explicar por qué la inmutabilidad evita una clase de bugs.

## Criterios y niveles

### C1 — Corrección de las transformaciones · mapea: O1, O3
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Alguna función no devuelve lo esperado; `totalRecaudado` suma también los no pagados, o falta el valor inicial de `reduce`. |
| **en-progreso** | `pagados`/`conIva` correctas pero `totalRecaudado` mal (suma todo, o usa `reduce` sin `0` y revienta en lista vacía). |
| **competente** | Las tres funciones pasan los tests: `pagados` filtra, `conIva` mapea con el campo nuevo, `totalRecaudado` reduce solo los pagados con valor inicial `0`. |
| **excelente** | Además explica por qué el valor inicial de `reduce` no es opcional (lista vacía) y por qué `filter` va antes de `reduce`. |

### C2 — Inmutabilidad · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Muta el original: `forEach` con `p.totalConIva = ...`, o `pedidos.push(...)`, o un `for` que reasigna campos. El test de no-mutación falla. |
| **en-progreso** | No muta el array pero sí los objetos (agrega el campo al objeto original en vez de copiarlo). |
| **competente** | Ninguna función toca la entrada; `conIva` usa spread (`{ ...p, totalConIva }`); el array y los objetos originales quedan intactos. |
| **excelente** | Sabe explicar que la inmutabilidad evita bugs de "alguien me cambió el objeto a mis espaldas" y que es el hábito base de React/F4. |

### C3 — Estilo idiomático (array methods, no bucles manuales) · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Bucles `for` con `.push()` a una variable externa para todo (no usa array methods). |
| **en-progreso** | Mezcla: usa `map`/`filter` en una función pero `for`+`push` en otra. |
| **competente** | Usa `filter`/`map`/`reduce` en las tres; código declarativo y legible. |
| **excelente** | Compone con claridad (encadena o separa pasos con intención); agrega un caso borde propio significativo (ningún pagado, `tasa = 0`). |

## Errores típicos a marcar
- **Mutar el original**: `forEach` que asigna `p.totalConIva = ...` o `pedidos.push(...)` — rompe la inmutabilidad aunque "el resultado se vea bien".
- **`reduce` sin valor inicial**: `reduce((a, p) => a + p.total)` revienta con `TypeError` en lista vacía; el `0` no es opcional.
- **Usar `forEach` para construir un array** empujando a una variable externa: el anti-patrón que delata no haber entendido `map`.
- **`totalRecaudado` que suma todos** (olvida filtrar por `pagado`).
- **Confundir `map` con `filter`**: devolver el mismo largo cuando se quería descartar, o viceversa.
- (transversal testing) no agregar un caso borde propio, o agregar uno trivial que no prueba nada nuevo.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Uso de utilidades avanzadas impropias del nivel (`structuredClone` dentro de la solución, `Object.freeze`, lodash, `reduceRight`) sin poder explicar por qué.
- Código perfecto pero no sabe responder "¿qué pasa si quito el `0` de `reduce`?" ni "¿por qué `conIva` no muta `p`?".
- **Verificación sugerida:** pedir que, sin ejecutar, prediga qué imprime `pedidos` después de llamar `conIva(pedidos, 0.19)`, y que explique por qué `{ ...p, ... }` no toca el objeto original.

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "El test que falla es el de **no mutación**. Algo en tu código está cambiando un objeto de entrada en vez de crear uno nuevo. ¿Dónde asignas a una propiedad de `p`?"
- **Pregunta socrática (nivel 2):** "Cuando haces `{ ...p, totalConIva: x }`, ¿estás modificando `p` o creando un objeto nuevo? ¿Y si hicieras `p.totalConIva = x`? ¿Por qué el primero conserva el original y el segundo no?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "`pagados` es un `filter`. `conIva` es un `map` que devuelve `{ ...p, totalConIva: p.total * (1 + tasa) }` — el spread copia, no muta. `totalRecaudado` es `filter` de pagados + `reduce((acc, p) => acc + p.total, 0)`. Revisa 4.3–4.4 y reintenta antes de mirar la referencia."

## Conexión con el proyecto / capstone
- Transformar listas de objetos sin mutarlas es la gramática diaria del lado JS/TS del **Capstone F1** y el hábito que hace predecible el código React de F4. El `reduce` reaparece en cualquier agregación (totales, conteos, resúmenes).
