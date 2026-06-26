---
ejercicio_id: fase-0/leer-stack-traces
fase: fase-0
sub_unidad: "0.8"
version: 1
---

# Rúbrica — Lee el stack trace (a mano)

> Rúbrica analítica para un ejercicio **a-mano**. Lo que se evalúa es el **método de lectura** (de abajo
> hacia arriba; camino vs causa; causa raíz anclada al dato), no que el alumno memorice los mensajes. Se
> diagnostica **antes** de ejecutar; ejecutar después es verificación, no atajo.

## Objetivos evaluados
- **O1** — Leer un traceback de abajo hacia arriba: tipo de error, mensaje y frame donde reventó.
- **O2** — Distinguir el frame culpable (el de más abajo) del camino de llamadas (los de arriba).
- **O3** — Razonar la causa raíz en términos del dato de entrada y proponer un fix mínimo dirigido.

> Resultados correctos: caso 1 = `KeyError: 'precio'` (clave `"valor"` mal escrita); caso 2 = `TypeError`
> al sumar `int + "3000"`; caso 3 = `ZeroDivisionError` por `reporte([])` (lista vacía). El corrector lo
> sabe; **no se lo dice al alumno** salvo al cerrar, y nunca como atajo que evite el diagnóstico.

## Criterios y niveles

### C1 — Lectura del error (tipo + mensaje + dirección) · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `diagnostico.md`, o copia el mensaje sin explicarlo / lee de arriba hacia abajo. |
| **en-progreso** | Acierta uno o dos tipos; explica el mensaje a medias; no menciona la dirección de lectura. |
| **competente** | Los **tres** tipos correctos, cada mensaje explicado con sus palabras. |
| **excelente** | Además nombra explícitamente "de abajo hacia arriba / `most recent call last`" y usa los marcadores `^^^`/`~~~` para ubicar la sub-expresión que falló. |

### C2 — Frame culpable vs camino · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Señala el frame de arriba (`<module>`) como culpable, o no identifica frames. |
| **en-progreso** | Acierta el culpable en los casos de 2 frames pero se confunde en el caso 3 (3 frames). |
| **competente** | Identifica el frame de **más abajo** (línea exacta) como culpable en los tres, incluido el caso 3. |
| **excelente** | En el caso 3 nombra los tres frames como cadena `<module>` → `reporte` → `promedio` y explica por qué el de más abajo es la causa y los otros el camino. |

### C3 — Causa raíz (dato) + fix mínimo (metacognición) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | "El código está mal", sin nombrar el dato; fix al azar o ausente. |
| **en-progreso** | Causa raíz parcial (señala la línea pero no el dato concreto); fix genérico no dirigido. |
| **competente** | Cada causa raíz apunta al **dato** (clave `"valor"`, el `str "3000"`, la lista vacía) y el fix es mínimo y dirigido a ese dato. |
| **excelente** | El fix apunta al **origen del dato** (validar/convertir en la entrada), no sólo un parche local, y verificó ejecutando después de predecir. |

## Errores típicos a marcar
- **Leer de arriba hacia abajo:** señalar el frame de `<module>` como el culpable. Es el error #1.
- **Confundir camino con causa** en el caso 3: creer que `reporte` o `print` causaron el `ZeroDivisionError`.
- **Causa raíz sin dato:** "falta algo" en vez de "la lista llegó vacía" / "la clave dice `valor`".
- **Fix al azar** (envolver todo en `try/except` que esconde el error) en vez de validar/convertir el dato.
- **Ejecutar antes de diagnosticar:** invalida el Primero-Sin-IA aunque el resultado sea correcto.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Diagnóstico impecable y exhaustivo pero sin ningún rastro de razonamiento propio (ni una duda, ni una
  corrección tras ejecutar), redactado como salida de modelo.
- Usa terminología precisa de tracebacks que no puede explicar si se le pregunta de otra forma.
- **Verificación sugerida:** pedir que prediga, **sin ejecutar**, qué pasa si `caso3.py` se llama con
  `reporte([7])` (no falla → imprime `7.0`) o que diagnostique un `IndexError` nuevo. Si leyó de verdad,
  lo resuelve; si dependió de la IA, se traba.

## Feedback sugerido (graduado)
> Nunca dar el diagnóstico completo antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Vuelve a la primera línea del traceback: dice `most recent call last`. ¿En qué
  dirección lo estás leyendo? ¿Cuál de los frames es el más reciente?"
- **Pregunta socrática (nivel 2):** "En el caso 3 hay tres frames. ¿Cuál ejecutó la línea que reventó, y
  cuáles sólo lo llamaron? ¿Qué **dato** entró por `reporte(...)` para que `len(...)` diera 0?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "La causa raíz siempre se nombra en términos
  del dato: en el caso 1 es la clave `"valor"` del segundo item; en el 2, el `str "3000"`; en el 3, la
  lista vacía. Reescribe cada fix apuntando a **ese** dato en su origen, no a un parche que tape el error."

## Conexión con el proyecto / capstone
- Leer tracebacks es la habilidad que sostiene la depuración del **Capstone F0 — CLI sin IA**: sin
  debugger mágico, cuando tu propio CLI falle, el traceback que tú provocaste es el mapa para arreglarlo.
  Es exactamente lo que un *live coding* (T0.3) mide cuando tu código se cae frente a la cámara.
