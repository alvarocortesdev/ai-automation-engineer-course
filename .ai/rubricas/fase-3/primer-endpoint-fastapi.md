---
ejercicio_id: fase-3/primer-endpoint-fastapi
fase: fase-3
sub_unidad: "3.8"
version: 1
---

# Rúbrica — Tu primera API FastAPI: tareas con CRUD parcial

> Rúbrica **analítica** atada a los `objetivos`. Evalúa `app.py` + `bitacora.md` con
> `test_app.py` en verde. El test es objetivo (status codes, validación, filtro). Pero pasar
> el test no basta: la `bitacora.md` debe mostrar que el alumno entiende **quién** valida, **cuándo**
> y **por qué** el response_model importa.

## Objetivos evaluados
- **O1** — Endpoints que reciben path/query/body y los validan con modelos pydantic.
- **O2** — Status code correcto (201 al crear) + response_model explícito que controla la salida.
- **O3** — Caso "no existe" con `HTTPException(404)`, no un error disfrazado de 200.

## Criterios y niveles

### C1 — Corrección de los endpoints · mapea: O1, O2, O3
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Algún endpoint sin implementar o `test_app.py` en rojo en varios casos. |
| **en-progreso** | Crea y lista, pero falla algo sustancial: no devuelve 201, no maneja el 404, o el filtro/limite no funciona. |
| **competente** | Los 7 tests en **verde**: 201 al crear, 422 (titulo ausente y vacío), 404, filtro `completada`, validación de `limite`. |
| **excelente** | Verde + `TareaCrear` con restricciones claras (`Field(min_length=1)`), endpoints `async` donde no hay I/O bloqueante, y código limpio sin validación manual redundante. |

### C2 — Validación delegada a pydantic (no ifs) · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Valida `titulo` con `if not titulo: ...` dentro del endpoint en vez de en el modelo. |
| **en-progreso** | Declara el modelo pero deja `titulo` opcional o sin `min_length`, así que el 422 de vacío no sale. |
| **competente** | `titulo: str = Field(min_length=1)`; FastAPI rechaza con 422 antes del endpoint. |
| **excelente** | Además explica en la bitácora que la validación ocurre en el borde, antes de su código, y por qué eso reduce defensas manuales. |

### C3 — Comprensión demostrada (bitácora) · mapea: O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `bitacora.md` ausente o no responde las preguntas. |
| **en-progreso** | Responde a medias: "da 422 porque está mal" sin decir quién detiene el request ni cuándo. |
| **competente** | Explica que pydantic rechaza el body inválido antes del endpoint (422), qué filtra `response_model`, y por qué crear es 201. |
| **excelente** | Conecta `response_model` con seguridad (no fugar campos) y los status codes con el contrato REST de `3.7`. |

## Errores típicos a marcar
- **Devolver el dict crudo confiando en que "no pasa nada":** funciona aquí porque el dict calza, pero el hábito correcto es declarar `response_model`; señala que es la barrera anti-fuga.
- **`titulo` opcional:** sin `min_length=1` (o sin marcarlo requerido), `test_titulo_vacio`/`test_titulo_ausente` fallan. Es justo lo que mide el ejercicio.
- **Manejar el 404 con `return {"error": ...}`:** devuelve 200; el cliente no distingue éxito de fallo. Debe ser `raise HTTPException(404, ...)`.
- **Validar con `if` dentro del endpoint:** reinventa pydantic; acopla validación a lógica.
- **Olvidar `global _siguiente_id`:** `UnboundLocalError` al incrementar. Marca el alcance de variables.
- (transversal spec-driven) no abrir `/docs` para ver el contrato OpenAPI que FastAPI generó solo.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Código impecable con patrones no enseñados aún (routers, lifespan, SQLModel) en un ejercicio de tres endpoints en memoria: sofisticación impropia del nivel.
- `bitacora.md` que no sabe decir **quién** detiene un request inválido ni **en qué momento**.
- No puede explicar por qué su endpoint es `async def` (o por qué daría igual aquí, al no haber I/O real).
- **Verificación sugerida:** pídele que prediga, sin correr, qué status devuelve `POST /tareas` con `{"titulo": ""}` y por qué; y qué pasaría si quitara `response_model` y su dict tuviera un campo `secreto`.

## Feedback sugerido (graduado)
> Nunca pegar el cuerpo de los endpoints antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Corre el test y lee qué caso falla. ¿El 422 de titulo vacío sale? Si no, mira dónde declaraste (o no) la restricción del título."
- **Pregunta socrática (nivel 2):** "Cuando llega un body sin `titulo`, ¿tu función llega a ejecutarse o FastAPI lo corta antes? ¿Dónde declaras que `titulo` es obligatorio para que eso ocurra?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Declara `titulo: str = Field(min_length=1)` en `TareaCrear`, devuelve un 201 con `status_code`, y para el 404 usa `raise HTTPException(status_code=404, ...)`. Repasa 4.5–4.7."

## Conexión con el proyecto / capstone
- Es el patrón base de cada endpoint del capstone: validar entrada, controlar salida, status codes correctos y 404 honesto. El `response_model` es la primera defensa de seguridad (no fugar datos) que endureces en `3.13`.
