---
ejercicio_id: fase-1/excepciones-idiomaticas-python
fase: fase-1
sub_unidad: "1.9"
version: 1
---

# Rúbrica — Excepciones de dominio en Python (parser de gastos)

> Rúbrica **analítica** atada a los `objetivos` del contrato. Lo que se evalúa es la **decisión de
> diseño**: la unidad lanza, el lote devuelve los errores como datos, y la causa se preserva con
> encadenamiento. No basta "que los tests pasen": el alumno debe poder defender *por qué* cada nivel
> usa un idioma distinto.

## Objetivos evaluados
- **O1** — Implementar una jerarquía de excepciones de dominio (subclase de `Exception`) y lanzarla ante entrada inválida.
- **O2** — Encadenar excepciones con `raise ... from e` preservando la causa original.
- **O3** — Decidir el nivel del manejo: la unidad lanza; el lote devuelve los errores como datos sin caerse.

## Criterios y niveles

### C1 — Corrección (la unidad lanza, el lote separa) · mapea: O1, O3
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `parsear_linea` no cubre los 4 modos de fallo, o `parsear_archivo` se cae con una línea mala; varios tests fallan. |
| **en-progreso** | `parsear_linea` lanza, pero `parsear_archivo` no separa bien (cuenta mal los números de línea, no ignora blancas, o relanza en vez de acumular). |
| **competente** | Pasan todos los tests: los 4 modos de fallo lanzan `LineaInvalida`, y `parsear_archivo` separa válidos y errores, ignora blancas y no se cae. |
| **excelente** | Además agregó un test propio realista y el código es legible (early-raise por modo de fallo, sin anidamiento profundo). |

### C2 — Encadenamiento y elección de la excepción · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Lanza `Exception`/`ValueError` genérico, o no define una excepción de dominio; sin `from e`. |
| **en-progreso** | Define `LineaInvalida` pero no encadena el `ValueError` del `int()` (sin `from e`), o hereda de `BaseException`. |
| **competente** | `LineaInvalida(Exception)`; el monto no entero usa `raise LineaInvalida(...) from e` y `__cause__` es el `ValueError`. |
| **excelente** | Explica que el `from e` preserva la causa para la stack trace (observabilidad) y por qué heredar de `Exception` y no de `BaseException`. |

### C3 — Comprensión demostrada (cuándo lanzar vs devolver) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No distingue por qué la unidad lanza y el lote devuelve; trataría ambos igual. |
| **en-progreso** | Intuye la diferencia pero no la articula en términos de contrato ("válido o nada" vs "todo lo que puedas + reporte"). |
| **competente** | Explica que el contrato de cada función dicta el idioma: interrumpir el flujo (excepción) vs reportar fallos esperados (datos). |
| **excelente** | Conecta con el capstone: estas excepciones de dominio se mapearán a códigos HTTP en FastAPI; el patrón de recolección sirve para procesar lotes (correos, cartolas). |

## Errores típicos a marcar
- **`except` pelado o `except Exception` que se traga todo** en `parsear_archivo` (atraparía bugs reales, no solo `LineaInvalida`). Debe ser `except LineaInvalida`.
- **Olvidar `from e`** → se pierde la causa; la stack trace ya no apunta al `ValueError` original.
- **Heredar de `BaseException`** → atraparía `KeyboardInterrupt`/`SystemExit`.
- **Pre-chequear el monto con regex/isdigit en vez de EAFP** (`try int()`), que además falla con negativos y signos.
- **Contar mal los números de línea** (no usar `enumerate(..., start=1)`, o saltarse el conteo de las blancas).
- **`parsear_archivo` que relanza** en vez de acumular → se cae en la primera línea mala (rompe su contrato).
- (transversal) no agregar un test propio; perseguir que "pase" sin razonar el diseño.

## Señales de dependencia-IA
> Describir sin acusar; proponer una verificación.
- Código correcto pero **incapacidad de explicar** por qué el lote devuelve y la unidad lanza.
- Uso de `contextlib.suppress`, `ExceptionGroup`/`except*` u otras features avanzadas impropias del nivel y sin defensa, mientras falla lo básico.
- `from e` presente pero el alumno no sabe qué hace `__cause__` ni dónde lo vería.
- **Verificación sugerida:** pídele que prediga, sin ejecutar, qué imprime la stack trace de `parsear_linea("Lider;abc;super")` con y sin `from e`, y qué cambia. Si lo diseñó, lo explica; si lo copió, titubea.

## Feedback sugerido (graduado)
> Nunca dar la solución completa. Primero pista, luego pregunta, luego dirección.
- **Pista (nivel 1):** "Tu `parsear_archivo` se cae con la primera línea mala. ¿Qué hace el `except` cuando atrapa: relanza o guarda el error y sigue?"
- **Pregunta socrática (nivel 2):** "`parsear_linea` y `parsear_archivo` fallan distinto a propósito. ¿Cuál es el *contrato* de cada una? ¿Cuál dice 'válido o nada' y cuál 'procesa todo y repórtame'? ¿Qué idioma de error sirve a cada contrato?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Dos arreglos: (1) en el monto, usa `try: int(monto_raw) except ValueError as e: raise LineaInvalida(...) from e` para conservar la causa; (2) en `parsear_archivo`, el `except LineaInvalida as e` no debe relanzar — debe hacer `errores.append(ErrorLinea(numero, linea, str(e)))` y continuar. Cuenta las líneas con `enumerate(splitlines(), start=1)` y salta las blancas con `if not linea.strip(): continue`."

## Conexión con el proyecto / capstone
- En el **Capstone F1** (lado Python) cada fallo esperado (no encontrado, stock insuficiente) lanza una excepción de dominio; en la Fase 3 esas excepciones se mapean a HTTP (404/409) en un solo lugar. El patrón "lote que recolecta errores" reaparece al procesar correos/cartolas en lotes (Fase 7). Aquí se siembra el criterio de cuándo lanzar y cuándo devolver.
