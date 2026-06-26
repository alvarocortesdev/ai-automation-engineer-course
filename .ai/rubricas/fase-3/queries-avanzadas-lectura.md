---
ejercicio_id: fase-3/queries-avanzadas-lectura
fase: fase-3
sub_unidad: "3.2"
version: 1
---

# Rúbrica — Lee y diagnostica: JOINs, NULLs y window functions

> Rúbrica **analítica** atada a los `objetivos` del contrato. Lo que se evalúa no es solo si las
> tablas predichas coinciden, sino si el alumno **razona el porqué**: por qué Dani da 0 (no 1), por
> qué el `WHERE` rompe el outer join, y qué decide el tipo de JOIN. Un alumno puede acertar la 1 de
> memoria y aun así no entender el mecanismo. La rúbrica separa "acertó el número" de "entendió".

## Objetivos evaluados
- **O1** — Predecir la salida de `LEFT JOIN` + `COUNT` y de window functions (`RANK`, `SUM OVER`) sin ejecutar.
- **O2** — Diagnosticar y corregir el `WHERE` que degrada un `LEFT JOIN` a `INNER`.
- **O3** — Decidir el tipo de JOIN según qué filas sin pareja deben sobrevivir.

## Criterios y niveles

### C1 — Corrección de las predicciones (P1 y P4) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Falta una de las dos tablas, o da descripciones sin valores. En P1 pone Dani = 1 (no entiende `COUNT(p.id)`). |
| **en-progreso** | Acierta P1 pero falla P4 (confunde `RANK` con `ROW_NUMBER`, o el acumulado no es corriente sino el total de la región). |
| **competente** | P1 correcta (Ana 2, Beto 1, Cora 2, Dani 0) y P4 correcta (RANK por región y acumulado corriente por mes). |
| **excelente** | Además anota *por qué* cada valor: "Dani 0 porque COUNT ignora el NULL"; "acumulado = total corriente por el `ORDER BY mes` dentro del OVER". |

### C2 — Diagnóstico del bug del outer join (P2) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No identifica la causa; "corrige" agregando otra tabla o un `OR`, o no recupera a Dani. |
| **en-progreso** | Intuye que es por el NULL pero no nombra que el `WHERE` degradó el `LEFT` a `INNER`; la corrección no es mover al `ON`. |
| **competente** | Explica que la fila fantasma de Dani tiene `fecha_devolucion = NULL`, `NULL IS NOT NULL` es falso → se cae; corrige moviendo la condición al `ON`. |
| **excelente** | Articula la regla general: condición sobre la tabla preservada de un outer join → `ON`; filtro del resultado final → `WHERE`. |

### C3 — Decisión de JOIN justificada (P3) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Elige tipos al azar o sin justificar; (a) con INNER, (c) con LEFT. |
| **en-progreso** | Acierta tipos pero justifica con "porque sí" o "es lo común", no por las filas sin pareja. |
| **competente** | (a) LEFT (conservar socios con 0), (b) INNER (solo préstamos con socio), (c) FULL (huérfanos en ambos lados); cada una con el porqué correcto. |
| **excelente** | En (a) nota que necesita filtrar "no devueltos" en el `ON`, no en el `WHERE`, para no repetir el bug de P2; en (b) reconoce que el INNER ya excluye lo no emparejado. |

## Errores típicos a marcar
- **Dani = 1 en P1**: confunde `COUNT(*)` con `COUNT(columna)`; no internalizó que `COUNT` de columna ignora NULL.
- **"Corregir" P2 con `WHERE ... OR p.libro IS NULL`**: parche frágil; la corrección idiomática es mover la condición al `ON`.
- **P4 con acumulado = total de la región** (350 para Norte en todas las filas): ignora que el `ORDER BY` dentro del `OVER` crea un marco corriente, no global.
- **Confundir `RANK` y `ROW_NUMBER`** en P4: aquí no hay empates en `ventas`, así que coinciden — si el alumno no lo nota, preguntarle qué pasaría con un empate.
- **(c) con LEFT en vez de FULL**: no ve que "huérfanos en *ambos* lados" exige FULL.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Tablas predichas perfectas pero sin una sola línea de razonamiento (resultado sin proceso) — sospechoso de haber ejecutado o pedido a una IA antes de predecir.
- Usa vocabulario avanzado ("anti-join", "marco RANGE/ROWS") pero no puede explicar por qué Dani da 0.
- La corrección de P2 es exactamente la forma canónica pero la explicación del *porqué* es genérica o no calza.
- **Verificación sugerida:** pedir que prediga, en voz alta, qué pasaría con P1 si se cambiara `COUNT(p.id)` por `COUNT(*)`. Quien entendió dice "Dani pasa a 1"; quien dependió de la IA se traba.

## Feedback sugerido (graduado)
> Nunca dar la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "En P1, mira la fila de Dani tras el LEFT JOIN: ¿qué hay en `p.id`? ¿Y qué cuenta `COUNT` de una columna cuando el valor es NULL?"
- **Pregunta socrática (nivel 2):** "En P2, ¿qué valor tiene `p.fecha_devolucion` en la fila que el LEFT JOIN inventa para Dani? Evalúa `NULL IS NOT NULL`. ¿Dónde tendría que ir esa condición para no borrar esa fila?"
- **Dirección concreta (nivel 3, solo tras intento real):** "La regla: en un outer join, la condición que describe la tabla que quieres conservar va en el `ON`; lo que filtra el resultado final va en el `WHERE`. Reescribe P2 con la condición en el `ON` y comprueba que Dani vuelve con `libro` NULL."

## Conexión con el proyecto / capstone
- Leer y diagnosticar JOINs/NULLs es exactamente lo que harás revisando queries (propias, de un ORM o de una IA) detrás de los endpoints del **Capstone F3 — API de producción**. El bug del `WHERE` que degrada el outer join es uno de los más caros y silenciosos en producción.
