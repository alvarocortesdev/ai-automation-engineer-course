# SPEC — Plataforma RAG de producción

> Escribe esta spec ANTES de codear. Borra los comentarios de ayuda al completarla.

## Propósito

<!-- Una frase: qué problema real resuelve este RAG y para quién. -->

## Corpus y usuarios

- Fuente de documentos: <!-- de dónde salen, formato, volumen aproximado -->
- Usuarios reales (≥3): <!-- quiénes son, cómo accederán -->

## Contratos del sistema

### Ingest (offline, batch, idempotente)

- Entrada: <!-- documentos, formatos -->
- Chunking: <!-- estrategia + tamaño + overlap, y por qué (decisión, ver ADR) -->
- Embeddings: <!-- modelo elegido -->
- Salida: <!-- a qué vector DB, con qué metadata por chunk -->
- Idempotencia: <!-- cómo evitas duplicar al re-ingerir el mismo documento -->

### Query (online)

- Entrada: <!-- pregunta del usuario + filtros de metadata opcionales -->
- Retrieval: <!-- hybrid search (BM25 + vector), k, reranking, metadata filtering -->
- Generación: <!-- modelo, streaming, política de citas, qué hace si el contexto no responde -->
- Salida: <!-- respuesta con citas; formato del stream (SSE) -->

## Budget de costo/latencia (techo)

- Costo máximo por consulta (USD): <!-- p. ej. tope y qué pasa al excederlo -->
- Latencia objetivo: <!-- p95 objetivo; time-to-first-token objetivo -->
- Qué ocurre al exceder el techo: <!-- corta, degrada, alerta... -->

## Evals (eval-first)

- Dataset: `evals/dataset.jsonl`, <!-- N -->+ casos
- Métricas: faithfulness, context recall, context precision
- Umbral absoluto: <!-- p. ej. 0.75 --> · Tolerancia de regresión: <!-- p. ej. 0.02 -->
- Gate: bloquea el merge si cae bajo umbral O regresa vs baseline

## Seguridad (OWASP web + LLM)

- Web: <!-- rate limiting, validación de entrada, secrets fuera del repo -->
- LLM: <!-- segregación de contenido no confiable, mitigación de prompt injection
  directa e indirecta, system prompt leakage, unbounded consumption -->

## Casos borde

- Pregunta sin respuesta en el corpus → <!-- el sistema lo dice, no inventa -->
- Documento con instrucción inyectada → <!-- el sistema no obedece -->
- Documento gigante en ingest → <!-- respeta el budget -->
- Vector DB vacía / sin resultados → <!-- comportamiento definido -->

## Fuera de alcance (a propósito)

<!-- Qué NO vas a hacer en este capstone y por qué. Ej.: tool use / acciones externas
(eso es la Fase 7). Decláralo para que DoD-6 quede explícitamente "no aplica". -->
