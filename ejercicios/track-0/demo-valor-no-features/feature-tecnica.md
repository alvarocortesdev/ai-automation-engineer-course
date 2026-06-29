# La feature técnica a traducir (insumo del ejercicio)

> Esto es lo que "construiste", descrito como se lo contarías a otro ingeniero. Tu trabajo es
> presentárselo a **Marta, jefa de operaciones** de una distribuidora, que no sabe (ni le interesa) qué
> es un embedding. NO le muestres esto: tradúcelo.

---

## Asistente de búsqueda sobre la base de conocimiento interna

**Stack y diseño:**

- Pipeline RAG: ingest de ~4.000 documentos internos (políticas, manuales, fichas de producto) →
  chunking semántico de 512 tokens con overlap → embeddings con `text-embedding-3-large` → almacenados
  en **pgvector** sobre PostgreSQL.
- Retrieval **híbrido** (BM25 + similitud coseno) con **reranking** cross-encoder sobre el top-50; se
  pasan los 5 mejores chunks al LLM como contexto.
- Generación con un LLM con **grounding**: cada respuesta cita el documento fuente (chunk_id). Si el
  retrieval no supera un umbral de score, responde "no encontré información suficiente" en vez de
  inventar (mitigación de alucinaciones).
- **Latencia** p95 de ~1,8 segundos por consulta. **Costo** ~USD 0,003 por consulta con prompt caching.
- Evaluado con un harness propio: **0,87 de faithfulness** y **0,82 de answer relevance** sobre un set
  de 60 preguntas etiquetadas. Hay un ~13% de consultas donde el grounding es débil y conviene revisión
  humana.
- Interfaz: una caja de búsqueda en la intranet; la respuesta llega con un link al documento fuente.

**Qué resuelve técnicamente:** búsqueda semántica en lenguaje natural sobre documentación que hoy está
dispersa en carpetas de Drive y PDFs sin buscador.

---

> **Contexto del cliente (Marta):** hoy, cuando alguien del equipo necesita un dato de una política o
> ficha, busca a mano en el Drive y tarda en promedio ~15-20 minutos, y a veces no lo encuentra. Marta
> mide a su equipo por **tiempo de respuesta a clientes** y **errores por información desactualizada**.
