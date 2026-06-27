---
ejercicio_id: fase-6/eleccion-vector-db
fase: fase-6
sub_unidad: "6.6"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es **una** solución defendible,
> no la única. Úsala como vara de medir la calidad del razonamiento, no para exigir coincidencia
> literal (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Decisión: vector DB + índice + métrica + filtrado

## Escenario 1 — RAG interno sobre la wiki de la empresa

- **Restricción dominante:** **operación / simplicidad** (equipo pequeño, ya corren
  Postgres, no quieren otro servicio que mantener). Volumen moderado.
- **Vector DB:** **pgvector**. Si ya hay Postgres, agregar Qdrant/Azure es complejidad
  operacional regalada: pgvector resuelve decenas de miles de páginas de sobra y reusa
  backups, transacciones y `WHERE` existentes.
- **Índice:** **HNSW**. Volumen moderado → la RAM no es problema; HNSW da mejor recall por
  latencia y se llena incremental (no exige datos antes de construir, a diferencia de
  IVFFlat).
- **Métrica:** **coseno** (texto; o producto interno si el modelo entrega vectores
  normalizados).
- **Filtrado:** **pre-filter** por `seccion`/`espacio` de la wiki (relevancia).
- **Riesgo de seguridad:** **envenenamiento del índice** — *cualquier empleado puede
  editar la wiki*, así que alguien podría plantar contenido (o instrucciones ocultas) que
  el RAG recupere y el LLM obedezca. Mitigación: validar/atribuir el ingest, tratar lo
  recuperado como **no confiable** antes de pasarlo al modelo (enlaza 6.2/6.14), y
  versionar/auditar cambios de la wiki.

## Escenario 2 — Buscador semántico SaaS multi-tenant a gran escala

- **Restricción dominante:** **escala + aislamiento multi-tenant** (decenas de millones de
  vectores, crecimiento, "ningún cliente ve a otro"). Latencia y filtrado fuerte importan.
- **Vector DB:** **Qdrant** (u otra dedicada). pgvector se queda corto en este volumen y
  en filtrado avanzado; Qdrant ofrece filtrado por payload potente, hybrid y cuantización
  para domar la RAM. (Azure AI Search también es defendible si el stack es Azure.)
- **Índice:** **HNSW** por la latencia, **pero** reconociendo el costo de RAM a decenas de
  millones → cuantización (escalar/INT8) o evaluar IVFFlat si la memoria se vuelve el
  cuello de botella. (Aceptable IVFFlat bien tuneado si priorizan costo de RAM sobre
  recall máximo.)
- **Métrica:** **coseno** / producto interno según el modelo.
- **Filtrado:** **pre-filter server-side por `tenant_id`** (o **colecciones/particiones
  separadas por tenant**). Aquí el filtro NO es relevancia: es **aislamiento**.
- **Riesgo de seguridad:** **fuga multi-tenant** — un post-filter ingenuo o un filtro
  ausente devuelve documentos de otro cliente. Mitigación: filtrado por tenant integrado
  al índice (no post-filter), idealmente aislamiento físico por colección para los datos
  más sensibles; tests que verifiquen que el tenant A nunca recibe docs del B.

## Escenario 3 — Prototipo de fin de semana en un notebook

- **Restricción dominante:** **fricción / time-to-first-result** (empezar hoy, pocos miles
  de chunks, sin operar infra). Escala y latencia no importan.
- **Vector DB:** **Chroma**, embebida en el proceso Python con persistencia en disco en una
  línea. (pgvector también vale si ya tienes Postgres local, pero Chroma es la de menor
  fricción para arrancar.)
- **Índice:** **HNSW** (el default de Chroma); a esta escala da igual el costo de RAM.
- **Métrica:** **coseno** (`configuration={"hnsw": {"space": "cosine"}}`).
- **Filtrado:** pre-filter con `where` si los apuntes tienen metadata (curso/tema); a esta
  escala el modo casi no afecta el resultado.
- **Riesgo de seguridad:** **fuga por inversión de embeddings** — aunque sea un prototipo,
  si los apuntes tuvieran algo sensible, recordar que el embedding **no es anónimo** (se
  puede reconstruir texto). Mitigación: no subir esa base a un repo público, tratarla con
  el mismo cuidado que los documentos originales.

## Qué buscar al corregir

- ¿La DB **se deriva** de la restricción, o es "la mejor"? (Esp. escenario 1: si ya hay
  Postgres y eligió algo dedicado sin razón de escala, marcar.)
- ¿Aparece el eje **memoria/construcción** en al menos un HNSW vs IVFFlat, no solo
  "velocidad"?
- ¿El escenario 2 nombra explícitamente la **fuga multi-tenant** y la resuelve con
  pre-filter/aislamiento? Es el punto central del escenario.
- ¿Cada escenario tiene **un riesgo de seguridad** con mitigación real?
- Una solución que elija distinto (p. ej. Azure AI Search en el escenario 2 por stack
  Azure, o pgvector en el 3) es **igual de válida** si el trade-off está bien argumentado.
