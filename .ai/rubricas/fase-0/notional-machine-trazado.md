---
ejercicio_id: fase-0/notional-machine-trazado
fase: fase-0
sub_unidad: "0.3"
version: 1
---

# Rúbrica — Traza una inversión in-place con aliasing

> Rúbrica analítica para un ejercicio **a-mano**. Lo que se evalúa es el **proceso de razonamiento** (la tabla de estado y el modelo "nombres → objetos"), no solo si las tres líneas coinciden. Un alumno puede acertar las líneas por suerte y seguir sin entender el aliasing; otro puede errar una línea y tener un modelo casi correcto. La rúbrica distingue ambos casos.

## Objetivos evaluados
- **O1** — Predecir la salida exacta sin ejecutar.
- **O2** — Construir una tabla de estado que justifique la predicción.
- **O3** — Explicar, con "nombres → objetos", por qué `original is resultado` da `True`.

> Resultado correcto (el corrector lo sabe; **no se lo da al alumno** salvo al cerrar, y nunca como atajo que evite la traza):
> ```
> [1, 2, 8, 5]
> [1, 2, 8, 5]
> True
> ```

## Criterios y niveles

### C1 — Corrección de la predicción · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No hay predicción, o se ejecutó antes de predecir (la "predicción" es la salida copiada). |
| **en-progreso** | Predice con razonamiento pero falla por un malentendido sistemático: invierte mal el swap, o cree que `copia`/`resultado` son listas distintas y predice `is` → `False`. |
| **competente** | Predice las tres líneas correctas con razonamiento coherente, aunque la tabla tenga lagunas menores. |
| **excelente** | Predice las tres y además anticipa las dos trampas (mutación in-place visible por `original`, identidad por aliasing) explicándolas antes de ejecutar. |

### C2 — Calidad de la tabla de estado · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay tabla, o solo el resultado final sin pasos intermedios. |
| **en-progreso** | Tabla parcial: registra `izquierda`/`derecha` pero no muestra el contenido de `xs` tras cada swap, o salta la vuelta donde el bucle termina. |
| **competente** | Tabla con columnas `izquierda`, `derecha` y contenido de `xs` por vuelta; los valores cuadran con la predicción y se ve por qué el `while` para (`izquierda < derecha` deja de cumplirse). |
| **excelente** | Además marca explícitamente la condición de parada y nota que `xs` y `original` son el mismo objeto durante toda la traza. |

### C3 — Comprensión del modelo "nombres → objetos" (metacognición) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No ejecutó para verificar, o no hay `reflexion.md`. |
| **en-progreso** | Verificó, pero la reflexión es superficial ("me equivoqué en el `is`") sin nombrar el aliasing ni la mutación in-place. |
| **competente** | Nombra con precisión por qué `is` da `True`: un solo objeto lista, dos (o tres) nombres apuntándolo. |
| **excelente** | Convierte el error en regla reutilizable ("cuando una función muta su argumento in-place y lo retorna, el retorno es el mismo objeto: `=` nunca copió nada"). |

## Errores típicos a marcar
- **`is` → `False`**: creer que `copia = original` o que `return xs` crean una lista nueva. Es el error central; sin entender aliasing, falla.
- **Swap mal trazado**: confundir el orden del intercambio `xs[izquierda], xs[derecha] = xs[derecha], xs[izquierda]` y predecir una lista mal invertida.
- **Bucle que no termina / termina tarde**: no notar que `izquierda` y `derecha` convergen y el `while` para cuando se cruzan (con 4 elementos hace 2 swaps; con índices 1 y 2 la condición ya no se cumple).
- **`original` no cambia**: predecir que `original` sigue `[5, 8, 2, 1]` porque "no se tocó" — ignora que `reordenar(copia)` mutó el objeto compartido.
- **Ejecutar antes de predecir**: invalida O1 aunque el resto esté impecable.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- `prediccion.md` con las tres líneas correctas pero **sin tabla de estado**, o con una tabla que no podría haber producido ese razonamiento (resultado sin proceso).
- `reflexion.md` que no menciona ni *aliasing* ni *in-place*, como si no se hubiera trazado el código concreto.
- Vocabulario muy por encima del nivel F0 (habla de `id()`, refcounting, CPython) sin poder explicar el caso simple.
- **Verificación sugerida:** pedir que prediga, sin ejecutar, una variante donde `reordenar` haga `xs = xs[::-1]` (que **reasigna** el nombre local en vez de mutar). Si entendió el modelo, ve que ahí `original` **no** cambia y el `is` daría `False`. Si dependió de la IA, se traba.

## Feedback sugerido (graduado)
> Nunca dar las líneas ni la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Cuenta cuántos objetos lista existen en todo el programa. Si tu respuesta no es 'uno', vuelve a leer la línea `copia = original`."
- **Pregunta socrática (nivel 2):** "Cuando `reordenar` hace el swap, ¿crea una lista nueva o cambia la que recibió? ¿Y `return xs` devuelve cuál objeto? ¿Cómo lo sabes sin ejecutar?"
- **Dirección concreta (nivel 3, solo tras intento real):** "El patrón a corregir es **aliasing + mutación in-place**: `=` mueve etiquetas, no copia objetos; el swap muta el objeto compartido. Reescribe la traza marcando que `xs`, `original`, `copia` y `resultado` son el mismo objeto, y vuelve a predecir el `is`."

## Conexión con el proyecto / capstone
- Entender aliasing y mutación in-place es lo que evita el bug silencioso #1 al construir el **Capstone F0 — CLI sin IA**: pasar una lista a una función, mutarla sin querer, y "perder" datos que creías intactos. Es también exactamente lo que mide un live coding sobre estructuras mutables.
