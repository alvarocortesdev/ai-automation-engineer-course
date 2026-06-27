---
ejercicio_id: fase-6/validacion-tool-args
fase: fase-6
sub_unidad: "6.4"
version: 1
---

# Rúbrica — Gate de validación de argumentos de una tool

> Rúbrica **analítica** atada a los `objetivos` del contrato. Lo central no es "pasan
> los tests", es que el alumno **distinga forma de semántica** y entienda **por qué el
> gate existe** (el modelo pide, tú decides). Un gate que pasa los tests pero ejecuta
> tools fuera de la allowlist, o que no separa las tres capas, no demuestra el objetivo.

## Objetivos evaluados
- **O1** — Gate de tres capas (permiso → forma → semántica) sobre una tool call.
- **O2** — Validar argumentos con pydantic; forma válida ≠ semántica válida.
- **O3** — HITL (`CONFIRMAR`) para acción irreversible sobre el techo.
- **O4** — Explicar por qué forma válida no es ejecución segura (LLM06 / least privilege).

## Criterios y niveles

### C1 — Corrección del gate (¿hace lo que el objetivo pide?) · mapea: O1, O3
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No corre, o no devuelve `Decision`; varios tests en rojo. |
| **en-progreso** | Pasa algunos tests pero confunde capas (p. ej. valida argumentos de una tool no permitida, o ejecuta reembolsos sobre el techo). |
| **competente** | Los 11 tests en verde; las tres ramas (`EJECUTAR`/`RECHAZAR`/`CONFIRMAR`) salen donde corresponde. |
| **excelente** | Además rechaza argumentos **extra** no pedidos (`extra="forbid"` o equivalente) y/o normaliza el motivo de rechazo de forma legible para logging. |

### C2 — Calidad de ingeniería (validación real, orden correcto, clean code) · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin pydantic: valida "a mano" con `if`/`isinstance` desperdigados; o no maneja `ValidationError`. |
| **en-progreso** | Usa pydantic pero el **orden** de las capas está mal (valida forma antes de chequear allowlist) o atrapa excepciones demasiado amplias (`except Exception`). |
| **competente** | pydantic por tool con `field_validator` para los positivos; orden permiso → forma → semántica; atrapa `ValidationError`; agregó al menos un test propio. |
| **excelente** | Modelos por tool en un mapa (`{nombre: Modelo}`) sin `if` anidados frágiles; test propio relevante (p. ej. argumento extra, o monto exactamente en el techo). |

### C3 — Seguridad (OWASP LLM05/LLM06 aplicada) · mapea: O3, O4
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | El gate ejecuta cualquier tool cuyo nombre "suene bien"; no hay allowlist real. |
| **en-progreso** | Hay allowlist pero la acción irreversible cara se `EJECUTA` sin HITL. |
| **competente** | Allowlist comprobada **primero**; reembolso sobre el techo → `CONFIRMAR`; nunca se valida ni ejecuta una tool no permitida. |
| **excelente** | El `verificacion.md` nombra con precisión por qué esto es least privilege + control de Excessive Agency, y por qué `strict`/forma no sustituyen al gate. |

### C4 — Comprensión demostrada (write-up calza con el código) · mapea: O2, O4
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `prediccion.md`, o las predicciones se escribieron después de ejecutar (calzan demasiado perfecto, sin razonamiento). |
| **en-progreso** | `verificacion.md` dice "valido por si acaso" sin nombrar forma vs. semántica ni LLM06. |
| **competente** | Distingue claramente forma (schema/pydantic) de semántica (reglas de negocio) y conecta con least privilege. |
| **excelente** | Da un ejemplo propio de "forma válida + dato/peligro real" (p. ej. `reembolsar` con argumentos perfectos pero a un pedido ajeno) y dice dónde lo atraparía. |

## Errores típicos a marcar
- **Validar la forma antes de chequear la allowlist** — corre validación (y potencialmente lógica) sobre una tool que jamás debió considerarse. El permiso va primero.
- **Confiar en que `strict`/pydantic basta** — la forma válida no impide un reembolso de un millón ni una tool a un pedido ajeno; falta la capa semántica.
- **`except Exception` en vez de `except ValidationError`** — esconde bugs reales del gate como si fueran "argumentos inválidos".
- **Ejecutar la acción irreversible cara sin HITL** — `reembolsar` sobre el techo debe ser `CONFIRMAR`, no `EJECUTAR`.
- **Frontera mal puesta** — usar `>=` en vez de `>` para el techo (200 000 exacto debe `EJECUTAR`).
- (transversales) confía en la salida del LLM sin validar; agente con exceso de tools/permisos; falta un trade-off defendible en el write-up.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Código con `extra="forbid"`, mapas de modelos y manejo de errores impecable pero un `verificacion.md` que no sabe explicar **por qué** el orden de las capas importa.
- `prediccion.md` con las tres decisiones correctas pero sin razón, o con vocabulario muy por encima del nivel sin poder defenderlo.
- **Verificación sugerida:** pedir que prediga, sin ejecutar, el resultado de una **cuarta** tool nueva (p. ej. `cancelar_pedido`, irreversible, sin monto) y que diga en qué capa la atraparía. Si entendió las capas, lo resuelve; si dependió de la IA, se traba.

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Tu gate valida los argumentos de una tool que no está en la allowlist. ¿En qué orden deberían correr permiso, forma y semántica? ¿Qué no quieres ni mirar?"
- **Pregunta socrática (nivel 2):** "Si pydantic ya dice que los argumentos son válidos, ¿por qué `reembolsar` con `monto_clp` de un millón no debería ejecutarse solo? ¿Quién define ese límite, el modelo o tú?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Separa explícitamente tres pasos: (1) `if nombre not in ALLOWLIST: RECHAZAR`; (2) `try: Modelo.model_validate(args) except ValidationError: RECHAZAR`; (3) regla de negocio del techo → `CONFIRMAR`/`EJECUTAR`. La forma la da pydantic; la decisión de ejecutar la das tú."

## Conexión con el proyecto / capstone
- Este gate es exactamente el entregable "validación de salida antes de ejecutar + least-privilege de tools + HITL para acciones sensibles" del Definition of Done del capstone de la fase (y de los agentes de 6.8). Sin él, un RAG/agente que actúa es un incidente esperando ocurrir.
