---
ejercicio_id: fase-5/cliente-azure-openai-v1
fase: fase-5
sub_unidad: "5.6"
version: 1
---

# Rúbrica — Escribe el cliente v1 de Azure OpenAI

> Rúbrica **analítica** atada a los `objetivos` del contrato. Hay un test estructural que da el piso
> (verde/rojo), pero el corrector evalúa además **comprensión**: que el alumno sepa *por qué* la forma
> v1 es la correcta, no solo que pegó el patrón.

## Objetivos evaluados

- O1: Construir el cliente vigente (API v1 GA): `OpenAI()`, `base_url` con `/openai/v1`, sin `api_version`.
- O2: Leer endpoint y clave del entorno, sin hardcodear secretos (12-factor).
- O3: Llamar a `chat.completions` con `model=<deployment>`, sabiendo por qué es el deployment y no el modelo base.

## Criterios y niveles

### C1 — Corrección (¿usa la API v1 vigente?) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Usa `AzureOpenAI()` y/o `api_version`; o `base_url` sin `/openai/v1`. Tests en rojo. |
| **en-progreso** | Cliente `OpenAI()` pero le falta el sufijo `/openai/v1`, o deja un `api_version` muerto. |
| **competente** | `OpenAI()` + `base_url` con `/openai/v1/` + sin `api_version`. Todos los tests en verde. |
| **excelente** | Lo anterior + arma `base_url` robusto (maneja el `/` final del endpoint) y menciona Managed Identity como la variante de prod. |

### C2 — Higiene de config y secretos (12-factor) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Endpoint o clave **hardcodeados** en el código. |
| **en-progreso** | Lee uno del entorno pero deja el otro fijo, o usa nombres de variable inventados. |
| **competente** | `AZURE_OPENAI_ENDPOINT` y `AZURE_OPENAI_API_KEY` desde el entorno; nada hardcodeado. |
| **excelente** | Además explica el salto a Managed Identity (cero claves) como el ideal de prod. |

### C3 — `model` = deployment · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No usa el parámetro `deployment` en `model=`, o no devuelve el contenido. |
| **en-progreso** | Usa `model=deployment` pero no puede explicar la diferencia con el modelo base. |
| **competente** | `model=deployment`, devuelve `choices[0].message.content`, y explica que es la etiqueta del deployment. |
| **excelente** | Explica además qué error da equivocarse (`DeploymentNotFound`) y por qué difiere de la API pública de OpenAI. |

## Errores típicos a marcar

- Dejar `AzureOpenAI()` o `api_version` (residuo de tutoriales viejos): es el error central del ejercicio.
- `base_url` sin el sufijo `/openai/v1/` (no activa la v1).
- Endpoint/clave hardcodeados, o un `.gitignore` ofrecido como "seguridad".
- `model` con el nombre del modelo base en vez del deployment.
- (transversal) confiar en la salida del LLM sin pensar validación (aquí no se pide, pero el excelente lo menciona).

## Señales de dependencia-IA

- Código v1 perfecto pero el alumno no sabe explicar por qué `model=` es el deployment ni qué era `api_version`.
- Aparece manejo sofisticado (retries, streaming) que el enunciado no pide y que no puede defender.
- Mezcla patrones de la API vieja y la nueva sin notar la contradicción (señal de copy-paste de dos fuentes).

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "Tu cliente, ¿es `OpenAI()` o `AzureOpenAI()`? Mira el 4.3: la v1 usa el estándar y el sufijo `/openai/v1/`."
- **Pregunta socrática (nivel 2):** "Si en la API pública `model='gpt-4.1-mini'` es el modelo, ¿qué es `model` en Azure? ¿Qué tuviste que crear antes en el portal?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Quita `api_version` (la v1 lo eliminó), arma `base_url` = endpoint + `/openai/v1/` (cuida la doble barra), y pasa `deployment` a `model=`. La clave, desde `os.environ`. Revisa 4.3–4.4."

## Conexión con el proyecto / capstone

- Es el bloque de inferencia del RAG sobre Azure (Capstone F5 vía Azure): sin el cliente v1 correcto, el resto del pipeline no llama al modelo. El excelente ya apunta a la Managed Identity que el DoD premia.
