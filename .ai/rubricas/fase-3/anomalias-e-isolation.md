---
ejercicio_id: fase-3/anomalias-e-isolation
fase: fase-3
sub_unidad: "3.3"
version: 1
---

# Rúbrica — Diagnosticar anomalías y elegir el isolation level

> Rúbrica **analítica** atada a los `objetivos`. Es un ejercicio de razonamiento: evalúa el
> `analisis.md` del alumno contra los tres escenarios de `escenarios.md`. La pieza que más
> revela dominio es la **justificación**, no la etiqueta: "es phantom" sin explicar el
> entrelazado no demuestra nada. Mira los tres escenarios juntos.

## Objetivos evaluados
- **O1** — Nombrar la anomalía correcta a partir del patrón del entrelazado.
- **O2** — Predecir si ocurre bajo `READ COMMITTED` y bajo `REPEATABLE READ` en Postgres.
- **O3** — Elegir el nivel/técnica **mínimo** que la resuelve y justificar el trade-off.

## Criterios y niveles

### C1 — Identificación de la anomalía · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Etiquetas equivocadas (ej. llama "lost update" al escenario 3, que es write skew) o sin justificar. |
| **en-progreso** | Acierta 1–2 de 3, o acierta la etiqueta pero la justificación no describe el entrelazado. |
| **competente** | Las tres anomalías correctas (1: non-repeatable read; 2: lost update; 3: write skew) y justificadas con la línea de tiempo. |
| **excelente** | Además distingue por qué el escenario 3 NO es un lost update (filas distintas, no se pisan) sino una invariante violada entre transacciones. |

### C2 — Comportamiento por isolation level · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Cree que `READ COMMITTED` ya evita non-repeatable/phantom, o que `REPEATABLE READ` permite phantom en Postgres. |
| **en-progreso** | Sabe el default pero confunde qué corta cada nivel en al menos un escenario. |
| **competente** | Correcto: esc.1 lo corta `REPEATABLE READ`; esc.2 (lost update) NO lo arregla subir a `REPEATABLE READ` en silencio (da `40001`); esc.3 SOLO lo evita `SERIALIZABLE`. |
| **excelente** | Menciona explícitamente que `REPEATABLE READ` de Postgres es más estricto que el estándar (sin phantom) y por qué. |

### C3 — Elección mínima + trade-off · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | "Todo a `SERIALIZABLE`" sin más, o una técnica que no resuelve el caso. |
| **en-progreso** | Elige un nivel que funciona pero no el mínimo, o no nombra el costo. |
| **competente** | Nivel/técnica mínimo por escenario (esc.2: aritmética atómica o `FOR UPDATE` sin subir nivel) + costo en 1–2 frases. |
| **excelente** | Compara alternativas (ej. `FOR UPDATE` vs subir a `SERIALIZABLE` para esc.2) y defiende la elección por contención/simplicidad. |

## Errores típicos a marcar
- **Confundir lost update con write skew:** el escenario 2 pisa la **misma** fila (lost update); el 3 toca filas **distintas** que juntas rompen una invariante (write skew). Es el error conceptual más común.
- **Creer que `READ COMMITTED` repite lecturas:** en el escenario 1, las dos lecturas de A difieren porque B confirmó en medio — eso es exactamente non-repeatable read.
- **Pensar que `REPEATABLE READ` permite phantom en Postgres:** NO los permite (más estricto que el estándar SQL).
- **"Subir a `SERIALIZABLE` arregla el lost update sin tocar la app":** lo convierte en error `40001`, que la app DEBE reintentar; no es transparente.
- **Olvidar la aritmética atómica como opción:** para el escenario 2, `UPDATE ... SET stock = stock - 1 WHERE id = ... AND stock > 0` resuelve sin locks ni subir nivel; es la primera opción que un senior considera.
- (transversal spec-driven) elegir un nivel sin nombrar la invariante de negocio que se quiere proteger.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Análisis que usa vocabulario perfecto ("predicate locks", "SSI", "EvalPlanQual") pero no puede decir, en el escenario concreto, **quién leyó qué y cuándo**.
- Las tres respuestas con la misma estructura copiada y cero referencia a las líneas específicas de cada escenario.
- **Verificación sugerida:** pídele que prediga, sin notas, qué pasa en el escenario 3 si ambos médicos corren bajo `SERIALIZABLE` (uno confirma, el otro recibe `40001` y al reintentar ve count=1, así que ya no se da de baja). Si no lo sabe reconstruir, la etiqueta fue memorizada, no entendida.

## Feedback sugerido (graduado)
> Nunca dar la tabla resuelta antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Para cada escenario, dibuja la línea de tiempo: ¿quién lee, quién escribe, quién confirma y en qué orden? La anomalía sale del patrón, no de las tablas."
- **Pregunta socrática (nivel 2):** "En el escenario 3, ¿los dos `UPDATE` tocan la misma fila? Si no se pisan, ¿por qué se rompe la regla 'al menos 1 de turno'? ¿Qué tendría que haber visto cada transacción para no darse de baja?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Esc.1 = non-repeatable (lo corta `REPEATABLE READ`: snapshot por transacción). Esc.2 = lost update (aritmética atómica `SET stock = stock - 1` o `FOR UPDATE`; subir nivel solo lo vuelve `40001`). Esc.3 = write skew (SOLO `SERIALIZABLE` lo evita, porque cruza filas distintas). Repasa la sección 4.4 antes de mirar la referencia."

## Conexión con el proyecto / capstone
- Cada endpoint del capstone que escribe un recurso compartido necesita esta decisión documentada en un ADR. Saber elegir el nivel mínimo (no `SERIALIZABLE` para todo) es lo que mantiene la API rápida y correcta a la vez.
