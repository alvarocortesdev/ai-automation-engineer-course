---
ejercicio_id: fase-6/idp-confianza-gate
fase: fase-6
sub_unidad: "6.11"
version: 1
---

# Rúbrica — El gate de confianza + validación de un IDP

> Rúbrica **analítica** atada a los `objetivos` del contrato. El corrector evalúa el
> **proceso** (¿predijo a mano antes de codear?) y la **comprensión** (¿separa confianza
> de corrección?), no solo si los tests pasan. Lee la solución de referencia **al final**,
> cuando ya formaste tu propio juicio.

## Objetivos evaluados

- **O1** — Gate de confianza: separar campos auto-aceptables de los de revisión humana.
- **O2** — Validación cruzada total-vs-líneas con tolerancia de coma flotante.
- **O3** — Combinar gate y validación en una decisión auto/HITL, entendiendo que confianza
  no es corrección.

## Criterios y niveles

### C1 — Corrección del gate y la validación · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No pasa los tests; o usa `>` en vez de `>=` en el umbral, o revienta con `confidence == None`, o compara el total con `==` sobre floats. |
| **en-progreso** | Pasa la mayoría pero falla un borde (None, el umbral exacto, la tolerancia de floats, o el orden de los campos). |
| **competente** | Todos los tests verdes: `None` y bajo-umbral van a revisión, `== umbral` se acepta, `total_cuadra` usa tolerancia, se preserva el orden de entrada. |
| **excelente** | `decidir_procesamiento` **reusa** las otras dos (no duplica el filtro ni la aritmética) y la lógica queda legible; o añade un test propio (p. ej. campo con confidence 0.0). |

### C2 — Decisión combinada y motivos · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `decidir_procesamiento` ignora uno de los dos chequeos (solo mira confidence, o solo el total), o devuelve "auto" sin vaciar `motivos`. |
| **en-progreso** | Decide bien auto/HITL pero los `motivos` no distinguen el campo dudoso del total descuadrado. |
| **competente** | "auto" solo si ambos pasan; cuando falla, junta motivos que nombran el campo dudoso y/o el total descuadrado; "auto" ⇒ `motivos == []`. |
| **excelente** | Acumula ambos motivos cuando ambos fallan, sin cortar al primero; mensajes accionables para el humano. |

### C3 — Proceso Primero-Sin-IA (predicción antes de medir) · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `prediccion.md`, o se escribió después de correr los tests (decisiones calcadas sin razón). |
| **en-progreso** | Da las decisiones pero sin el motivo, o no cubre los 3 casos. |
| **competente** | `prediccion.md` existe antes de ejecutar: A=auto, B=HITL (Total bajo umbral), C=HITL (total no cuadra), con su razón. |
| **excelente** | Anticipa que el caso C es el interesante: confidence alto pero incoherente; nombra por qué el gate solo no lo atrapa. |

### C4 — Comprensión demostrada (confianza ≠ corrección, LLM05) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `verificacion.md` ausente, o dice "hay que validar" sin explicar por qué el confidence no basta. |
| **en-progreso** | Separa confianza de corrección pero no conecta con LLM05 / el agente que actúa. |
| **competente** | Explica que confidence es auto-estimación de la *lectura*, no de la *coherencia*; que `total_cuadra` es una regla de negocio que atrapa lo que el gate deja pasar; nombra LLM05. |
| **excelente** | Conecta con el capstone agéntico (Fase 7): validar la salida ANTES de que el agente pague/ejecute; menciona indirect prompt injection desde el texto del documento (LLM01). |

## Errores típicos a marcar

- **`>` en vez de `>=`** en el umbral: un campo justo en el umbral cae mal a revisión (lo atrapa `test_clasificar_en_el_umbral_se_acepta`).
- **No manejar `confidence is None`**: revienta o lo trata como 0/auto. Un campo sin confidence es *desconocido*, va a revisión.
- **Comparar el total con `==`** sobre floats: `0.1 + 0.2 != 0.3`; lo atrapa `test_total_cuadra_con_tolerancia_de_floats`.
- **`decidir_procesamiento` que reimplementa** el filtro o la suma en vez de reusar las otras dos: duplicación que se desincroniza.
- **Cortar al primer motivo** (return temprano) en vez de acumular: el humano pierde info de qué más revisar.
- **Confundir "confianza alta" con "dato correcto"** en la reflexión: el corazón conceptual del ejercicio.
- (transversal) Tratar el texto/dato extraído como confiable sin mencionar que es input no confiable (LLM01/LLM05).

## Señales de dependencia-IA

> Describir sin acusar; proponer una verificación.

- Implementación correcta pero `prediccion.md` ausente o idéntica al output real (predijo "después").
- `verificacion.md` usa "confianza no es corrección" como eslogan pero, ante una pregunta de seguimiento, no puede dar un ejemplo concreto (un total bien leído de una factura incoherente).
- **Verificación sugerida:** pedir que invente un cuarto caso donde el gate de confianza pase pero la validación cruzada falle, y que lo razone a mano.

## Feedback sugerido (graduado)

> Nunca pegar el código de la solución.

- **Pista (nivel 1):** "¿Qué pasa con un campo cuyo `confidence` es `None`? ¿Tu `<` lo maneja, o revienta?"
- **Pregunta socrática (nivel 2):** "Si el modelo está 99% seguro de haber leído `100.000`, pero las líneas suman `90.000`, ¿qué te dice el confidence y qué te dice la suma? ¿Cuál atrapa el error?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Separa los tres pasos: (1) clasificar por umbral (cuidando `None` y `>=`), (2) validar la aritmética con `abs(suma - total) <= tolerancia`, (3) combinar: 'auto' solo si la lista de revisar está vacía Y el total cuadra; junta los motivos en una lista en vez de cortar al primero."

## Conexión con el proyecto / capstone

- Este gate es el patrón de "validación de salida antes de ejecutar" del **Definition of Done** del capstone agéntico (Fase 7): un agente que procesa documentos no actúa sobre datos no validados, y el HITL recibe lo dudoso. Documenta el umbral y la validación cruzada en un ADR.
