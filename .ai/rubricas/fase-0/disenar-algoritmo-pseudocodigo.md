---
ejercicio_id: fase-0/disenar-algoritmo-pseudocodigo
fase: fase-0
sub_unidad: "0.2"
version: 1
---

# Rúbrica — Diseña un algoritmo preciso (y luego trázalo)

> Rúbrica analítica para un ejercicio **a-mano**. Se evalúan dos cosas distintas: que el **diseño** sea correcto *por construcción* (no por ensayo y error) y que la **traza** sea consistente con ese diseño. Un alumno puede tener un algoritmo correcto y trazarlo mal (no entendió su propio diseño), o trazar bien un algoritmo con un hueco en los casos borde. La rúbrica los separa.

## Objetivos evaluados
- **O1** — Diseñar un algoritmo en pseudocódigo sin pasos ambiguos.
- **O2** — Manejar los casos borde (carpeta vacía, empate) dentro del diseño.
- **O3** — Trazar a mano el algoritmo y obtener el resultado correcto.

> Resultado correcto de la traza de ejemplo: el algoritmo recorre la lista una vez y devuelve **`video.mp4`** (primer archivo que alcanza el máximo de 1500; ver nota de empate). El corrector lo sabe; **no se lo dice al alumno** salvo al cerrar.

## Criterios y niveles

### C1 — Diseño sin ambigüedad · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No hay pseudocódigo, o es prosa vaga ("busca el más grande") imposible de ejecutar paso a paso. |
| **en-progreso** | Hay estructura (un recorrido + una comparación) pero con ambigüedad: no se ve cómo se inicializa el "mejor", o la comparación está mal expresada. |
| **competente** | Recorre los archivos, mantiene un "mejor hasta ahora", lo actualiza con una comparación clara y devuelve el nombre. Cualquiera lo ejecutaría igual. |
| **excelente** | Diseño limpio y mínimo, con inicialización bien pensada (p. ej. "mejor empieza como el primer archivo" o "como un centinela de tamaño -1"), y nota explícita de que **una sola pasada** basta. |

### C2 — Casos borde · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Ningún caso borde manejado; el algoritmo asume que siempre hay archivos y que no hay empates. |
| **en-progreso** | Maneja uno de los dos (normalmente el de carpeta vacía) pero la regla de empate falta o es "el que sea". |
| **competente** | Carpeta vacía resuelta explícitamente (devuelve nada/None/aviso, decidido por el alumno) **y** regla de empate escrita y consistente con el diseño. |
| **excelente** | Además justifica la elección (por qué `>` y no `>=` produce "el primero gana" en empate, o viceversa), demostrando que entiende cómo la comparación determina el desempate. |

### C3 — Traza consistente · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay tabla de traza, o solo el resultado final sin pasos. |
| **en-progreso** | Tabla parcial: no muestra cómo cambia "mejor hasta ahora" en cada archivo, o salta filas. |
| **competente** | Tabla con una fila por archivo, columna "mejor hasta ahora" que evoluciona correctamente, resultado final coherente con el diseño. |
| **excelente** | La traza **expone** el comportamiento del empate (muestra que al llegar a `musica.mp3` con 1500 el "mejor" NO cambia porque `>` es estricto) y el alumno lo comenta. |

## Errores típicos a marcar
- **Ordenar para encontrar el máximo:** "ordeno la lista y tomo el último". *Funciona*, pero es más caro (ordenar es más trabajo que una pasada) y muchas veces señal de no haber pensado el patrón "mejor hasta ahora". No es incorrecto, pero el corrector debe preguntar si vio la solución de una sola pasada.
- **Inicializar "mejor" en 0 o en vacío sin pensar:** si la lista puede tener tamaños raros, o si "mejor" arranca como un archivo inexistente, la primera comparación puede fallar. El centinela o "el primer elemento" deben estar justificados.
- **Empate sin regla:** dejar "el que sea" rompe el criterio de *sin ambigüedad*: el resultado dependería del azar.
- **Confundir `>` con `>=`:** ambos son válidos, pero **cambian quién gana el empate**. Marcarlo si el alumno escribe uno pero su traza se comporta como el otro (señal de no entender su propio código).
- **Trazar primero y ajustar el diseño después:** si el algoritmo "aparece" ya perfecto justo después de la traza, sospechar que invirtió el orden (ver señales de dependencia-IA).

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Pseudocódigo idiomático de un lenguaje real (sintaxis Python/JS exacta) en un ejercicio que pedía pseudocódigo a-mano de F0 —posible copia de una solución generada.
- Traza impecable pero que **no comenta** el empate (la IA suele dar el resultado sin la observación metacognitiva que el ejercicio pide).
- Manejo de casos borde redactado en lenguaje muy técnico sin que el alumno pueda explicar la diferencia entre `>` y `>=`.
- **Verificación sugerida:** pídele que prediga, sin reejecutar, qué devuelve su algoritmo si la lista fuera `[("a", 5)]` (un solo archivo) y si fuera `[]` (vacía). Si diseñó de verdad, contesta al toque; si dependió de la IA, duda.

## Feedback sugerido (graduado)
> Nunca dar el pseudocódigo de la solución. Empujar al alumno a su propio hueco.
- **Pista (nivel 1):** "¿Qué pasa con tu algoritmo si la carpeta está vacía? Recórrelo mentalmente con una lista sin elementos y mira en qué línea se rompe o qué devuelve."
- **Pregunta socrática (nivel 2):** "Cuando dos archivos empatan en tamaño, ¿tu comparación usa `>` o `>=`? Traza esos dos casos por separado: ¿gana el primero o el último? ¿Es eso lo que querías?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Tu patrón es 'mejor hasta ahora': una variable que recuerda el máximo mientras recorres **una sola vez**. Asegúrate de tres cosas: cómo arranca 'mejor' (antes de comparar nada), la condición exacta para reemplazarlo, y qué devuelves si nunca entraste al bucle. Reescribe el pseudocódigo cubriendo esas tres y vuelve a trazar."

## Conexión con el proyecto / capstone
- Diseñar en pseudocódigo y *luego* trazar es exactamente el flujo del **Capstone F0 — CLI sin IA**: pensar el algoritmo en una servilleta antes de teclear, y verificarlo a mano cuando no hay debugger. Conecta hacia adelante con **0.3 (notional machine)**: la traza de este ejercicio es la misma habilidad que mide un live coding.
