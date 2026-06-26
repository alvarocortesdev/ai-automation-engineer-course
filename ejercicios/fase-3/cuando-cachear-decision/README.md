# Ejercicio 3.15 — ¿Cachear o no? Decide y elige la estructura

> **Modalidad: razonamiento y diseño (Primero-Sin-IA, timebox 35 min).** No hay código que correr.
> Se evalúa tu **criterio**: la habilidad senior no es agregar una cache, es decidir con datos cuándo
> conviene, cuándo no, y con qué estructura. Decide a mano, sin IA, justificando con las métricas dadas.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.15` Redis (caching/sesiones)
**Ruta:** opcional/profundización · **Timebox:** 35 min

## 🎯 Objetivo

Para cada escenario, decidir **si** una cache (o Redis) se justifica, **cómo** (estructura, TTL,
invalidación) si la respuesta es sí, y **qué hacer en su lugar** si la respuesta es no — argumentando
siempre con las métricas, no con "porque es más rápido".

## 📋 Contexto

El reflejo de "está lento → cachéalo" es justo el hábito que esta lección reemplaza por "mide, entiende
el cuello de botella, y recién entonces decide". Este ejercicio entrena ese músculo. Alimenta la decisión
documentada en un ADR que tu capstone de la fase espera de ti.

## 📏 Primero-Sin-IA

1. Decide **solo**, a mano (timebox arriba). Está bien dudar; argumenta con lo que sabes.
2. Solo entonces, consulta la **documentación oficial** (redis.io, AWS caching strategies) si lo necesitas.
3. **Solo al final**, usa IA para *revisar y cuestionar* tus decisiones — no para *generarlas*.
4. Mañana, **rehaz una de las decisiones de memoria** y compárala con lo que escribiste.

## 🧩 Los escenarios

Decide para los **cuatro**. Las métricas son lo que tienes; no inventes datos que no están.

**Escenario A — Catálogo de productos.**
`GET /productos/{id}` recibe ~5.000 lecturas/min, p95 = 1,2 s. Los productos cambian en promedio
**una vez al día** (carga nocturna). Corriste `EXPLAIN ANALYZE` y la query hace un *seq scan* sobre
una columna usada en el `WHERE` que **no tiene índice**.

**Escenario B — Sesiones de usuario.**
Tu API corre en **3 instancias** detrás de un load balancer. Las sesiones hoy viven en la memoria del
proceso. Los usuarios reportan que "se deslogean solos" al azar varias veces al día.

**Escenario C — Precio de una criptomoneda en vivo.**
`GET /precio/btc` devuelve el precio actual, que **cambia cada segundo**. Se lee mucho (~2.000/min).
El negocio exige que el precio mostrado sea fiel al del último segundo.

**Escenario D — Límite de peticiones por IP.**
Quieres limitar a **100 peticiones/min por IP** en tus 3 instancias. Hoy cada instancia cuenta por su
cuenta, así que un cliente puede hacer 300/min repartidas entre las tres.

## 🛠️ Qué entregar

Crea `decisiones.md`. Para **cada** escenario (A–D):

- **Decisión:** ¿cachear/usar Redis sí o no? Justifícala con las **métricas dadas** (lee-mucho/cambia-poco
  vs. lo contrario; ¿el cuello de botella es la query, el diseño, o algo más?).
- **Si la respuesta es sí:** qué **estructura Redis** (string / hash / list / set / sorted set) y **por qué**;
  qué **TTL** y por qué ese número; cómo **invalidas** (o por qué el TTL basta).
- **Si la respuesta es no (o "primero otra cosa"):** qué harías en su lugar (índice, arreglar N+1, TTL mínimo, nada).
- **Riesgo:** nombra al menos un riesgo (staleness, thundering herd, race, datos volátiles) que tu decisión introduce o evita.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Las cuatro decisiones están justificadas con las métricas, no con afirmaciones genéricas.
- [ ] Al menos una decisión es **"no cachear" / "primero otra cosa"** bien argumentada.
- [ ] Cada elección de estructura calza con el caso (una sesión no es un string suelto; un contador no es una list).
- [ ] Puedes defender, sin notas, por qué cachear un dato que cambia en cada request es contraproducente.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para cada escenario pregúntate dos cosas: (1) ¿el dato se **lee mucho y cambia poco**? (eso favorece
cache); (2) ¿cuál es el **cuello de botella real**? A veces el problema no es la falta de cache sino algo
que se arregla mejor de raíz. Ojo: no todos los usos de Redis son "caching" — sesiones compartidas y
contadores de rate limit usan Redis sin ser una cache de la base de datos. Repasa las secciones 4.2 (estructuras)
y 4.6 antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `decisiones.md` (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-3/cuando-cachear-decision.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-3/cuando-cachear-decision.md` — no la mires
antes de intentarlo de verdad.
