---
ejercicio_id: fase-2/dsa-analisis-big-o
fase: fase-2
sub_unidad: "2.1"
version: 1
---

# Rúbrica — Defiende la complejidad: auditoría Big-O

> Rúbrica **analítica** para un ejercicio **a-mano**. Se evalúa el **razonamiento**, no si las letras O
> coinciden por suerte. Un alumno puede acertar "O(n²)" sin saber por qué, y otro puede errar una letra
> con un modelo casi correcto. La rúbrica distingue ambos: lo que importa es que **nombre el patrón
> dominante** y pueda defenderlo.

## Objetivos evaluados
- **O1** — Estimar tiempo y espacio Big-O de un fragmento por intuición, identificando el patrón dominante.
- **O2** — Distinguir O(n), O(n²), O(log n) y O(1) reconociéndolos en código ajeno.
- **O3** — Justificar una elección de estructura (`list` vs `set`) con Big-O y órdenes de magnitud.

> Respuestas de referencia (el corrector las sabe; **no se las da al alumno** salvo al cerrar, y nunca como atajo que evite el razonamiento):
> - **A**: tiempo O(n), espacio O(1) — un solo bucle, acumulador.
> - **B**: tiempo O(n²), espacio O(n²) en el peor caso (la lista `pares` puede tener hasta n² tuplas) — bucle anidado.
> - **C**: tiempo O(log n), espacio O(1) — búsqueda binaria, parte por la mitad.
> - **D**: tiempo O(n), espacio O(n) — construir `set(nums)` recorre y guarda hasta n elementos.
> - **Decisión**: `set`. `list` = O(n)×10.000 ≈ 10¹⁰ operaciones; `set` = O(1)×10.000 ≈ 10⁴. Diferencia de ~un millón de veces.

## Criterios y niveles

### C1 — Corrección del análisis de tiempo · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Faltan fragmentos, o las complejidades son arbitrarias sin razonamiento. |
| **en-progreso** | Acierta algunas pero falla un patrón clave: marca B como O(n) (no ve el bucle anidado) o C como O(n) (no ve la división por mitades). |
| **competente** | Las cuatro complejidades de tiempo correctas, cada una con el patrón dominante nombrado. |
| **excelente** | Además nota el matiz: B tiene espacio O(n²) por la lista de salida (no solo tiempo), y D esconde su costo dentro de `set(...)`. |

### C2 — Análisis de espacio · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No analiza espacio, o lo confunde con tiempo. |
| **en-progreso** | Da espacio para algunos pero asume que B y D son O(1) (ignora la lista/`set` que crecen con la entrada). |
| **competente** | Espacio correcto para los cuatro: A y C son O(1) extra; B hasta O(n²); D es O(n). |
| **excelente** | Explica que el espacio "extra" se mide aparte de la entrada, y razona el peor caso de B (cuántas tuplas puede acumular `pares`). |

### C3 — Decisión justificada con magnitud · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No decide, o decide "set porque es más rápido" sin números. |
| **en-progreso** | Elige `set` por la complejidad correcta pero no pone los órdenes de magnitud (10¹⁰ vs 10⁴). |
| **competente** | Elige `set`, justifica con O(n) vs O(1) por consulta × 10.000 consultas, y da el orden de magnitud. |
| **excelente** | Menciona el costo de construir el `set` una vez (O(n) ≈ 10⁶) y por qué se amortiza ante 10.000 consultas; reconoce cuándo `list` bastaría (pocas consultas). |

## Errores típicos a marcar
- **B como O(n)**: no ver que dos bucles `range(len(nums))` anidados dan O(n²).
- **C como O(n)**: no reconocer que descartar la mitad cada vuelta es O(log n) (y olvidar que exige lista ordenada).
- **D como O(1)**: creer que `len(set(nums))` es gratis; construir el `set` es O(n) tiempo y O(n) espacio.
- **Espacio de B como O(1)**: ignorar que `pares` puede crecer a O(n²).
- **Decisión sin números**: "el set es más rápido" sin cuantificar el factor (~10⁶×).

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Complejidades correctas pero patrones dominantes ausentes o genéricos ("es eficiente"), como si copiara la respuesta sin derivarla.
- Notación impecable (Θ, Ω, análisis amortizado formal) impropia del nivel F2, sin poder explicar por qué B es cuadrático en una frase simple.
- La decisión final repite "O(1) vs O(n)" pero no aterriza los números 10⁴ vs 10¹⁰.
- **Verificación sugerida:** pedir que analice un quinto fragmento nuevo en el momento (p. ej. un bucle que dentro hace `x in lista`). Quien razona ve el O(n²) escondido; quien dependió de la IA no lo deriva solo.

## Feedback sugerido (graduado)
> Nunca dar las respuestas antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Para cada fragmento, cuenta los bucles y de qué depende cada uno. En B, ¿cuántas veces se ejecuta la línea del `if`? En C, ¿qué le pasa al rango `lo..hi` en cada vuelta?"
- **Pregunta socrática (nivel 2):** "En D no ves bucles, pero `set(nums)` hace uno por dentro: ¿cuánto cuesta construir un conjunto de `n` elementos, en tiempo y en memoria? Y para la decisión: ¿cuántas operaciones son 10.000 consultas si cada una recorre un millón de elementos?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Revisa la chuleta de patrones de la sección 4.4: bucle anidado = O(n²), partir por la mitad = O(log n), construir/lookup en `set` = O(n)/O(1). Reescribe el análisis nombrando el patrón de cada fragmento y pon los números 10⁴ vs 10¹⁰ en la decisión."

## Conexión con el proyecto / capstone
- Esta auditoría es el músculo que usarás al escribir los ADRs del **Capstone F2**: "elegí esta estructura porque la operación dominante pasa de O(n) a O(1)". Defender una complejidad por escrito y en voz alta es lo que el live coding y la revisión de diseño evalúan.
