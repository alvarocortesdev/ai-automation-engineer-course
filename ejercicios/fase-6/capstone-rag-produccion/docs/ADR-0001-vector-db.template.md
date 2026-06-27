# ADR-0001 — Elección de vector DB

- Estado: <!-- propuesta | aceptada -->
- Fecha: <!-- YYYY-MM-DD -->

## Contexto

<!-- Qué necesitas del motor de vectores: volumen de chunks, si quieres hybrid search nativo,
si ya tienes Postgres en el stack (pgvector encaja), latencia objetivo, operación/costo. -->

## Decisión

<!-- Qué motor elegiste (pgvector / Qdrant / Chroma / Azure AI Search / otro) y con qué índice
(HNSW / IVFFlat) y parámetros. -->

## Alternativas consideradas

<!-- Al menos una alternativa real, con por qué la descartaste para ESTE caso. Ej.:
- pgvector: reusa mi Postgres, una pieza menos de infra; hybrid search requiere combinar con
  full-text de Postgres.
- Qdrant: hybrid search y filtrado por metadata de primera clase; suma un servicio a operar. -->

## Consecuencias

<!-- (+) lo que ganas · (−) lo que aceptas. Sé honesto sobre el trade-off. -->

---

> Crea un segundo ADR (ADR-0002) para la estrategia de chunking/retrieval (tamaño, overlap,
> hybrid search, reranking) con la misma estructura.
