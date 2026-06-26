---
ejercicio_id: fase-1/python-basico-intermedio-idiomatico
fase: fase-1
sub_unidad: "1.1"
version: 1
---

# Rúbrica — Inventario idiomático, empaquetado

> Rúbrica **analítica** atada a los `objetivos` del contrato. Lo que distingue este ejercicio de uno de Fase 0 no es solo que *funcione*, sino que el código sea **idiomático** (Pythonic) y que el **paquete siga importable**. Un alumno puede dejar los tests verdes con código en estilo "C" (con `range(len(...))` y `+` de strings): pasa la corrección de máquina, pero no el objetivo O1. La rúbrica mira el estilo, no solo el resultado.

## Objetivos evaluados
- **O1** — Implementar funciones idiomáticas (f-strings, `enumerate`, comprehensions, truthiness) que pasen los tests.
- **O2** — Mantener el paquete importable re-exportando desde `__init__.py` (`from despensa import ...`).
- **O3** — Validar entradas y manejar la lista vacía sin reventar.

## Criterios y niveles

### C1 — Corrección (¿pasan los tests, incluido el de paquete?) · mapea: O1, O2, O3
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Faltan funciones, o `test_import_desde_paquete` falla (no tocó `__init__.py`), o varios tests rojos. |
| **en-progreso** | La mayoría pasa pero falla un caso borde (lista vacía revienta, o no valida negativos, o el formato de `formatear_lineas` no es exacto). |
| **competente** | Los 9 tests pasan, incluido el import desde el paquete. Lista vacía y validación cubiertas. |
| **excelente** | Todo verde + un test propio significativo (no trivial) + firma/contrato respetados al pie. |

### C2 — Estilo idiomático (Pythonic) · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Estilo "C": `range(len(...))`, concatenación con `+` y `str(...)`, `if len(x) == 0`, bucle con `append` donde cabe una comprehension. |
| **en-progreso** | Mezcla: usa f-strings pero conserva `range(len(...))`, o construye con `append` en vez de comprehension en al menos un lugar. |
| **competente** | f-strings para el formato, `enumerate(..., start=1)` para numerar, comprehension/`sum` con generator para el resumen, truthiness (`if not productos`) para el vacío. |
| **excelente** | Lo anterior + validación en un solo recorrido, sin listas intermedias innecesarias; nombres claros; sin repetición. |

### C3 — Calidad de ingeniería (validación, manejo de errores, test propio) · mapea: O3, hilo testing
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No valida, o "valida" con `assert`/`print` en vez de `raise ValueError`; sin test propio. |
| **en-progreso** | Valida pero el orden o el alcance flaquea (no cubre precio Y stock), o el test propio es un duplicado. |
| **competente** | `raise ValueError` con mensaje claro para precio y stock negativos; un test propio que agrega un caso real. |
| **excelente** | Validación antes de acumular (el total nunca se contamina) + test propio que cubre un borde no obvio (p. ej. producto con stock 0 y precio 0, o varios agotados). |

## Errores típicos a marcar
- **Verde pero no idiomático:** tests pasan con `range(len(...))` y concatenación. Cumple la máquina, no O1. Es el error central de este ejercicio.
- **Olvidar `__init__.py`:** `test_import_desde_paquete` falla con `ImportError`/`AttributeError`. El alumno suele "arreglarlo" moviendo el test en vez de re-exportar.
- **Formato inexacto en `formatear_lineas`:** espacios, el guión `—` (em dash, no `-`), el `(x3)`, o numerar desde 0 (olvidar `start=1`).
- **Validar después de acumular:** el negativo ya entró al total antes del `raise`.
- **Default mutable** si el alumno "mejora" la firma con un parámetro extra `=[]` (no debería tocar firmas, pero ocurre).
- (transversal) Test propio que persigue cobertura en vez de una aserción con sentido; o que mockea algo que no hace falta mockear.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Código sospechosamente "perfecto" (uso de `defaultdict`, `dataclasses`, walrus) que el alumno **no puede explicar** ni justificar al nivel de la lección 1.1.
- `__init__.py` re-exporta pero el alumno no sabe **por qué** el test de paquete lo necesitaba.
- Comentarios o docstrings con un registro distinto al resto del código (pegado de un modelo).
- **Verificación sugerida:** pedir que, sin ejecutar, prediga qué pasa si se borra la línea del `__init__.py` y se corre `pytest`; y que reescriba `formatear_lineas` de memoria. Si dependió de la IA, se traba.

## Feedback sugerido (graduado)
> Nunca pegar el código de la solución de referencia.
- **Pista (nivel 1):** "Tus tests pasan, pero mira la línea con `range(len(productos))`: ¿qué necesitas de verdad ahí, el índice, el elemento, o ambos? Hay un built-in para 'ambos'."
- **Pregunta socrática (nivel 2):** "Si `from despensa import resumen_inventario` falla pero `from despensa.inventario import resumen_inventario` funciona, ¿qué diferencia hay entre importar el paquete y el módulo? ¿Dónde se decide qué expone el paquete?"
- **Dirección concreta (nivel 3, solo tras intento real):** "El patrón a aplicar es la **fachada del paquete**: `__init__.py` debe re-exportar los nombres que quieres ofrecer a nivel de paquete. Y para el estilo, sustituye `range(len(...))` por `enumerate(..., start=1)` y el `append` por una comprehension. Reescribe y vuelve a correr antes de mirar nada más."

## Conexión con el proyecto / capstone
- Este `despensa/` es el **esqueleto del lado Python del Capstone F1**. El estilo idiomático y la estructura de paquete que practicas aquí son los que el capstone exige desde la primera línea; la lógica se reusará tal cual y se cubrirá con más tests en `1.6`.
