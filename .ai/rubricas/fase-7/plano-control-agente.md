---
ejercicio_id: fase-7/plano-control-agente
fase: fase-7
sub_unidad: "7.7"
version: 1
---

# Rúbrica — El plano de control de un agente que actúa

> Rúbrica **analítica** atada a los `objetivos` del contrato. Ejercicio **mixto**:
> hay tests automáticos (`test_plano_control.py`) **y** un `write-up.md`. El verde
> de los tests es necesario, no suficiente: el corrector evalúa también si el
> write-up demuestra que el alumno entiende *por qué* una acción sensible va a HITL
> y *por qué* validar el schema no es confiar en el contenido. Pasar los tests sin
> un write-up defendible es `competente` a lo sumo.

## Objetivos evaluados

- O1: Implementar el plano de control aplicando los cinco chequeos en orden.
- O2: Justificar por qué el orden de los chequeos es el diseño de seguridad.
- O3: Distinguir validar el schema de confiar en el contenido; nombrar LLM05/LLM06.

## Criterios y niveles

### C1 — Corrección del plano de control · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Tests en rojo; falta alguna ruta, o el techo de costo es un parámetro muerto. |
| **en-progreso** | Las rutas básicas funcionan pero el **orden** falla (p. ej. un duplicado con schema inválido devuelve `RECHAZO`, o una acción sensible con confianza alta devuelve `AUTO`). |
| **competente** | Los 12 tests en verde: cada rama cubierta y el orden verificado (idempotencia → schema → costo → sensible → confianza). |
| **excelente** | Además, un caso propio significativo (p. ej. duplicado que también es sensible → gana `DUPLICADO`), y motivos descriptivos que identifican exactamente qué barrera frenó. |

### C2 — Seguridad: orden de chequeos y least-privilege · mapea: O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | El write-up trata el orden como arbitrario, o cree que con confianza alta se puede auto-ejecutar una acción sensible. |
| **en-progreso** | Justifica algún chequeo pero no el orden completo, o no conecta el HITL obligatorio con Excessive Agency. |
| **competente** | Explica que la primera barrera que aplica decide, y por qué una acción sensible va a HITL aunque la confianza sea 0.99 (LLM06 + confianza no calibrada). |
| **excelente** | Articula la defensa en profundidad: el cerebro puede caer (prompt injection), pero el plano de control determinista sigue exigiendo schema, reglas y HITL. |

### C3 — Comprensión: schema vs contenido · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Cree que "validó el schema" = "el contenido es correcto". |
| **en-progreso** | Distingue forma de verdad pero no da un ejemplo. |
| **competente** | Explica que el schema garantiza la forma, no la verdad, y da un ejemplo (salida válida vs schema pero con monto/categoría equivocados). |
| **excelente** | Conecta con que el guardrail de schema es la primera barrera, no la única (reglas de negocio + verificación + HITL encima). |

## Errores típicos a marcar

- Poner la confianza como primer chequeo → cortocircuita idempotencia, schema, costo y la regla de acción sensible (es el agujero del ejercicio 6.2 MODIFY).
- Auto-ejecutar una acción sensible porque la confianza es alta (viola LLM06; ignora que la confianza no está calibrada).
- Actuar sobre una salida con `valido=False` (Improper Output Handling, LLM05).
- Recibir `techo_costo_usd` y no usarlo (Unbounded Consumption sin circuit-breaker).
- Validar el schema antes de chequear idempotencia → procesa de más un duplicado en algunos flujos; además es trabajo desperdiciado.
- Combinar barreras en un solo `if ... and ...`, perdiendo el `motivo` que identifica qué frenó.
- (transversal) Confundir "validó el schema" con "es correcto"; creer que el agente no necesita idempotencia "porque la parte nueva es el LLM".

## Señales de dependencia-IA

- Plano de control impecable pero el alumno no puede explicar por qué el orden importa, ni qué pasa si la confianza va primero.
- Write-up que usa el vocabulario exacto de la lección (LLM05/LLM06) sin poder dar un ejemplo propio de salida válida pero incorrecta.
- Sofisticación impropia (menciona NeMo Guardrails, Llama Guard, calibración Platt) sin poder explicar el caso simple "acción sensible → HITL siempre".
- **Verificación sugerida:** pedir que prediga, sin ejecutar, la ruta de un duplicado con schema inválido y acción sensible (debe decir `DUPLICADO`). Si entendió el orden, responde al instante; si dependió de IA, duda.

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "Corre mentalmente un caso que dispare DOS barreras a la vez (p. ej. duplicado + schema inválido). ¿Cuál gana en tu código? ¿Cuál debería ganar?"
- **Pregunta socrática (nivel 2):** "Si el modelo reporta 0.99 de confianza en un reembolso de 10 millones, ¿qué te garantiza ese número? ¿De dónde sale realmente la garantía de que la acción es correcta?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Ordena los chequeos como una cadena de `if` con `return` temprano: idempotencia → schema → costo → sensible → confianza. La confianza es el ÚLTIMO chequeo y solo para acciones no sensibles. Para el write-up, LLM05 e LLM06 viven en la sección 4.4 y 5 de la lección."

## Conexión con el proyecto / capstone

- Este plano de control es el **punto 6 del Definition of Done** del [capstone F7](/fase-7-automatizacion/proyecto/) hecho código: validación de salida + least-privilege de tools + HITL para acciones sensibles + techo de costo. Es la pieza que vuelve digno de producción al agente que ejecuta acciones.
