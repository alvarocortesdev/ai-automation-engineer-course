---
ejercicio_id: fase-2/tdd-sumador-de-texto
fase: fase-2
sub_unidad: "2.7"
version: 1
---

# Rúbrica — Sumador de texto (kata de TDD desde cero)

> Rúbrica **analítica** atada a los `objetivos`. Aquí el producto NO es solo la función
> correcta: es la **evidencia de proceso** (la `bitacora.md`) de que el alumno escribió el
> test antes del código y vio el rojo en cada ciclo. Una `solucion.py` perfecta sin bitácora
> de ciclos —o con bitácora que delata test-after— NO es "excelente". Evaluar `bitacora.md`,
> `test_solucion.py` y `solucion.py` juntos.

## Objetivos evaluados
- **O1** — Seguir red-green-refactor estricto: test rojo antes del código, mínimo para el verde, refactor en verde.
- **O2** — Traducir la lista de comportamientos en tests, uno a uno, dejando que cada test conduzca el diseño (fake it + triangulación).
- **O3** — Diseñar el camino de error con un test que lo exija (ValueError ante negativo), no como añadido.

## Criterios y niveles

### C1 — Corrección del comportamiento · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `acceptance_test.py` queda en **rojo**: falta algún comportamiento (típico: el `\n` no separa, o no hace `strip`). |
| **en-progreso** | Pasa la mayoría pero falla un borde (p. ej. el negativo no lanza `ValueError`, o el mensaje no incluye el número). |
| **competente** | Los 7 comportamientos pasan; `acceptance_test.py` en **verde** sin tocarlo. |
| **excelente** | Verde + la implementación no tiene código que ningún test exija (sin ramas muertas, sin "por si acaso"). |

### C2 — Disciplina de TDD (el corazón del ejercicio) · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `bitacora.md`, o un solo test gigante que prueba todo de una: no hay rastro de ciclos. |
| **en-progreso** | Bitácora presente pero sin rojos (todos los pasos arrancan en verde → huele a test-after), o tests escritos todos juntos al final. |
| **competente** | Un test por comportamiento; bitácora con `🔴`→`🟢` por ciclo, en el orden de la spec. |
| **excelente** | Además muestra **fake it** explícito (un verde con constante) y la **triangulación** que lo rompió, y al menos un **refactor** anotado (el del `\n`). |

### C3 — Camino de error y aserción · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | El negativo devuelve un número raro o revienta con otra excepción; no hay test del error. |
| **en-progreso** | Lanza `ValueError` pero el test no usa `pytest.raises` (lo "verifica" con un try/except a mano), o el mensaje no incluye el negativo. |
| **competente** | `pytest.raises(ValueError, match=...)` testea el error y el mensaje incluye el número negativo. |
| **excelente** | Maneja **varios** negativos (los reporta todos), y el test del error se escribió en **rojo primero**. |

## Errores típicos a marcar
- **Test-after disfrazado:** la `solucion.py` ya completa y luego una tanda de tests que pasan a la primera. Señal: bitácora sin rojos, o sin bitácora.
- **Saltarse la triangulación:** programar `split(",")` + `sum` "de una" en el comportamiento 2, en vez de dejar que el 3/4 lo pidan. No es un error grave, pero contradice O2; comentar.
- **`acceptance_test.py` abierto antes de tiempo** y usado como sustituto de escribir los propios tests (los tests del alumno son copias literales del acceptance).
- **El `\n` tratado como caso aparte** con un `if "\n" in numeros` en vez del refactor limpio (`replace("\n", ",")`): funciona pero pierde la lección del refactor.
- **No usar `pytest.raises`** para el caso de error (try/except artesanal).
- (transversal spec-driven) un solo commit gigante en vez de ciclos visibles; historial que no cuenta la historia.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- `solucion.py` con manejo de separadores configurables, regex sofisticado o soporte de delimitadores custom (`"//;\n1;2"`, la versión avanzada del kata) que el enunciado **no pide**: sofisticación impropia del nivel → receta pegada.
- Bitácora redactada en perfecto "lenguaje de libro" pero que no calza con el orden real del código (menciona un refactor que no aparece).
- No puede explicar **por qué** el comportamiento 4 "salió gratis", ni qué test concreto lo cubrió.
- **Verificación sugerida:** pedir que, sin ejecutar, prediga qué pasa con `sumar("1,2\n")` (coma/`\n` al final → parte vacía → `int("")` revienta) y diga si su suite lo cubre. Revela si entiende su propio split o si lo pegó.

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "¿Tu `bitacora.md` tiene un rojo por cada comportamiento? Si algún paso arrancó en verde sin código nuevo, ese test no probó nada — reescríbelo esperando el rojo."
- **Pregunta socrática (nivel 2):** "Cuando agregaste el `\n` como separador, ¿lo trataste como un caso especial o encontraste la forma de reusar tu split de una sola separación? ¿Qué transformación deja `'1\n2,3'` con una sola clase de separador?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Antes de separar, normaliza: `numeros.replace('\n', ',')`. Así tu `split(',')` cubre ambos. Para los espacios, `.strip()` cada parte antes de `int(...)`. Para el negativo, junta los `< 0` en una lista y `raise ValueError(f'...{negativos}')`. Repasa la sección 7 de la lección antes de mirar la referencia."

## Conexión con el proyecto / capstone
- Es el ensayo en pequeño del hábito que el **Capstone F2 (Refactor + suite de tests)** asume: cada feature y cada bug se atacan test-first, con el ciclo red-green-refactor visible en los Conventional Commits. La calidad de estos tests se afina en 2.8 y se mide (sin perseguir coverage) en 2.9.
