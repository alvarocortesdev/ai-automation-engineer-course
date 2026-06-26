---
ejercicio_id: fase-3/carrera-stock-locking
fase: fase-3
sub_unidad: "3.3"
version: 1
---

# Rúbrica — Resolver la carrera del stock: pesimista vs optimista

> Rúbrica **analítica** atada a los `objetivos`. Evalúa `solucion.py` + `bitacora.md` con
> `test_acceptance.py` en verde (requiere Postgres). El test es duro: si hay lost update,
> se venden más de 50 o el stock queda negativo. Pero pasar el test no basta — la
> `bitacora.md` debe mostrar que el alumno entiende **por qué** cada estrategia funciona y
> cuándo elegir cuál.

## Objetivos evaluados
- **O1** — Locking pesimista con `SELECT ... FOR UPDATE` que evita overselling.
- **O2** — Locking optimista con `version` + reintento con tope ante `rowcount == 0`.
- **O3** — Justificar cuál conviene según la contención (baja vs alta).

## Criterios y niveles

### C1 — Corrección bajo concurrencia · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Alguna estrategia vende ≠ 50 o deja stock negativo (`test_acceptance.py` en rojo). |
| **en-progreso** | Una de las dos pasa; la otra falla o entra en loop infinito / agota reintentos. |
| **competente** | Ambas en **verde**: exactamente 50 ventas, stock final 0, nunca negativo. |
| **excelente** | Verde + código limpio: la pesimista valida dentro del lock; la optimista re-lee dentro del loop y tiene tope explícito. |

### C2 — Disciplina de cada estrategia · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | "Pesimista" sin `FOR UPDATE` (solo `SELECT`+`UPDATE`), u "optimista" sin la guarda `WHERE version = ...`. Pasa por casualidad o no pasa. |
| **en-progreso** | Usa los mecanismos pero con fallos: optimista que no re-lee la `version` dentro del loop, o pesimista que decrementa sin revalidar stock. |
| **competente** | Pesimista: `FOR UPDATE` + validación de stock dentro de la misma transacción. Optimista: re-lee y reintenta ante `rowcount == 0`, con tope. |
| **excelente** | Aritmética del decremento en SQL (`stock = stock - 1`), no recalculada en Python con un valor viejo; maneja el caso `stock <= 0` antes de escribir. |

### C3 — Criterio de elección · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `bitacora.md` ausente o "las dos hacen lo mismo". |
| **en-progreso** | Describe ambas pero no liga la elección a la contención. |
| **competente** | Argumenta: baja contención → optimista (sin locks, más throughput); alta contención → pesimista (serializa, evita tormenta de reintentos). |
| **excelente** | Menciona alternativas (aritmética atómica `WHERE stock > 0`, `FOR UPDATE SKIP LOCKED` para colas) y el costo de deadlock del pesimista. |

## Errores típicos a marcar
- **"Pesimista" sin `FOR UPDATE`:** un `SELECT` normal no bloquea; bajo concurrencia se cuela el lost update. El `FOR UPDATE` es lo que serializa el acceso a la fila.
- **Recalcular el stock en Python:** `nuevo = stock - 1; UPDATE SET stock = nuevo` reintroduce la ventana. Mejor `SET stock = stock - 1` en SQL (aunque dentro de `FOR UPDATE` el cálculo en Python ya es seguro, el hábito de hacerlo en SQL es el correcto).
- **Optimista sin re-leer en el loop:** reintentar con la misma `version` vieja nunca avanza (loop hasta agotar el tope).
- **Sin tope de reintentos:** `while True` bajo alta contención puede no terminar; el test lo penaliza si excede el tope o cuelga.
- **Confundir el lock de conexión con el de fila:** el `with pool.connection()` no bloquea la fila; lo hace `FOR UPDATE`. Sin él, dos conexiones leen el mismo valor.
- **No devolver `False` cuando no hay stock:** vender de más o lanzar excepción en vez de retornar `False`.
- (transversal testing) no agregar a `bitacora.md` la observación de qué pasó si probó la versión "ingenua" (sin protección) y vio el overselling.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Código perfecto en ambas funciones pero `bitacora.md` que no explica **por qué** el `FOR UPDATE` libera el lock recién en el commit, ni qué es `rowcount == 0`.
- Generalizaciones no pedidas (reintentos con backoff exponencial, métricas, decoradores) impropias del enunciado.
- No sabe explicar por qué un `SELECT` + `UPDATE` sin protección falla el test (señal de que no razonó el entrelazado).
- **Verificación sugerida:** pídele que prediga, sin correr, qué pasaría si en la optimista quitara el `AND version = %s` del `UPDATE` (vuelve el lost update: ambos decrementan desde el mismo valor leído). Y que diga, en la pesimista, en qué línea exacta espera el segundo hilo.

## Feedback sugerido (graduado)
> Nunca pegar el cuerpo de las funciones antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "¿Tu versión 'pesimista' tiene literalmente las palabras `FOR UPDATE` en el `SELECT`? Si no, dos hilos leen el mismo stock y ninguno espera al otro."
- **Pregunta socrática (nivel 2):** "En la optimista, cuando tu `UPDATE ... WHERE version = 7` afecta 0 filas, ¿qué significa eso sobre lo que pasó entre tu lectura y tu escritura? ¿Con qué `version` deberías reintentar — la 7 que ya leíste, o una nueva lectura?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Pesimista: `SELECT stock FROM eventos WHERE id=%s FOR UPDATE`, valida `stock > 0`, `UPDATE ... SET stock = stock - 1`. Optimista: en un loop con tope, `SELECT stock, version`, y `UPDATE ... SET stock = stock-1, version = version+1 WHERE id=%s AND version=%s`; si `cur.rowcount == 0`, re-lee y reintenta. Repasa 4.7 antes de la referencia."

## Conexión con el proyecto / capstone
- Es el patrón exacto que el capstone necesita en cualquier endpoint que decremente stock/saldo/cupos. La elección pesimista vs optimista, justificada por contención, es material de ADR — y la base sobre la que se monta la idempotencia de `3.14`.
