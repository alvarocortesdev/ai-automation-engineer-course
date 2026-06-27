---
ejercicio_id: fase-6/recall-y-filtrado
fase: fase-6
sub_unidad: "6.6"
version: 1
---

# Rúbrica — Recall de un índice + filtrado por metadata (pre vs post)

> Rúbrica **analítica** atada a los `objetivos` del contrato. El corrector la usa con `INSTRUCCIONES-CORRECTOR.md`. No es una nota numérica. El objetivo de fondo no es que los tests pasen, sino que el alumno entienda **qué mide recall@k y por qué un índice ANN no es exacto**, y que pueda explicar **por qué el post-filter ingenuo es un bug de retrieval y, con `tenant_id`, una fuga de datos**.

## Objetivos evaluados

- **O1** — Implementar la búsqueda exacta por fuerza bruta como ground truth del recall.
- **O2** — Calcular recall@k contra el ground truth, manejando el borde de ground truth vacío.
- **O3** — Implementar filtrado por metadata en modos pre y post, demostrando por qué el post-filter puede devolver menos de `k`.

## Criterios y niveles

### C1 — Corrección de búsqueda exacta y recall · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `buscar_exacto` no ordena descendente o pierde el índice original; o `recall_at_k` divide por cero con ground truth vacío. |
| **en-progreso** | `buscar_exacto` correcto pero `recall_at_k` cuenta mal (usa `len(ids_aprox)` como denominador en vez de `len(ids_exactos)`, o no usa intersección de conjuntos). |
| **competente** | `buscar_exacto` devuelve top-k `(indice, score)` descendente (todos si `k` > corpus); `recall_at_k` = intersección / `len(ids_exactos)`, y devuelve `1.0` si el ground truth es vacío. Pasan los tests. |
| **excelente** | Reusa `similitud_coseno`; usa `set(...)` para la intersección; el alumno explica que recall@k mide "qué fracción de los vecinos verdaderos recuperó el índice" y por qué un ANN tiene recall menor que 1.0. |

### C2 — Corrección del filtrado pre vs post · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Ambos modos hacen lo mismo, o el `"post"` filtra **antes** (no demuestra el bug), o se pierde el índice original (devuelve la posición dentro del subconjunto filtrado). |
| **en-progreso** | Un modo correcto y el otro no; o el `where` solo soporta una clave fija en vez de "todas las claves deben calzar". |
| **competente** | `"pre"` filtra el corpus y rankea solo lo que cumple (hasta `k`); `"post"` rankea el top-k global y luego descarta (puede dar menos de `k`); índices originales conservados. Pasan los tests. |
| **excelente** | `where` general con `all(...)` sobre las claves; el alumno conecta por iniciativa el post-filter con el riesgo multi-tenant (filtrado = control de seguridad). |

### C3 — Calidad de ingeniería (testing real) · mapea: O1, O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No agregó ningún test propio. |
| **en-progreso** | Agregó un test trivial (re-testea un caso ya cubierto). |
| **competente** | Agregó al menos un caso borde genuino (recall con extras en `ids_aprox`, `where` de dos claves, post-filter donde ningún top-k cumple). |
| **excelente** | El test propio captura un borde que el alumno razonó y explica por qué lo eligió. |

### C4 — Comprensión demostrada (el write-up calza con el código) · mapea: O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No puede explicar qué es recall@k ni por qué el post-filter puede devolver menos de `k`. |
| **en-progreso** | Explica recall pero no la dimensión de **seguridad** del filtrado (tenant). |
| **competente** | Explica recall@k, por qué un ANN no es exacto, y por qué el post-filter ingenuo es un bug de retrieval. |
| **excelente** | Conecta con HNSW/IVFFlat (recall se tunea con `ef`/`probes`) y con 6.14 (post-filter de `tenant_id` = fuga de datos). |

## Errores típicos a marcar

- **`recall_at_k` con denominador equivocado**: divide por `len(ids_aprox)` en vez de `len(ids_exactos)` (eso es *precision*, no *recall*).
- **Ground truth vacío → ZeroDivisionError**: no maneja el borde.
- **`"post"` que filtra antes de rankear**: no reproduce el bug; entonces no entendió la diferencia.
- **Perder el índice original** en `buscar_con_filtro`: devuelve la posición dentro del subconjunto filtrado.
- **`where` que solo compara una clave fija** en vez de exigir que todas calcen.
- Tratar recall como porcentaje de relevancia subjetiva (no: es fracción de vecinos verdaderos recuperados).

## Señales de dependencia-IA

> Indicios de que el alumno usó IA para *pensar* en vez de *aprender*. Describir sin acusar; proponer verificación.

- Usa `numpy` (`np.argsort`, `np.intersect1d`) pese a que el enunciado pide Python puro a mano.
- Implementación impecable pero **no sabe explicar** por qué el post-filter devuelve menos de `k`, ni la diferencia recall/precision.
- Confunde *precision* y *recall* en el write-up aunque el código esté bien (señal de copiar sin entender).
- **Verificación sugerida:** pídele que, sin correr código, diga cuántos resultados devuelve el `test_postfilter_puede_devolver_menos_de_k` y por qué. Si entendió, responde "1, porque idx2 del top-2 global es 'gatos' y cae"; si dependió de la IA, necesita ejecutar.

## Feedback sugerido (graduado)

> Ordenadas de menos a más directas. **Nunca incluir el código de la solución.**

- **Pista (nivel 1):** "Tu `buscar_exacto` se ve bien. En `recall_at_k`, ¿el denominador es cuántos trajo el aproximado, o cuántos había que encontrar? Esa elección decide si mides recall o precision."
- **Pregunta socrática (nivel 2):** "En modo `"post"`, ¿en qué momento aplicas el filtro: antes o después de tomar el top-k global? Si lo aplicas después, ¿qué pasa cuando varios del top-k no cumplen el `where`?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "El bug del post-filter está en el orden: rankea TODO, recorta a `k`, y recién entonces descarta los que no cumplen. Por eso puede quedar con menos de `k`. El pre-filter invierte el orden: filtra el corpus primero y rankea solo eso. Asegúrate de conservar el índice original del documento en ambos casos."

## Conexión con el proyecto / capstone

- Este motor es la lógica que una vector DB hace por ti en el **Capstone F6 (Plataforma RAG)**: el `recall@k` es la métrica que tu [eval harness](/fase-6-ai-engineering/6-9-eval-driven-development/) reportará sobre el retrieval, y el pre/post-filter es exactamente la decisión de seguridad/relevancia que tomarás al filtrar por tenant o por fuente. Quien lo implementó a mano puede diagnosticar "mi RAG devuelve pocos/los equivocados" en vez de quedar a ciegas frente a una librería.
