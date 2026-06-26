---
ejercicio_id: fase-3/migracion-reversible
fase: fase-3
sub_unidad: "3.4"
version: 1
---

# Rúbrica — Escribe una migración reversible con backfill

> Rúbrica **analítica** atada a los `objetivos` del contrato. Los tests verdes son **necesarios pero
> no suficientes**: un alumno puede pasarlos con un `downgrade` que "funciona de casualidad" o sin
> entender por qué el orden importa. La rúbrica mide el **modelo mental de migración**, no solo el
> color de la barra de pytest.

## Objetivos evaluados
- **O1** — Cambiar esquema y datos a la vez: agregar columnas y rellenarlas (backfill) desde una existente.
- **O2** — Escribir un `downgrade` que revierte sin perder ni alterar los datos originales (round-trip idéntico).
- **O3** — Explicar por qué el `ADD COLUMN` precede al `UPDATE` de backfill.

## Criterios y niveles

### C1 — Corrección de la migración (upgrade + backfill) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `upgrade` no agrega las columnas, o las agrega pero no rellena; el split está mal (apellido con espacio de más, o nombre y apellido cruzados). |
| **en-progreso** | Agrega y rellena, pero falla el caso sin apellido (deja `NULL` en vez de `""`), o asume siempre dos palabras y revienta con `"Cher"`. |
| **competente** | `upgrade` agrega `nombre`/`apellido` y los rellena correctamente para los tres casos (incluido el de un solo nombre → `apellido=""`); no toca `nombre_completo`. Tests de upgrade en verde. |
| **excelente** | Además maneja bordes no exigidos (espacios dobles, string en blanco) con `str.split(None, 1)` —que los resuelve gratis— y lo comenta; backfill en una sola pasada eficiente. |

### C2 — Reversibilidad (downgrade + round-trip) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `downgrade`, o borra/altera `nombre_completo` (pérdida de datos), o deja columnas colgando. |
| **en-progreso** | `downgrade` quita las columnas nuevas pero el round-trip no queda idéntico (p. ej. olvida `commit`, o deja una columna). |
| **competente** | `downgrade` deja la tabla exactamente como estaba (`id` + `nombre_completo` con datos intactos); el round-trip `upgrade`→`downgrade` y el repetible pasan. |
| **excelente** | Articula por qué *este* cambio es reversible (porque `nombre_completo` nunca se borra) y reconoce que un `DROP COLUMN nombre_completo` haría el downgrade irrecuperable. |

### C3 — Calidad de ingeniería y test propio (testing) · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No agregó test propio; código que no corre o con firmas cambiadas. |
| **en-progreso** | Agregó un test trivial que repite uno existente, sin pensar un borde nuevo. |
| **competente** | Agregó al menos un test con un caso borde genuino (espacios dobles, tres palabras, solo espacios) y pasa. |
| **excelente** | El test propio captura un borde real del split y el alumno explica qué garantiza; usa `conn.commit()` donde corresponde y la solución es legible. |

### C4 — Comprensión demostrada (el porqué del orden) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No puede explicar por qué `ADD COLUMN` va antes del `UPDATE`. |
| **en-progreso** | Dice "porque sí" o "porque lo pedía el enunciado", sin el mecanismo. |
| **competente** | Explica que no se puede escribir en una columna que aún no existe; el `UPDATE` fallaría con "no such column". |
| **excelente** | Conecta con la migración real: esquema y datos son fases distintas; en Alembic es lo mismo, y por eso una migración de datos importa una tabla "ligera" en vez del modelo vivo. |

## Errores típicos a marcar
- **`apellido` queda `NULL` en vez de `""`** para nombres de una sola palabra (no leyó el contrato del split).
- **Asumir siempre dos palabras** (`split(" ")[1]`) → `IndexError` con `"Cher"`.
- **Usar `split(" ")` en vez de `split(None, 1)`** → "Grace Murray Hopper" parte mal o deja espacios.
- **Borrar o tocar `nombre_completo`** en el upgrade o el downgrade → pérdida de datos, round-trip roto.
- **Olvidar `conn.commit()`** → cambios no persistidos, tests intermitentes.
- (transversales) tests verdes pero sin test propio; no poder defender el orden esquema→datos.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Solución que usa una API rebuscada (regex, librería externa) para algo que `str.split(None, 1)` resuelve, impropia del nivel, pero el alumno no puede explicar el caso `"Cher"`.
- `downgrade` "perfecto" pero el alumno no sabe decir por qué este cambio es reversible y un drop de `nombre_completo` no lo sería.
- **Verificación sugerida:** pídele que prediga, sin correr nada, qué pasa si invierte el orden (UPDATE antes de ADD COLUMN). Quien entendió dice "falla: no such column"; quien dependió de la IA duda.

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "¿En qué orden tienen que pasar las dos cosas? No puedes llenar un vaso que todavía no existe. Mira tu `upgrade`: ¿qué hace primero?"
- **Pregunta socrática (nivel 2):** "Para `"Cher"`, ¿cuántos elementos te devuelve tu forma de partir el nombre? ¿Y qué pones en `apellido` si solo hay uno? ¿Es `""` o `None`?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Usa `partes = nombre_completo.split(None, 1)`; `nombre = partes[0]`, `apellido = partes[1] if len(partes) > 1 else ''`. Para el downgrade, recuerda que reviertes quitando solo las columnas nuevas, porque `nombre_completo` sigue intacto."

## Conexión con el proyecto / capstone
- Este es el patrón de migración (esquema + datos, reversible) que el **Capstone F3 — API de producción** exige tener versionado con Alembic. Dominar el round-trip aquí es lo que evita que una migración rota bote el servicio del capstone.
