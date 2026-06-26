---
ejercicio_id: fase-2/pbt-repartir-monto
fase: fase-2
sub_unidad: "2.8"
version: 1
---

# Rúbrica — Property-based testing: caza el bug del remanente

> Rúbrica **analítica** atada a los `objetivos` del contrato. Lo central no es que `repartir_monto`
> pase los ejemplos, sino que el alumno **diseñe propiedades que afirmen invariantes reales** y entienda
> por qué una propiedad caza lo que un ejemplo no. Un alumno puede tener la función correcta y aun así
> escribir propiedades **tautológicas** (que no prueban nada) o solo ejemplos disfrazados. La rúbrica
> separa "la función anda" de "diseñó buenas propiedades".

## Objetivos evaluados
- **O1** — Escribir property-based tests con Hypothesis que afirman invariantes (suma conservada, equidad, cantidad).
- **O2** — Distinguir un test de ejemplo de una propiedad y reconocer una propiedad tautológica.
- **O3** — Explicar por qué la propiedad caza el bug del remanente que los ejemplos no, y qué es el *shrinking*.

## Criterios y niveles

### C1 — Corrección de la implementación (¿hace lo que el objetivo pide?) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `repartir_monto` no implementada, o falla los ejemplos provistos (típico: `[total // partes] * partes`, que pierde el remanente). |
| **en-progreso** | Pasa la mayoría de ejemplos pero falla un borde (no distribuye el resto, o no maneja `partes <= 0`). |
| **competente** | Pasa todos los ejemplos provistos y reparte el resto correctamente (las primeras `total % partes` partes llevan +1); lanza `ValueError` con `partes <= 0`. |
| **excelente** | Además la implementación es limpia (`divmod`, una sola expresión clara) y agregó ejemplos propios significativos. |

### C2 — Diseño de propiedades (el núcleo del ejercicio) · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `@given`, o solo repite ejemplos dentro de un `@given` sin afirmar una invariante. |
| **en-progreso** | Una o dos propiedades, o una de ellas es **tautológica** (recomputa el algoritmo en el assert: `== [base+1 if ...]`). |
| **competente** | Al menos **tres** propiedades no tautológicas (conservación de la suma, equidad `max-min<=1`, cantidad), con estrategias **acotadas** (`min_value`/`max_value`), todas verdes. |
| **excelente** | Además agregó la propiedad de no-negatividad o una metamórfica (p. ej. `repartir_monto(k*total, partes)` se relaciona con `repartir_monto(total, partes)`), y acotó las estrategias con criterio (evita overflow/tiempos absurdos). |

### C3 — Comprensión demostrada (`propiedades.md` calza con el código) · mapea: O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `propiedades.md`, o no explica qué afirma cada propiedad. |
| **en-progreso** | Describe las propiedades pero no demuestra que P1 falla contra la versión ingenua, o no menciona el shrinking. |
| **competente** | Por cada propiedad explica la invariante y el bug que atrapa; muestra que P1 falla contra `[total // partes] * partes`. |
| **excelente** | Explica el *shrinking* (Hypothesis entrega el caso mínimo, p. ej. `total=1, partes=2`) y por qué una propiedad tautológica no aporta; reconoce cuándo property-based **no** vale la pena (función trivial sin invariante clara). |

## Errores típicos a marcar
- **Propiedad tautológica:** `assert repartir_monto(t, n) == [base + 1 if i < resto else base ...]` — reimplementa la función en el assert; solo prueba que el código es igual a sí mismo, no que es correcto. Es el error conceptual central.
- **Solo ejemplos dentro de `@given`:** usar `st.sampled_from([(100,4), (101,4)])` y comparar contra valores fijos — eso es una tabla de ejemplos, no property-based testing.
- **Estrategias sin acotar:** `st.integers()` sin `max_value` para las partes → genera `partes` gigantes y el test tarda o consume memoria; o `partes` negativas que disparan el `ValueError` y "ensucian" la propiedad de suma.
- **Confundir la propiedad de equidad:** afirmar `max - min == 1` (falso cuando el reparto es exacto, ahí es 0) en vez de `<= 1`.
- (transversales) no maneja `partes <= 0`; `propiedades.md` que afirma "uso Hypothesis" sin explicar qué invariante prueba cada propiedad.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Propiedades impecables y exóticas (estrategias `@composite`, `assume()`) pero `propiedades.md` que no puede explicar **por qué** P1 falla contra la versión ingenua.
- Vocabulario sofisticado ("shrinking", "metamórfico", "stateful testing") sin poder explicar el caso simple de "ordenar dos veces == ordenar una vez".
- Las tres propiedades verdes pero ninguna es la de conservación de la suma (la que de verdad caza el bug del enunciado): señal de propiedades generadas sin entender el objetivo.
- **Verificación sugerida:** pedir que, en voz alta, prediga qué caso mínimo entregaría Hypothesis si la propiedad de suma fallara. Quien entendió dice algo como "`total=1, partes=2`"; quien dependió de la IA se traba.

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Tus ejemplos pasan. Pregúntate: ¿qué tiene que ser verdad para *cualquier* `total` y `partes`, no solo para 100/4? Esa frase, escrita como assert sin un valor esperado fijo, es tu primera propiedad."
- **Pregunta socrática (nivel 2):** "Si reemplazaras tu implementación por `[total // partes] * partes`, ¿cuál de tus propiedades se pondría roja? Si la respuesta es 'ninguna', tus propiedades no están afirmando la invariante correcta — ¿qué afirma 'no se pierde plata'?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Tu propiedad de suma debe ser `sum(repartir_monto(total, partes)) == total`, no una comparación contra una lista recomputada. Acota las estrategias (`max_value`) para que el test corra rápido. Y en `propiedades.md`, corre mentalmente la versión ingenua para mostrar que P1 falla: ahí está el valor del ejercicio."

## Conexión con el proyecto / capstone
- Las propiedades que se diseñan aquí son las que blindan la **lógica de negocio** del **Capstone F2** (cálculos de precio/descuento/reparto) contra los bordes que los ejemplos no cubren, y se miden mejor con el **mutation testing** de `2.9` que con un % de cobertura. La invariante "no se pierde plata" reaparece en cualquier sistema financiero real.
