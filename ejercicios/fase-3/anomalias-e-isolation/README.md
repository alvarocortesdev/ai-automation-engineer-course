# Ejercicio 3.3 — Diagnosticar anomalías y elegir el isolation level

> **Modalidad: a mano (razonamiento, sin ejecutar, sin IA).** Este ejercicio entrena el músculo que un entrevistador busca en 30 segundos: ¿sabes qué le pasa a tus datos cuando dos transacciones se cruzan? No hay código que correr; hay entrelazados que leer y decisiones que justificar.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.3` PostgreSQL a fondo
**Ruta:** crítica · **Timebox:** 30–40 min

## 🎯 Objetivo

Dado un entrelazado de dos sesiones concurrentes, **nombrar la anomalía** (dirty read / non-repeatable / phantom / lost update / write skew), **predecir** si ocurre bajo `READ COMMITTED` y bajo `REPEATABLE READ`, **elegir el isolation level (o técnica) mínimo** que la resuelve, y **justificar el trade-off**.

## 📋 Contexto

Cada endpoint del capstone que modifica un recurso compartido (stock, saldo) puede sufrir una de estas anomalías. Elegir el nivel correcto —ni de menos (bug en producción) ni de más (`SERIALIZABLE` para todo = reintentos y latencia que no necesitabas)— es una decisión de diseño que va a un ADR. Aquí la practicas en seco.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Dibuja la línea de tiempo de cada escenario.
2. Solo entonces, consulta la **documentación oficial** (Transaction Isolation de Postgres).
3. **Solo al final**, usa IA para *revisar y explicar* tu análisis — no para generarlo.
4. Mañana, **reconstruye de memoria** la tabla anomalía × nivel.

## 🛠️ Instrucciones

1. Abre `escenarios.md`: tiene **tres** escenarios de dos sesiones (A y B) con sus pasos en orden temporal.
2. Para **cada** escenario, escribe en `analisis.md`:
   - **(1) Anomalía:** nómbrala y explica *por qué* es esa (no solo la etiqueta — el patrón del entrelazado).
   - **(2) ¿Ocurre bajo `READ COMMITTED`? ¿Y bajo `REPEATABLE READ`?** Sí/No con una frase de justificación cada uno.
   - **(3) Solución mínima:** el isolation level más bajo que basta, **o** la técnica (aritmética atómica `SET x = x - 1` / `SELECT ... FOR UPDATE`) si no hace falta subir el nivel.
   - **(4) Trade-off:** 1–2 frases sobre el costo de tu elección (bloqueo, reintentos, latencia).
3. (Opcional) Verifica en `psql` con **dos terminales**: abre `BEGIN;` en cada una y ejecuta los pasos en el orden del escenario.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Los tres escenarios tienen anomalía nombrada correctamente y justificada con el entrelazado.
- [ ] Distingues bien qué permite `READ COMMITTED` vs `REPEATABLE READ` (en Postgres `REPEATABLE READ` ya elimina los phantom).
- [ ] Eliges el nivel/técnica **mínimo** que basta y nombras su costo (no "todo a `SERIALIZABLE`").
- [ ] Puedes explicar **sin notas** por qué subir el nivel convierte un lost update silencioso en un error `40001` que hay que reintentar.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

La anomalía la define el **patrón**, no las tablas:
- Repetir lectura de la **misma fila** y que cambie → non-repeatable read.
- Repetir una query de **rango** y que aparezcan filas nuevas → phantom read.
- Dos sesiones leen, modifican y escriben **la misma fila** pisándose → lost update.
- Dos sesiones leen un estado común y escriben **filas distintas** que juntas rompen una invariante → write skew.

Nivel mínimo: non-repeatable y phantom los corta `REPEATABLE READ`; el write skew **solo** lo evita `SERIALIZABLE`; el lost update puro lo arregla la aritmética atómica o `FOR UPDATE` **sin** subir el nivel. Revisa la sección 4.4 de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `analisis.md` (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-3/anomalias-e-isolation.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-3/anomalias-e-isolation.md` — no la mires antes de intentarlo de verdad.
