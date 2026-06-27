---
ejercicio_id: fase-6/reintentos-backoff
fase: fase-6
sub_unidad: "6.3"
version: 1
---

# Rúbrica — Reintentos con backoff exponencial + jitter

> Rúbrica **analítica** atada a los `objetivos` del contrato. El corrector evalúa el
> **proceso** (¿predijo las esperas antes de medir?) y la **comprensión** (¿por qué el
> Retry-After gana? ¿por qué el jitter?), no solo si los tests pasan. Lee la solución de
> referencia **al final**, cuando ya formaste tu propio juicio.

## Objetivos evaluados

- **O1** — Implementar backoff exponencial + jitter con Retry-After y tope.
- **O2** — Distinguir error reintentar-able del que se propaga de inmediato.
- **O3** — Predecir la secuencia exacta de esperas sin ejecutar.

## Criterios y niveles

### C1 — Corrección de la política de reintento · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No pasa los tests; o duerme también tras el último intento, o no aplica el tope, o el jitter pisa al Retry-After. |
| **en-progreso** | Pasa la mayoría pero falla un borde (Retry-After no gana, off-by-one en el número de esperas, o no re-lanza la última excepción). |
| **competente** | Todos los tests verdes: backoff `min(tope, base·2^i)` + jitter, Retry-After exacto gana, no duerme tras el último intento, re-lanza la última `ErrorReintentable`. |
| **excelente** | Además deja claro (comentario o estructura) por qué el último intento no duerme; o añade un test propio (p. ej. max_intentos=1 nunca duerme). |

### C2 — Clasificación de errores · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Reintenta cualquier excepción (un `except Exception` que traga el no-reintentable), o `dormir` se llama ante un error definitivo. |
| **en-progreso** | Distingue, pero captura de más (p. ej. atrapa el no-reintentable y lo re-lanza con ruido) o de menos. |
| **competente** | Solo `ErrorReintentable` se reintenta; cualquier otra excepción se propaga **de inmediato** sin dormir (lo verifica `test_error_no_reintentable_se_propaga_de_inmediato`). |
| **excelente** | El `verificacion.md` argumenta por qué un `400`/`401` no se reintenta (request inválido / key mala: el reintento manda lo mismo). |

### C3 — Proceso Primero-Sin-IA (predicción de esperas) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `prediccion.md`, o se escribió tras correr los tests (lista calcada sin razón). |
| **en-progreso** | Da la lista pero no explica por qué la última no es 16. |
| **competente** | `prediccion.md` antes de ejecutar: `[1, 2, 4, 8, 8]` y explica que el 5º valor se topa en 8 (tope) y que el 6º intento no duerme. |
| **excelente** | Anticipa que con jitter > 0 las esperas serían mayores y desincronizadas, sin que se lo pidan. |

## Errores típicos a marcar

- **Dormir tras el último intento**: produce una espera de más y un re-lanzamiento tardío. La política es: en el intento final, no duermas — re-lanza.
- **Off-by-one en el exponente**: usar `2^(i+1)` o empezar el backoff en `base·2^1` en vez de `base·2^0` → primera espera 2 en vez de 1.
- **No aplicar el tope** (`base·2^i` sin `min(tope, ...)`): la espera crece sin límite (esperar 17 minutos no sirve a nadie).
- **Jitter sobre el Retry-After**: el servidor dijo "vuelve en 8s"; sumarle jitter ignora la instrucción. El jitter es **solo** para el backoff calculado.
- **`except Exception`** que reintenta todo: convierte un `400`/`401` definitivo en 5 reintentos inútiles.
- **No re-lanzar la última excepción** al agotar (devolver `None` en silencio): el caller cree que tuvo éxito.
- (transversal) Usar `time.sleep`/`random` reales en vez de los inyectados → tests no deterministas y atados al reloj.

## Señales de dependencia-IA

> Describir sin acusar; proponer una verificación.

- Implementación correcta pero `prediccion.md` ausente o idéntica a las esperas reales (predijo "después").
- `verificacion.md` menciona "thundering herd" con precisión de manual pero, en seguimiento, no puede explicar **qué** pasaría sin jitter (todos reintentan al mismo segundo y vuelven a saturar).
- **Verificación sugerida:** pedir que prediga a mano un caso nuevo (p. ej. base=2, tope=10, 5 intentos, jitter 0) y que explique por qué el Retry-After se salta el tope.

## Feedback sugerido (graduado)

> Nunca pegar el código de la solución.

- **Pista (nivel 1):** "¿Tu bucle duerme también después del **último** intento? ¿Y qué pasa con el exponente en la primera espera — empieza en 2^0 o en 2^1?"
- **Pregunta socrática (nivel 2):** "Si el servidor te manda `Retry-After: 8`, ¿tiene sentido sumarle tu jitter aleatorio encima? ¿Quién sabe mejor cuándo volver, tú o el servidor?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Recorre `range(max_intentos)`; intenta y devuelve si funciona. Captura **solo** `ErrorReintentable`; cualquier otra excepción déjala propagar. Si es el último índice, sal del bucle y re-lanza. Si no: espera = `retry_after` si viene, si no `min(tope, base·2^i)` + jitter; `dormir(espera)`."

## Conexión con el proyecto / capstone

- Esta función es la capa de resiliencia del **Capstone F6 (RAG de producción)**: cuando el proveedor tira `429` bajo carga, es lo que mantiene la plataforma en pie en vez de caerse. Se conecta con la observabilidad (loguear cada intento + el `Retry-After`) y con el techo de costo/latencia del Definition of Done.
