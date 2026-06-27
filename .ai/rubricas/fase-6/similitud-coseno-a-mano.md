---
ejercicio_id: fase-6/similitud-coseno-a-mano
fase: fase-6
sub_unidad: "6.0"
version: 1
---

# Rúbrica — Similitud coseno desde cero (y un mini-retriever)

> Rúbrica **analítica** atada a los `objetivos` del contrato. El corrector la usa con `INSTRUCCIONES-CORRECTOR.md`. No es una nota numérica: es un mapa de qué observar y cómo dar feedback. El objetivo de fondo no es que la fórmula compile, sino que el alumno **entienda por qué coseno y no producto punto**, y que pueda defender el caso borde del vector cero.

## Objetivos evaluados

- **O1** — Implementar a mano producto punto, magnitud y similitud coseno entre vectores.
- **O2** — Usar la similitud coseno para rankear documentos por parecido a una consulta.
- **O3** — Manejar el caso borde del vector cero sin dividir por cero.

## Criterios y niveles

### C1 — Corrección de las operaciones (¿hace lo que el objetivo pide?) · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `producto_punto` o `magnitud` mal (suma en vez de multiplica, olvida la raíz); o `similitud_coseno` no divide por las dos magnitudes; los tests no pasan. |
| **en-progreso** | Las operaciones básicas están bien pero `rankear` no ordena, ordena al revés, o pierde el índice original; falla algún test de orden. |
| **competente** | Las cuatro funciones pasan todos los tests: coseno da ~0.999 y ~0.25 en el caso de la lección, y `rankear` devuelve tuplas `(indice, similitud)` de mayor a menor. |
| **excelente** | Además, código limpio y reusable (coseno se apoya en `producto_punto` y `magnitud`, no reimplementa), y `rankear` usa `sorted` con `key` en vez de un bucle de burbuja improvisado. |

### C2 — Manejo de casos borde y errores · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | El vector cero revienta con `ZeroDivisionError`; vectores de distinto largo dan resultado silencioso erróneo. |
| **en-progreso** | Maneja un caso borde (p. ej. distinto largo) pero no el otro (vector cero), o lo maneja devolviendo un valor raro (0, None) en vez de lanzar `ValueError`. |
| **competente** | Vector cero y distinto largo lanzan `ValueError` con mensaje claro, **antes** de operar; los tests de error pasan. |
| **excelente** | Mensajes de error que nombran el problema concreto (cuál vector, qué largos), y el chequeo de magnitud cero ocurre una sola vez de forma legible. |

### C3 — Comprensión demostrada (el write-up/explicación calza con el código) · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No puede explicar por qué se divide por las magnitudes, ni qué significa un coseno de 0 vs 1. |
| **en-progreso** | Explica la fórmula pero no la **intuición** (por qué coseno y no producto punto). |
| **competente** | Explica que el coseno normaliza la magnitud para medir solo dirección (significado), y por qué eso importa en búsqueda semántica. |
| **excelente** | Da el contraejemplo de la magnitud por iniciativa (un documento "más largo" gana en producto punto pero no en coseno), conectándolo con por qué el RAG usa coseno (hilo transversal: evals). |

## Errores típicos a marcar

- **Suma en vez de multiplica** en el producto punto (`a[i] + b[i]`), o magnitud sin la raíz.
- **Coseno dividido por una sola magnitud** o por `|a| + |b|` en vez de `|a| · |b|`.
- **Vector cero sin proteger**: `ZeroDivisionError` en lugar de `ValueError`; o "parchear" devolviendo 0.0 (oculta un dato inválido).
- **`rankear` que pierde el índice**: devuelve solo similitudes ordenadas y ya no se sabe a qué documento corresponden.
- **Ordenar ascendente** por descuido (`reverse=True` olvidado) y entregar el menos parecido primero.
- (transversal) Confiar en que "el número se ve bien" sin un test que fije el comportamiento; no añadir el caso borde propio.

## Señales de dependencia-IA

> Indicios de que el alumno usó IA para *pensar* en vez de *aprender*. Describir sin acusar; proponer verificación.

- Usa `numpy` (`np.dot`, `np.linalg.norm`) pese a que el enunciado pide Python puro a mano: señal de copiar una respuesta genérica sin hacer la operación.
- Código impecable con manejo de errores sofisticado pero el alumno **no sabe explicar** por qué coseno ignora la magnitud.
- Comentarios o nombres en inglés mezclados con un estilo que no calza con el resto de su trabajo.
- **Verificación sugerida:** pídele que calcule a mano, en 2 minutos y sin correr código, el coseno de `[2, 0]` y `[0, 3]`. Si entendió, dice 0 al instante (perpendiculares); si dependió de la IA, necesita ejecutar.

## Feedback sugerido (graduado)

> Ordenadas de menos a más directas. **Nunca incluir el código de la solución.**

- **Pista (nivel 1):** "Tu producto punto y magnitud están bien. Mira de nuevo la línea de `similitud_coseno`: ¿por qué entre QUÉ exactamente estás dividiendo?"
- **Pregunta socrática (nivel 2):** "Si tomo tu documento y lo hago 'el doble de largo' (cada coordenada × 2), ¿debería cambiar su parecido con la consulta? ¿Tu fórmula respeta eso? Pruébalo con `[1,2]` y `[2,4]`."
- **Dirección concreta (nivel 3, sólo tras intento real):** "El vector cero no tiene dirección, así que su coseno no está definido. Detecta magnitud 0 **antes** de dividir y lanza `ValueError`; un parche que devuelve 0.0 esconde un dato inválido que después te muerde en el RAG."

## Conexión con el proyecto / capstone

- Esta operación es la etapa *retrieval* del **Capstone F6 (Plataforma RAG)**: comparar el embedding de la pregunta con el de cada fragmento. Quien la implementó a mano puede depurar por qué su RAG trae fragmentos irrelevantes (umbral, normalización), en vez de quedar a ciegas frente a una librería.
