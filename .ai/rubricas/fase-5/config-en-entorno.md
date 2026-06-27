---
ejercicio_id: fase-5/config-en-entorno
fase: fase-5
sub_unidad: "5.2"
version: 1
---

# Rúbrica — Config en el entorno (Factor III)

> Rúbrica **analítica** atada a los `objetivos`. Evalúa `settings.py` + `bitacora.md`
> con `test_settings.py` en verde. Los tests verifican la mecánica (lee del entorno,
> fail-fast, tipos); la `bitacora.md` verifica que el alumno entiende **qué es config**
> y **por qué** importa el fail-fast.

## Objetivos evaluados
- **O1** — Leer config del entorno con `pydantic-settings` (`env_prefix`, tipos validados).
- **O2** — Campos requeridos sin default → la app falla al arrancar si falta config (fail-fast), sin defaults inseguros para secretos.
- **O3** — Explicar qué es config vs código y por qué un `.env` commiteado rompe el Factor III.

## Criterios y niveles

### C1 — Corrección de la config · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `test_settings.py` en rojo: no lee del entorno, no usa `env_prefix="APP_"`, o `database_url`/`api_key` tienen default (el test del entorno vacío no lanza). |
| **en-progreso** | Lee del entorno pero falla un caso: `port`/`debug` no parsean al tipo correcto, o `get_settings()` cachea y un test que cambia el entorno no ve el cambio. |
| **competente** | Todos los tests en verde: lee requeridos, `debug` parsea `"true"/"1"`, `port` default e desde entorno como `int`, falta-de-requerido y entorno-vacío lanzan `ValidationError`. |
| **excelente** | Verde + limpio: usa `BaseSettings`/`SettingsConfigDict` idiomático, sin `os.environ` manual; `get_settings()` devuelve instancia fresca; comenta por qué no cachea en el contexto de test. |

### C2 — Seguridad de la config · mapea: O2 (hilo seguridad)
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Deja algún secreto escrito en el código, o le pone default vacío a `api_key`/`database_url`. |
| **en-progreso** | Quita los secretos del código pero no entiende por qué (la `bitacora.md` no lo menciona). |
| **competente** | Cero secretos en el código; requeridos sin default; menciona que el `.env` va en `.gitignore`. |
| **excelente** | Razona en `bitacora.md` la diferencia entre un fallo ruidoso-temprano (requerido) y uno silencioso-tardío (default vacío); menciona el `.env.example` y que las vars reales tienen prioridad sobre el `.env`. |

### C3 — Comprensión demostrada (bitácora) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `bitacora.md` ausente o solo describe el código. |
| **en-progreso** | Dice "config va en el entorno" pero no distingue config de código con un ejemplo propio. |
| **competente** | Da un ejemplo de config (URL/secreto) y uno de no-config (nombre de la app, rutas) de su propio proyecto, y explica por qué un `.env` commiteado filtra secretos. |
| **excelente** | Conecta con la fase: la misma imagen en dev/prod (V/X), el gate de secret-scanning de `5.4`, y por qué fail-fast es preferible en un deploy. |

## Errores típicos a marcar
- **Default inseguro:** `api_key: str = ""` o `database_url: str = "sqlite:///./dev.db"` — convierte un fallo temprano en uno tardío y silencioso. El test del entorno vacío lo caza.
- **Leer con `os.environ` a mano:** funciona pero pierde la validación de tipos y el fail-fast; el enunciado pide `pydantic-settings`.
- **Cachear `get_settings()` con `lru_cache`** en este ejercicio: enmascara los cambios de entorno que los tests hacen; los tests de `port`/`debug` desde entorno fallan.
- **Olvidar `env_prefix`:** lee `DATABASE_URL` en vez de `APP_DATABASE_URL`; los tests definen las `APP_*`.
- **Confundir tipo:** dejar `port` como `str` o no parsear `debug` a `bool`.
- (transversal seguridad) dejar un secreto de ejemplo escrito "porque es de prueba": el hábito es lo que se evalúa.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Solución correcta pero `bitacora.md` que no sabe distinguir config de código (lo copió sin internalizarlo).
- Sobre-ingeniería no pedida: múltiples fuentes de settings, validadores custom, `lru_cache` con invalidación — impropio del nivel y rompe los tests.
- Usa una librería distinta a la pedida sin justificar.
- **Verificación sugerida:** pídele que prediga, sin correr, qué pasa si se despliega sin `APP_API_KEY`. Si no dice "ValidationError al arrancar / el proceso no levanta", no internalizó el fail-fast.

## Feedback sugerido (graduado)
> Nunca pegar el cuerpo de `Settings` antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "¿Tus campos `database_url`/`api_key` tienen un `=` con valor por defecto? ¿Qué pasa entonces cuando la variable falta?"
- **Pregunta socrática (nivel 2):** "Si despliegas a las 6pm sin la `APP_API_KEY` y le pusiste `api_key: str = ''`, ¿cuándo y cómo te enteras del problema? ¿Y si la dejas requerida?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Un campo sin `=` es requerido. `model_config = SettingsConfigDict(env_prefix='APP_')`. `Settings()` lee del entorno al instanciar y lanza `ValidationError` si falta un requerido. Repasa 4.2 y 6.3."

## Conexión con el proyecto / capstone
- Es el módulo de config del capstone de la Fase 5: una sola imagen, config por entorno, cero secretos en el repo. Junto con la auditoría (`auditoria-12-factor`) cubre el Factor III que el gate de secret-scanning de `5.4` exige y que la observabilidad de `5.10` y el despliegue de `5.9` dan por hecho.
