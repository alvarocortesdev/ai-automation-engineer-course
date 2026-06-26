---
ejercicio_id: fase-2/clean-code-refactor-nombres-funciones
fase: fase-2
sub_unidad: "2.2"
version: 1
---

# Rúbrica — Refactor: nombres con intención + funciones pequeñas

> Rúbrica analítica atada a los `objetivos` del contrato. **Clave:** los tests verdes solo
> garantizan que el comportamiento se preservó. La CALIDAD (nombres, descomposición) no la mide
> pytest; la mides tú leyendo el código. Un alumno puede dejar los tests verdes y el código casi
> tan ilegible como estaba.

## Objetivos evaluados
- **O1** — Renombrar variables/funciones para revelar intención, sin índices ni números mágicos, sin cambiar el comportamiento.
- **O2** — Descomponer la función en piezas con una sola responsabilidad, cada una nombrada por lo que hace.
- **O3 (transversal/testing)** — Mantener los tests en verde durante todo el refactor (red de seguridad).

> Resultado esperado (el corrector lo sabe; NO se lo entrega al alumno): nombres del dominio
> (`lineas`, `total`, `linea`), tupla desempaquetada en `producto, precio, cantidad, activo`,
> constantes `UMBRAL_DESCUENTO_VOLUMEN`/`TASA_DESCUENTO_VOLUMEN`, y al menos dos funciones
> (`subtotal_de_lineas_activas`, `con_descuento_por_volumen`) orquestadas por `total_pedido`.

## Criterios y niveles

### C1 — Nombres que revelan intención · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Sigue habiendo nombres de una letra (`d`, `r`, `i`) o se mantienen los índices mágicos (`linea[1]`, `linea[3]`). |
| **en-progreso** | Renombró algunas variables pero quedó al menos un índice mágico o un `== True`, o nombres genéricos (`data`, `temp`, `valor`) que no son del dominio. |
| **competente** | Todas las variables tienen nombre del dominio; la tupla está desempaquetada; no hay índices mágicos ni `== True`. |
| **excelente** | Además, los nombres se leen como una frase y la intención de cada uno es evidente sin leer el cuerpo; usó `sum(... for ...)` con nombres claros. |

### C2 — Una función, una responsabilidad · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Todo sigue en una sola función que filtra, suma y aplica descuento. |
| **en-progreso** | Extrajo algo, pero la división es arbitraria (parte por líneas, no por responsabilidad) o las funciones extraídas tienen nombres pobres. |
| **competente** | Separó "sumar líneas activas" de "aplicar descuento por volumen"; `total_pedido` orquesta; cada función hace una cosa nombrada. |
| **excelente** | Puede justificar la división en términos de "razones para cambiar" y NO cayó en partir de más (extraer triviales de una sola línea sin ganancia de legibilidad). |

### C3 — Números mágicos y constantes · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `100000` y `0.1` siguen incrustados como literales. |
| **en-progreso** | Subió uno de los dos a constante, o usó constantes con nombres poco descriptivos (`X`, `LIMITE`). |
| **competente** | Ambos literales están en constantes con nombre claro (`UMBRAL_DESCUENTO_VOLUMEN`, `TASA_DESCUENTO_VOLUMEN`). |
| **excelente** | Además usa `100_000` legible y comenta brevemente la unidad/significado donde aporta. |

### C4 — Comportamiento preservado bajo tests · mapea: O3 (testing)
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Algún test quedó rojo, o cambió la firma pública `total_pedido(lineas)`. |
| **en-progreso** | Tests verdes al final, pero hay señales de que cambió comportamiento y "ajustó" un test, o no agregó test propio. |
| **competente** | Todos los tests verdes, firma intacta, y un test borde propio razonable. |
| **excelente** | El test propio cubre un borde real (precio/cantidad 0, todas inactivas) y el alumno describe que corrió los tests entre pasos. |

## Errores típicos a marcar
- Dejar índices mágicos (`linea[1] * linea[2]`) "porque ya funciona": es justo lo que el ejercicio ataca.
- Cambiar la firma pública o el formato de entrada (romper los tests) creyendo que "se ve mejor".
- Partir de más: extraer una función de una línea usada una sola vez que solo agrega un salto mental (viola KISS; ver lección 4.4 y el último `:::caution`).
- Constantes con nombres tan crípticos como los literales que reemplazan (`A = 100000`).
- Comentar lo que el nombre ya dice (`total += precio  # suma el precio`).
- (transversal/testing) no correr los tests entre pasos y descubrir el rojo al final sin saber qué paso lo causó.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Refactor "perfecto" e idiomático pero el alumno no puede explicar **por qué** desempaquetar la tupla es mejor que los índices, ni qué problema evita.
- Introduce una `dataclass` o `NamedTuple` impecable que no calza con el nivel ni con el resto de su código y no sabe defender.
- **Verificación sugerida:** pídele que, sin ejecutar, prediga qué pasaría si insertara un campo nuevo al inicio de la tupla en la versión original con índices vs. en su versión desempaquetada. Si entiende el refactor, explica por qué los índices mágicos son frágiles.

## Feedback sugerido (graduado)
> Nunca pegar la solución de referencia ni el código completo.
- **Pista (nivel 1):** "Lee tu `total_pedido` en voz alta. ¿En qué punto tuviste que parar a recordar 'qué había en `linea[2]`'? Ahí hay un nombre que falta."
- **Pregunta socrática (nivel 2):** "Si el negocio cambiara mañana SOLO la regla del descuento, ¿cuántas funciones tuyas tendrías que tocar? ¿Y si cambiara solo qué líneas se suman? Si la respuesta a ambas es 'la misma función', ¿cuántas responsabilidades tiene?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Desempaqueta la tupla en `producto, precio, cantidad, activo` para eliminar los índices; sube `100000` y `0.1` a constantes con nombre; y separa la suma del descuento en dos funciones que `total_pedido` llame. No te doy el código."

## Conexión con el proyecto / capstone
- Este es, en miniatura, el trabajo del **Capstone F2 (Refactor + suite de tests)**: mejorar la legibilidad archivo por archivo manteniendo la suite verde. El reflejo de "correr los tests entre pasos" es el prerrequisito que [2.7 TDD](/fase-2-ingenieria/2-7-tdd-obligatorio/) formaliza.
