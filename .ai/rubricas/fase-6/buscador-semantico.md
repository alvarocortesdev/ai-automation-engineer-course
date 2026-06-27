---
ejercicio_id: fase-6/buscador-semantico
fase: fase-6
sub_unidad: "6.5"
version: 1
---

# Rúbrica — Buscador semántico desde cero (chunking + ranking + dedup)

> Rúbrica **analítica** atada a los `objetivos` del contrato. El corrector la usa con `INSTRUCCIONES-CORRECTOR.md`. No es una nota numérica: es un mapa de qué observar y cómo dar feedback. El objetivo de fondo no es que los tests compilen, sino que el alumno entienda **por qué el solape importa**, **por qué se rankea por coseno y no por palabra clave**, y que pueda defender el caso borde de `solape >= tam` (bucle infinito).

## Objetivos evaluados

- **O1** — Partir un documento en chunks de tamaño fijo con solape, manejando casos borde.
- **O2** — Rankear un corpus por similitud coseno y devolver el top-k ordenado.
- **O3** — Deduplicar vectores casi-idénticos con una estrategia greedy por umbral.

## Criterios y niveles

### C1 — Corrección del chunking · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `chunk_texto` no avanza `tam - solape` (usa `tam` como paso y pierde el solape, o avanza de a 1); o no parte nunca y devuelve el texto entero. |
| **en-progreso** | El paso es correcto pero falla un caso borde: no maneja texto vacío, o no valida `solape >= tam` (bucle infinito o paso negativo silencioso). |
| **competente** | Avanza `tam - solape`, devuelve un solo chunk si el texto es ≤ `tam`, lista vacía si el texto es vacío, y lanza `ValueError` cuando `solape >= tam`. Pasan los tests de chunking. |
| **excelente** | Además, código limpio (un solo bucle claro, corte explícito cuando `i + tam` cubre el resto) y el alumno explica **por qué** el solape evita partir una idea en el límite. |

### C2 — Corrección del ranking y la dedup · mapea: O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `buscar` no ordena, ordena ascendente, o pierde el índice original; `deduplicar` compara contra el vector anterior solamente (no contra todos los conservados) o usa `>` donde debe ser `>=`. |
| **en-progreso** | `buscar` correcto pero no recorta a `k` (o revienta si `k` > corpus); o `deduplicar` correcto pero `buscar` mal, o viceversa. |
| **competente** | `buscar` devuelve tuplas `(indice, score)` de mayor a menor recortadas a `k` (y todos si `k` > corpus); `deduplicar` conserva el primero y descarta los `>= umbral` contra cualquier conservado. Pasan los tests. |
| **excelente** | Reusa `similitud_coseno` en vez de reimplementar; `buscar` usa `sorted(..., key=..., reverse=True)` en vez de un bucle de burbuja improvisado. |

### C3 — Calidad de ingeniería (testing real) · mapea: O1, O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No agregó ningún test propio; confía en "se ve bien". |
| **en-progreso** | Agregó un test pero trivial (re-testea un caso ya cubierto). |
| **competente** | Agregó al menos un test de caso borde genuino (k=0, solape=0, dedup de lista vacía, chunk con una sola palabra). |
| **excelente** | El test propio captura un borde que el alumno razonó (p. ej. empate de scores: dos vectores con el mismo coseno) y explica por qué lo eligió. |

### C4 — Comprensión demostrada (el write-up calza con el código) · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No puede explicar por qué se busca por coseno y no por palabra clave, ni qué hace el solape. |
| **en-progreso** | Explica el coseno pero no por qué guarda la metadata del chunk aparte, o no entiende por qué consulta y corpus deben usar el mismo modelo. |
| **competente** | Explica que el coseno mide significado (dirección), que el solape conserva ideas en el límite, y que el texto del chunk se guarda aparte para responder/citar. |
| **excelente** | Conecta por iniciativa con cuándo la semántica falla (identificadores exactos → hybrid search) y con cómo esto alimenta el retrieval del Capstone RAG (hilo transversal). |

## Errores típicos a marcar

- **Paso de chunk = `tam`** (olvida restar el solape): los chunks no se solapan y se pierde la idea-en-el-límite.
- **No validar `solape >= tam`**: paso 0 o negativo → bucle infinito (el test lo atrapa, pero el alumno debe entender *por qué*).
- **`buscar` que pierde el índice**: devuelve solo scores ordenados y ya no se sabe a qué documento corresponden.
- **`buscar` que revienta con `k` > corpus** en vez de devolver todos.
- **`deduplicar` que compara solo contra el vector anterior**, no contra todos los conservados → deja pasar duplicados.
- **`deduplicar` con `>` en vez de `>=`** en el umbral (el test de umbral lo expone).
- **Umbral de coseno tratado como porcentaje** (creer que 0.8 = "80% relevante").
- (transversal) No añadir el caso borde propio; confiar en que "el número se ve bien" sin un test que fije el comportamiento.

## Señales de dependencia-IA

> Indicios de que el alumno usó IA para *pensar* en vez de *aprender*. Describir sin acusar; proponer verificación.

- Usa `numpy` (`np.dot`, `np.argsort`) pese a que el enunciado pide Python puro a mano.
- Implementación impecable con manejo de errores sofisticado pero **no sabe explicar** por qué el solape importa ni por qué la semántica falla con códigos exactos.
- Un chunking "creativo" (por oraciones con regex, por tokens reales) que no calza con el resto del estilo del alumno ni con lo pedido.
- **Verificación sugerida:** pídele que, sin correr código, diga cuántos chunks salen de un texto de 10 palabras con `tam=4, solape=1`. Si entendió el paso (`tam - solape = 3`), responde "empieza en 0, 3, 6, 9 → 4 chunks" al instante; si dependió de la IA, necesita ejecutar.

## Feedback sugerido (graduado)

> Ordenadas de menos a más directas. **Nunca incluir el código de la solución.**

- **Pista (nivel 1):** "Tu coseno y tu ranking se ven bien. Mira de nuevo cuánto avanza `i` en cada vuelta de `chunk_texto`: si el chunk mide `tam` palabras y quieres que se solapen, ¿cuánto deberías avanzar?"
- **Pregunta socrática (nivel 2):** "Si `solape` fuera igual a `tam`, ¿cuánto avanzaría `i` en cada vuelta? ¿Qué le pasa a tu bucle? Eso es justo lo que el `ValueError` previene."
- **Dirección concreta (nivel 3, sólo tras intento real):** "En `deduplicar`, comparar solo contra el vector inmediatamente anterior deja pasar duplicados que se parecen a uno más antiguo. Compara cada candidato contra **todos** los que ya conservaste, y descarta si el coseno llega o supera el umbral (`>=`, no `>`)."

## Conexión con el proyecto / capstone

- Este motor es el **ingest + retrieval** del **Capstone F6 (Plataforma RAG)**: el chunking decide la granularidad de lo que se recupera, y el ranking por coseno es exactamente lo que una vector DB (6.6) hará a escala. Quien lo implementó a mano puede diagnosticar por qué su RAG trae chunks irrelevantes (chunk mal cortado, umbral mal calibrado) en vez de quedar a ciegas frente a una librería.
