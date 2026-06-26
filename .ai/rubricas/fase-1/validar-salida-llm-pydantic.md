---
ejercicio_id: fase-1/validar-salida-llm-pydantic
fase: fase-1
sub_unidad: "1.4"
version: 1
---

# Rúbrica — Validar la salida de un LLM con pydantic

> Rúbrica **analítica** atada a los `objetivos` del contrato. Lo que se evalúa es la **disciplina de
> validar en la frontera**: el modelo debe aceptar lo bueno, coaccionar lo coaccionable, y rechazar lo
> malo (incluidos los campos alucinados) — no solo "que los tests pasen". Es la semilla de los hilos de
> evals y seguridad de IA.

## Objetivos evaluados
- **O1** — Diseñar un modelo pydantic v2 (`BaseModel` + `Field`) que tipe y valide datos externos no confiables.
- **O2** — Escribir un `@field_validator` (con `@classmethod`) para reglas que las constraints no cubren (strings de solo espacios).
- **O3** — Validar en la frontera la salida de un LLM: coacción, rechazo de campos alucinados (`extra="forbid"`) y manejo de `ValidationError`.

## Criterios y niveles

### C1 — Corrección del modelo (acepta lo bueno, rechaza lo malo) · mapea: O1, O3
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | El modelo no valida el JSON correcto, o `parsear_compra` no parsea+valida; varios tests fallan. |
| **en-progreso** | Valida el caso bueno y algunos malos, pero deja pasar campos alucinados (sin `extra="forbid"`) o no coacciona `monto`. |
| **competente** | Pasan los 9 tests: caso válido, coacción de `monto`, y rechazo de monto ≤ 0, vacíos, `items` vacío, fecha inválida y campo extra. |
| **excelente** | Además agregó un test propio realista (monto float, item vacío, campo faltante) y el modelo es legible y mínimo (sin sobre-ingeniería). |

### C2 — Calidad de los validadores · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin validador para los strings de solo espacios; `"   "` pasa como comercio válido. |
| **en-progreso** | Hay un `@field_validator` pero mal formado (sin `@classmethod`, o que no devuelve el valor, o mode equivocado) — funciona por casualidad o solo a medias. |
| **competente** | `@field_validator("comercio", "categoria")` con `@classmethod`, hace `strip`, lanza `ValueError` si queda vacío y **devuelve el valor normalizado**. |
| **excelente** | Reúsa un solo validador para ambos campos (DRY) y/o normaliza (devuelve el `strip`), de modo que el objeto validado queda limpio, no solo aceptado. |

### C3 — Seguridad / robustez de frontera (OWASP LLM: output handling) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Confía en la salida del LLM: sin `extra="forbid"`, los campos inventados entran sin avisar. |
| **en-progreso** | Cierra los extra pero no razona el porqué; lo puso "porque el test lo pedía". |
| **competente** | Usa `extra="forbid"` y explica que un campo alucinado debe fallar ruidoso, no pasar en silencio. |
| **excelente** | Conecta con el hilo de seguridad: "validar la salida del modelo antes de usarla" (LLM05 Improper Output Handling) y nombra esto como patrón de frontera reutilizable. |

### C4 — Comprensión demostrada · mapea: O1, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No distingue por qué pydantic (runtime) y no type hints (estático) para datos del LLM. |
| **en-progreso** | Entiende que pydantic valida pero no por qué eso es distinto de un type hint. |
| **competente** | Explica "validar en la frontera": el dato no confiable se valida al entrar; mypy no lo ve porque es runtime. |
| **excelente** | Articula el trade-off completo y por qué `model_validate_json` (un paso) es mejor que `json.loads` + validar (dos pasos, doble superficie de error). |

## Errores típicos a marcar
- **Confiar en la salida del LLM:** olvidar `extra="forbid"` → los campos alucinados entran silenciosos. Es el error #1 del ejercicio y del hilo de seguridad IA.
- **`min_length` creyendo que cubre los espacios:** `"   "` tiene largo 3 y pasa; falta el `@field_validator` con `strip`.
- **Sintaxis pydantic v1:** `@validator`, `.parse_raw()`, `.dict()`, `class Config:` — obsoleto. En v2 es `@field_validator`+`@classmethod`, `model_validate_json`, `model_dump`, `model_config = ConfigDict(...)`.
- **`@field_validator` sin `@classmethod`** o con los decoradores invertidos → error de configuración en v2.
- **Parsear y validar por separado** (`json.loads` + construir el modelo) cuando `model_validate_json` hace ambas.
- **Validador que no devuelve el valor:** un `@field_validator` que valida pero no hace `return v` deja el campo en `None`.
- (transversal) confiar en el LLM sin un test que demuestre el rechazo; no agregar caso borde propio.

## Señales de dependencia-IA
> Describir sin acusar; proponer una verificación.
- Modelo correcto pero **incapacidad de explicar** por qué `extra="forbid"` o por qué `"   "` pasa `min_length`.
- Uso de features avanzadas (`model_validator`, `Annotated[..., AfterValidator]`, `computed_field`) impropias del nivel y sin defensa, mientras falla lo básico.
- Mezcla de sintaxis v1 y v2 (señal de copia de fuentes desactualizadas sin comprender la diferencia).
- **Verificación sugerida:** pídele que prediga, sin ejecutar, qué pasa si el JSON trae `"monto": "mil"` en vez de un número, y que nombre qué tipo de error y por qué. Si diseñó el modelo, lo explica; si lo copió, titubea.

## Feedback sugerido (graduado)
> Nunca dar el modelo completo. Primero pista, luego pregunta, luego dirección.
- **Pista (nivel 1):** "Tu modelo acepta `comercio = '   '`. ¿Cuánto mide `'   '`? ¿`min_length=1` lo detiene? ¿Dónde pondrías una regla que `min_length` no puede expresar?"
- **Pregunta socrática (nivel 2):** "Un LLM te manda un campo `confianza` que nunca pediste. Por defecto, ¿pydantic lo rechaza o lo ignora? ¿Qué prefieres para datos no confiables, y con qué configuración lo consigues?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Te faltan dos piezas de frontera: (1) un `@field_validator` que haga `strip` y rechace lo vacío —porque `min_length` solo cuenta caracteres, no contenido útil—; y (2) `model_config = ConfigDict(extra='forbid')` para que un campo alucinado falle en vez de colarse. Revisa también que uses `model_validate_json` para parsear y validar en un solo paso."

## Conexión con el proyecto / capstone
- Validar la salida en la frontera es la pieza que reaparece en cada feature de IA del curso: en el **Capstone F1** los requests de la API se validan con pydantic; en F6 (`6.4` structured outputs, `6.14` seguridad LLM) este patrón se vuelve obligatorio (eval gate + guardrail de I/O). Aquí se siembra el hábito.
