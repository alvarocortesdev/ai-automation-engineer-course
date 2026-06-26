---
ejercicio_id: fase-3/cazar-n1
fase: fase-3
sub_unidad: "3.5"
version: 1
---

# Rúbrica — Caza y mata el N+1 con eager loading

> Rúbrica **analítica** atada a los `objetivos`. Evalúa `solucion.py` + `bitacora.md` con
> `test_acceptance.py` en verde. El test es objetivo: `test_no_hay_n_mas_1` cuenta las queries
> y exige ≤ 2; la versión lazy ejecuta 11 y falla. Pero pasar el test no basta — la `bitacora.md`
> debe mostrar que el alumno entiende **por qué** y sabe **elegir** la estrategia.

## Objetivos evaluados
- **O1** — Consulta sin N+1 (≤ 2 queries para N autores) que devuelve los datos correctos.
- **O2** — Elegir `joinedload` vs `selectinload` según la relación y justificar por escrito.
- **O3** — Diagnosticar el N+1 contando queries reales, no por intuición de tiempo.

## Criterios y niveles

### C1 — Corrección y ausencia de N+1 · mapea: O1, O3
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `test_datos_correctos` en rojo (estructura/datos mal) o la función no implementada. |
| **en-progreso** | Datos correctos pero `test_no_hay_n_mas_1` en rojo: sigue habiendo N+1 (usó lazy, accede a `.libros` en el bucle sin eager loading). |
| **competente** | Ambos tests en **verde**: datos correctos y ≤ 2 queries con eager loading explícito. |
| **excelente** | Verde + la `bitacora.md` reporta el conteo medido de la versión ingenua (11) vs la curada (1 o 2), demostrando que diagnosticó con números. |

### C2 — Disciplina de la estrategia · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No usa eager loading (pasa "de casualidad" reestructurando raro, o no pasa). |
| **en-progreso** | Usa eager loading pero con fallo: `joinedload` de la colección **sin** `.unique()` (revienta con `InvalidRequestError`), o elige sin entender. |
| **competente** | `selectinload(Autor.libros)` (2 queries) **o** `joinedload(Autor.libros).unique()` (1 query), correctamente aplicado. |
| **excelente** | Elige `selectinload` para la colección **y** lo argumenta (no multiplica filas, escala parejo en to-many); reconoce que `joinedload` aquí exige `.unique()`. |

### C3 — Comprensión demostrada (bitácora) · mapea: O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `bitacora.md` ausente o "usé selectinload" sin más. |
| **en-progreso** | Describe la estrategia pero no liga la elección al tipo de relación ni reporta conteos. |
| **competente** | Explica por qué eligió esa estrategia y reporta el conteo ingenua vs curada. |
| **excelente** | Conecta con costo/latencia (cada query = round-trip) y menciona que el conteo se vuelve un test de regresión (observabilidad/testing). |

## Errores típicos a marcar
- **Dejar el lazy loading:** `select(Autor)` y acceder a `.libros` en el bucle → 1+N. Es justo el bug del ejercicio; el test lo caza.
- **`joinedload` sin `.unique()`:** en SQLAlchemy 2.0, `session.scalars(...)` con `joinedload` de colección **lanza `InvalidRequestError`**. No es silencioso: hay que poner `.unique()`.
- **Eager loading global en el modelo** (`relationship(lazy="selectin")`) en vez de por consulta con `.options(...)`: penaliza todas las queries; no es lo que pide el ejercicio.
- **"Resolver" en Python** trayendo todo y filtrando: no reduce las queries, solo mueve el problema.
- **Confiar en el tiempo:** "va rápido, no hay N+1" — con 10 filas todo va rápido. El diagnóstico es el **conteo**, no el cronómetro.
- (transversal testing/observabilidad) no reportar en `bitacora.md` el conteo medido de la versión ingenua antes de curar.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Solución perfecta con `selectinload` pero `bitacora.md` que no explica la diferencia entre `joinedload` y `selectinload`, ni por qué uno necesita `.unique()`.
- Generalizaciones no pedidas (caché, paginación, async) impropias del enunciado.
- No sabe decir en qué **línea** nace cada query extra de la versión lazy.
- **Verificación sugerida:** pídele que prediga, sin correr, cuántas queries ejecutaría si cambiara `selectinload` por `joinedload` (1 en vez de 2) y por qué; y qué pasaría si quitara el `.options(...)` por completo (vuelve el 1+N).

## Feedback sugerido (graduado)
> Nunca pegar el cuerpo de la función antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Corre el test con tu versión lazy y lee el mensaje de `test_no_hay_n_mas_1`: te dice cuántas queries ejecutaste. ¿De dónde sale cada una?"
- **Pregunta socrática (nivel 2):** "¿En qué momento exacto SQLAlchemy va a la base por los libros de un autor? Si eso pasa dentro de tu bucle, ¿cuántas veces ocurre? ¿Cómo le pides los libros **antes** de iterar?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Añade `.options(selectinload(Autor.libros))` a tu `select(Autor)` y vuelve a contar (deben bajar a 2). Si prefieres `joinedload`, recuerda encadenar `.unique()` antes de `.all()`. Repasa 4.6–4.8 antes de la referencia."

## Conexión con el proyecto / capstone
- Es el patrón exacto que el capstone necesita en cada endpoint que liste recursos con relaciones. El conteo de queries se vuelve un **test de regresión** que protege la API de un N+1 futuro, y la cura vive idealmente en el **repositorio** (port de `3.9`).
