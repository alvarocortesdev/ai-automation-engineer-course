---
ejercicio_id: fase-1/tipar-y-pasar-mypy
fase: fase-1
sub_unidad: "1.4"
version: 1
---

# Rúbrica — Tipar un módulo y hacer pasar `mypy --strict`

> Rúbrica **analítica** atada a los `objetivos` del contrato. Lo que se evalúa no es solo "mypy en
> verde", sino **por qué** quedó en verde: que el alumno entienda el error de tipo que arregló, no que
> lo silenció. Un `# type: ignore` que apaga el aviso es un suspenso conceptual aunque mypy pase.

## Objetivos evaluados
- **O1** — Anotar funciones y un acumulador local con type hints precisos (`list[dict[str, int]]`, `int | None`, `float`).
- **O2** — Hacer pasar `mypy --strict` con 0 errores, interpretando cada error reportado.
- **O3** — Diagnosticar y arreglar, vía el aviso de mypy, el bug del campo opcional (`int | None` tratado como `int`).

## Criterios y niveles

### C1 — Corrección: mypy verde + tests verdes · mapea: O1, O2, O3
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Faltan anotaciones (mypy --strict reporta errores de "missing annotation"), o algún test falla, o el módulo no corre. |
| **en-progreso** | Anotó las funciones pero quedan errores de mypy (p. ej. no anotó `suma: float`), o los tests pasan pero mypy aún se queja. |
| **competente** | `mypy --strict despensa.py` = 0 errores **y** los 4 tests pasan; tipos correctos en firmas y acumulador. |
| **excelente** | Además agregó un test propio significativo (lista vacía u otro borde) y los tipos son los más precisos posibles (no `dict` pelado ni `Any`). |

### C2 — Calidad del arreglo (el bug nace del aviso, no de un parche) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | El bug del campo opcional sigue (test del item sin descuento falla) o se "arregló" capturando la excepción a ciegas. |
| **en-progreso** | Funciona pero el arreglo es un `# type: ignore` o un `cast`/`assert` que silencia mypy sin resolver la causa. |
| **competente** | El arreglo es un **default** en `.get("descuento_pct", 0)` que elimina el `None` en origen; mypy queda limpio por la razón correcta. |
| **excelente** | Articula (en comentario o write-up) por qué el default es superior a `# type: ignore`: el primero hace imposible el bug, el segundo solo esconde el aviso. |

### C3 — Comprensión demostrada (el write-up/explicación calza) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No puede explicar qué decía el error de mypy ni por qué. |
| **en-progreso** | Repite el texto del error sin entenderlo ("decía algo de None"). |
| **competente** | Explica que `.get` devuelve `int | None` y que un `int | None` no es asignable a un parámetro `int` sin manejar el `None`. |
| **excelente** | Conecta el concepto: mypy es "un test sobre los tipos antes de ejecutar"; el bug habría aparecido en runtime con un dato incompleto, y mypy lo adelantó. |

## Errores típicos a marcar
- **Silenciar en vez de arreglar:** `# type: ignore`, `cast(int, ...)` o `assert x is not None` para callar a mypy sin eliminar el `None`. mypy pasa, el bug conceptual queda.
- **`dict` o `list` pelados** bajo `--strict`: `--strict` los rechaza (disallow_any_generics). Hay que escribir `list[dict[str, int]]`.
- **Olvidar el acumulador:** anotar las funciones pero dejar `suma = 0` → mypy se queja porque le sumas un `float` a un `int`. Falta `suma: float = 0`.
- **Usar `Any` para que "pase":** apaga la verificación; es lo contrario del objetivo.
- **Arreglar el test en vez del código:** cambiar el test para que el item siempre traiga `descuento_pct` esquiva el bug real.
- (transversal) No agregar ningún test propio: pierde el hábito de pensar bordes.

## Señales de dependencia-IA
> Describir sin acusar; proponer una verificación.
- Anotaciones perfectas pero **incapacidad de explicar** qué error daba mypy o por qué `int | None` no calza.
- Sintaxis de tipos sofisticada e impropia del nivel F1 (p. ej. `TypeVar`, `Protocol`) sin poder defenderla, para un módulo trivial.
- El arreglo y la explicación no concuerdan (dice "le puse un default" pero el código tiene `# type: ignore`).
- **Verificación sugerida:** pídele que prediga, sin ejecutar, qué reporta mypy si cambia `.get("descuento_pct", 0)` de vuelta a `.get("descuento_pct")`. Si tipó de verdad, lo dice al toque.

## Feedback sugerido (graduado)
> Nunca dar el código de la solución. Primero pista, luego pregunta, luego dirección.
- **Pista (nivel 1):** "Lee el tipo que mypy nombra en el error: dice `int | None`. ¿De dónde sale ese `None`? Mira qué devuelve `.get` cuando la clave no existe."
- **Pregunta socrática (nivel 2):** "Si `item.get('descuento_pct')` puede ser `None`, ¿qué pasa en runtime cuando llega un item sin esa clave y haces `precio * None`? ¿Cómo le garantizas a mypy —y a ti— que ahí nunca habrá `None`?"
- **Dirección concreta (nivel 3, solo tras intento real):** "El patrón a corregir es **eliminar el `None` en origen**, no silenciarlo: dale a `.get` un valor por defecto del tipo correcto. Y revisa el tipo del acumulador: si le sumas un `float`, no puede declararse `int`."

## Conexión con el proyecto / capstone
- Tipar y pasar `mypy --strict` es exactamente lo que el **Capstone F1** exige del módulo Python (la mini-API de la despensa corre mypy en el pipeline). Este ejercicio es el primer eslabón de ese hábito.
