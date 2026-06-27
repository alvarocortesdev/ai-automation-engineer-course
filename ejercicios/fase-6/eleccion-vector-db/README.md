# Ejercicio 6.6 — Decisión: vector DB + índice + métrica + filtrado

> **Modalidad: diseño / razonamiento (sin código).** No hay tests ni función que
> implementar. Entregas un documento donde **decides y justificas** la arquitectura de
> almacenamiento vectorial para tres escenarios reales. Es exactamente lo que defiendes
> en una entrevista de AI Engineer y lo que escribes como ADR en el capstone.

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.6` Vector databases
**Ruta:** crítica · **Timebox:** 35 min · **Modalidad:** a-mano (diseño)

## 🎯 Objetivo

Para tres escenarios distintos, elegir y **justificar**: la **vector DB** (pgvector /
Qdrant / Chroma / Azure AI Search), el **tipo de índice** (HNSW vs IVFFlat, defendido por
los tres ejes: velocidad / recall / memoria-construcción), la **métrica de distancia**, la
**estrategia de filtrado** (pre vs post y qué metadata), la **restricción dominante**, y
**un riesgo de vector/embedding weakness** (envenenamiento / fuga / multi-tenant) con su
mitigación. No hay una única respuesta correcta: se evalúa la **calidad del trade-off**.

## 📋 Contexto

En el Capstone F6 escribirás un ADR ("Architecture Decision Record") explicando por qué
elegiste tal base y tal índice. Si no puedes derivar esa decisión de la restricción
dominante —y nombrar el riesgo de seguridad que introduce **tener** los embeddings—, el
revisor o el entrevistador te desarma. Este ejercicio entrena ese músculo.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba), apoyándote solo en la lección.
2. Para cada escenario, identifica **primero** la restricción que manda y deja que ella
   guíe el resto de las decisiones.
3. Solo al final, usa IA para *atacar* tus trade-offs, no para escribirlos.

## 🛠️ Instrucciones

Crea un archivo `decisiones.md` en esta carpeta. Resuelve los **tres** escenarios usando,
para cada uno, esta plantilla exacta:

```markdown
## Escenario N

- **Restricción dominante:** <privacidad | costo | latencia | memoria | escala | operación> — por qué manda aquí.
- **Vector DB:** <pgvector | Qdrant | Chroma | Azure AI Search> — justificación en 1–2 frases.
- **Índice:** <HNSW | IVFFlat> — justificado por velocidad / recall / memoria o tiempo-datos de construcción.
- **Métrica:** <coseno | producto interno | L2> — por qué.
- **Filtrado:** <pre | post> + qué metadata — por qué ese modo.
- **Riesgo de seguridad (vector/embedding weakness):** <envenenamiento | fuga por inversión | multi-tenant> + mitigación.
```

### Escenario 1 — RAG interno sobre la wiki de la empresa

Una empresa quiere un asistente RAG sobre su **wiki interna** (decenas de miles de
páginas). **Ya corren Postgres** para el resto del producto y el equipo es pequeño (no
quieren operar otro servicio). Cualquier empleado puede **editar la wiki**. Volumen
moderado, búsquedas internas.

### Escenario 2 — Buscador semántico SaaS multi-tenant a gran escala

Un SaaS ofrece búsqueda semántica a **cientos de clientes**, cada uno con sus propios
documentos. En total son **decenas de millones de vectores** y crecen rápido. Es **crítico
que un cliente nunca vea documentos de otro**. Necesitan filtrado potente y baja latencia.

### Escenario 3 — Prototipo de fin de semana en un notebook

Tú sola/o quieres prototipar un RAG sobre **tus apuntes del curso** (unos pocos miles de
chunks) en tu laptop, **hoy**, con la mínima fricción posible. No te importa la escala ni
operar infraestructura; te importa empezar ya.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Los tres escenarios resueltos con la plantilla completa.
- [ ] Cada elección de DB e índice nombra la **restricción dominante**, no "el mejor".
- [ ] Al menos un escenario justifica **HNSW vs IVFFlat** por **memoria** o por
      **tiempo/datos de construcción**, no solo "es más rápido".
- [ ] Cada escenario nombra **un riesgo de seguridad** concreto del vector store y su
      mitigación (envenenamiento, fuga por inversión, o multi-tenant).
- [ ] Puedes **defender oralmente** cada decisión sin leer tus notas.

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/eleccion-vector-db/` usando el framework de `.ai/`. Sigue
> `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-6/` — no la mires antes de
intentarlo de verdad. (Hay varias respuestas defendibles; el corrector evalúa tu
**justificación**, no que coincidas palabra por palabra.)
