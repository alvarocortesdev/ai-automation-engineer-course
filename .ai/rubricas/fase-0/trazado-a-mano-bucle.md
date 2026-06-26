---
ejercicio_id: fase-0/trazado-a-mano-bucle
fase: fase-0
sub_unidad: "0.3"
version: 1
---

# Rúbrica — Trazado a mano de un bucle anidado

> Rúbrica analítica para un ejercicio **a-mano**. Lo que se evalúa es el **proceso de razonamiento** (la tabla de traza), no sólo si el número final coincide. Un alumno puede acertar el número por suerte y seguir sin entender; uno puede errar el número y tener un modelo mental casi correcto. La rúbrica distingue ambos casos.

## Objetivos evaluados
- **O1** — Predecir la salida sin ejecutar.
- **O2** — Construir una tabla de traza que justifique la predicción.
- **O3** — Diagnosticar el propio error (predicción vs. ejecución).

> Resultado correcto: `misterio(4)` devuelve **10**. (El corrector lo sabe; **no se lo dice al alumno** salvo al cerrar, y nunca como atajo que evite la traza.)

## Criterios y niveles

### C1 — Corrección de la predicción · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay predicción, o se ejecutó antes de predecir (la "predicción" es la salida copiada). |
| **en-progreso** | Predice un valor con razonamiento, pero erróneo por un malentendido sistemático (p. ej. no reinicia `fila`, o cree que `range(i)` llega hasta `i`). |
| **competente** | Predice **10** con razonamiento coherente, aunque la tabla tenga lagunas menores. |
| **excelente** | Predice 10 y además anticipa los dos puntos resbalosos (reinicio de `fila`, `range(i)` = `0..i-1`) explicándolos. |

### C2 — Calidad de la tabla de traza · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay tabla, o sólo el resultado final sin pasos intermedios. |
| **en-progreso** | Tabla parcial: registra el bucle externo pero colapsa el interno (no muestra cómo crece `fila` por cada `j`), o salta iteraciones. |
| **competente** | Tabla completa con columnas `i`, `j`, `fila`, `total` y una fila por paso relevante; los valores intermedios cuadran con la predicción. |
| **excelente** | Además marca explícitamente el momento de reinicio de `fila` en cada vuelta del externo y el estado de `total` al final de cada `i`. |

### C3 — Diagnóstico del propio error (metacognición) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No ejecutó para verificar, o no hay `reflexion.md`. |
| **en-progreso** | Verificó, pero la reflexión es superficial ("me equivoqué en un número") sin nombrar la idea de fondo. |
| **competente** | Nombra con precisión la idea equivocada (o por qué acertó) y la liga a la línea del código. |
| **excelente** | Convierte el error en una regla reutilizable ("cada vez que veo un acumulador dentro de un bucle, primero pregunto dónde se reinicia"). |

## Errores típicos a marcar
- **No reiniciar `fila`** mentalmente: arrastra la suma del externo anterior → predice un número mayor (típico: 0,1,4,10 mal sumados).
- **Off-by-one en `range(i)`**: creer que `j` llega hasta `i` (incluye un término de más) o que `range(1, n+1)` excluye `n`.
- **Traza sólo del externo**: registrar `total` por cada `i` sin desglosar el crecimiento de `fila`. Oculta justo dónde está el riesgo de error.
- **Resultado sin proceso**: el número correcto pero sin tabla → no demuestra el objetivo (ver señales de dependencia-IA).
- **Ejecutar antes de predecir**: invalida O1 aunque el resto esté impecable.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- `prediccion.md` con el valor correcto pero **sin tabla de traza** o con una tabla que no podría haber producido ese razonamiento (resultado sin proceso).
- Reflexión genérica que no menciona ni `fila` ni `range`, como si no hubiera trazado el código concreto.
- Vocabulario o formato muy por encima del nivel F0 sin poder explicarlo.
- **Verificación sugerida:** pedir que prediga, sin ejecutar, `misterio(5)` o una variante donde el inner sea `range(1, i+1)`. Si trazó de verdad, lo resuelve; si dependió de la IA, se traba.

## Feedback sugerido (graduado)
> Nunca dar el número ni la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Tu tabla pierde el rastro de `fila` cuando el bucle externo avanza. Mira qué valor tiene `fila` justo al **empezar** la segunda vuelta del externo."
- **Pregunta socrática (nivel 2):** "¿En qué línea exactamente vuelve `fila` a cero? ¿Ocurre una vez, o una vez por cada `i`? ¿Cómo lo sabes sin ejecutar?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "El patrón a corregir es el **reinicio del acumulador interno**: `fila = 0` está dentro del bucle externo, así que ocurre en cada `i`. Reescribe la traza marcando ese reinicio y vuelve a predecir antes de ejecutar."

## Conexión con el proyecto / capstone
- Trazar a mano es el músculo que sostiene el **Capstone F0 — CLI sin IA**: depurar el CLI sin debugger exige predecir qué hace tu propio código. Es también exactamente lo que mide un live coding (T0.3).
