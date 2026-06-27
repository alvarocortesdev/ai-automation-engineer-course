---
ejercicio_id: fase-6/diagnostico-rag
fase: fase-6
sub_unidad: "6.7"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Hay un **rango**
> de respuestas válidas; lo que importa es el razonamiento (etapa + descarte + métrica),
> no calzar la palabra exacta.

# Solución de referencia — Diagnóstico de un RAG que falla

## Caso A — El RAG ignora los códigos exactos

- **Síntoma:** la pregunta es por `E_4521` exacto; el chunk correcto existe pero no
  entra al top-150 recuperado. Falla de **recall**.
- **Etapa:** `retrieve`.
- **Causa raíz:** el retrieval es solo vectorial. La búsqueda semántica **no engancha
  identificadores exactos** (un código no tiene "significado" que el embedding ubique
  cerca de la consulta).
- **Técnica:** **hybrid search** — agregar BM25 (búsqueda léxica) y fusionar con RRF.
  BM25 encuentra el match exacto de `E_4521` que la semántica se pierde.
- **Alternativa descartada:** "usar un modelo de embeddings mejor / más dimensiones"
  → no arregla el problema de fondo (ningún embedding indexa bien tokens-identificador
  raros). "Subir el top-k" → mete ruido sin garantizar que aparezca el exacto.
- **Cómo lo mido:** **recall@150** sobre un set de preguntas con códigos: ¿aparece el
  chunk de `E_4521` entre los recuperados? Comparar antes (solo vectorial) vs después
  (hybrid).

## Caso B — Chunks relevantes, respuesta vaga

- **Síntoma:** los chunks recuperados son del tema correcto, pero son **ambiguos en sí
  mismos** ("la empresa creció 3%" sin empresa ni período) → respuesta vaga, mezcla
  empresas.
- **Etapa:** `chunk` / `embed` (el ingest). El chunk se embebió **aislado**, sin
  contexto del documento.
- **Causa raíz:** chunking clásico sin contexto: el vector y el texto del chunk no
  dicen de qué documento/período/entidad salen.
- **Técnica:** **Contextual Retrieval** — prepender a cada chunk, en el ingest, un
  contexto corto (empresa, período, sección) generado por un LLM barato, y embeber/
  indexar eso. Alternativa válida: **parent-document retrieval** (recuperar el chunk
  pequeño pero pasarle al LLM el documento/sección padre).
- **Alternativa descartada:** **reranking** → un cross-encoder que lee un chunk
  ambiguo junto a la pregunta **tampoco** puede saber de qué empresa habla; no arregla
  la ambigüedad intrínseca. "Subir el top-k" → trae más chunks igual de ambiguos.
- **Cómo lo mido:** **faithfulness / answer correctness** (p. ej. con ragas) sobre
  preguntas que exigen empresa+período; y recall@k antes/después de contextualizar.

## Caso C — Preguntas que cruzan documentos

- **Síntoma:** pregunta **multi-hop / relacional** ("consultores del proyecto Atlas que
  reportan a la misma gerente"); la info está repartida en varios documentos; el RAG
  trae chunks sueltos y no conecta.
- **Etapa:** `retrieve` (y el modelo de recuperación en sí: similitud por chunk no
  traversa relaciones).
- **Causa raíz:** el retrieval por similitud trae los k chunks más parecidos a la
  pregunta, pero **no sigue relaciones entre entidades** ni razona en varios pasos.
- **Técnica:** **GraphRAG** (grafo de entidades/relaciones: consultor→proyecto,
  consultor→gerente; se responde recorriéndolo) o **Agentic RAG** (un agente recupera,
  ve que le falta, reformula y vuelve a recuperar en varios pasos).
- **Alternativa descartada:** **hybrid / reranking** → siguen recuperando chunks por
  parecido; ninguno conecta hechos de documentos distintos.
- **Cómo lo mido:** tasa de **task completion** sobre preguntas multi-hop (¿la
  respuesta nombra el conjunto correcto?), más costo/pasos por consulta (Agentic y
  Graph son caros: el eval debe incluir el presupuesto).

## Decisión 1 — HNSW vs IVFFlat

- **Elijo HNSW.** Restricción dominante: **recall alto** + **inserciones constantes**,
  y hay RAM. HNSW da el mejor recall/velocidad de query y maneja bien inserciones
  incrementales; su costo es la RAM, que aquí sobra.
- **Si la RAM fuera escasa:** IVFFlat (menos memoria), aceptando algo menos de recall y
  ajustando `lists`/`probes`. Ojo: IVFFlat **se degrada con inserciones constantes** si
  no se re-entrenan los clusters con datos representativos — justo el escenario de
  "documentos nuevos cada hora", lo que refuerza HNSW aquí.

## Decisión 2 — Seguridad multi-tenant

- **Diseño:** cada chunk lleva metadata `tenant` (y/o `permisos`). Toda consulta filtra
  por el `tenant` del usuario **antes** de devolver resultados (idealmente pre-filtro en
  la DB por costo).
- **Fail-closed:** un chunk **sin** campo `tenant`, o con tenant que no coincide, **no
  se recupera**. Ante la duda, no mostrar.
- **Si falla _open_** (deja pasar lo que no cumple): un cliente recibe un chunk de otro
  cliente → **fuga de datos entre tenants**. Es un **incidente de seguridad**, no un
  bug de relevancia (alcance: confidencialidad, posible obligación de notificación).
  Por eso el control va en el filtro de retrieval, no delegado al LLM ("pídele que no
  mencione otros clientes" es exactamente la falla de control de acceso de RAG).

## Notas para el corrector

- Acepta **parent-document retrieval** como equivalente a Contextual Retrieval en el
  Caso B si el alumno justifica que resuelve la ambigüedad de contexto.
- Acepta **Agentic RAG** o **GraphRAG** en el Caso C; lo importante es que reconozca
  que es multi-hop/relacional y descarte hybrid/reranking.
- El sello de **excelente** es razonar **costo/latencia** (Contextual = una vez en
  ingest; reranking/Agentic/Graph = por query) y el **orden de diagnóstico** (recall
  primero). Un alumno que diagnostica de la generación hacia el retrieval tiene el
  árbol al revés: es el feedback más importante a dar.
