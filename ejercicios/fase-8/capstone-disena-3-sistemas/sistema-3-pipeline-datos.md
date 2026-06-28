# Sistema 3 — "FreshIndex" (pipeline de datos para IA)

> Diséñalo **en papel**: diagrama + decisiones + ADR. Trabájalo a mano, sin IA, dentro del timebox.
> Es el sistema más nuevo del capstone: **sin esqueleto regalado**. Aplica los 6 pasos desde cero.

## Qué es

FreshIndex es el pipeline que **alimenta** un RAG (como el sistema 1). Toma documentos de varias fuentes,
los limpia y transforma, los corta en chunks, genera embeddings y los carga a una vector DB —y se
encarga de que el índice esté **fresco** cuando las fuentes cambian. El RAG consume el índice; FreshIndex
lo mantiene.

## Números (los que importan para el diseño)

- **Fuentes:** ~3 sistemas distintos — un Confluence/wiki (HTML), un bucket de PDFs (manuales) y una base
  de datos de productos (filas que cambian seguido).
- **Volumen:** ~**500.000 documentos** en total (~2 millones de chunks tras el chunking).
- **Cambios:** ~**5.000 documentos cambian o se agregan por día**, repartidos de forma desigual (la base
  de productos cambia mucho; los manuales casi nunca).
- **Costo de embeddings (ilustrativo):** USD 0,10 / millón de tokens; un chunk ~500 tokens. Un
  **re-embedding total** de los 2M de chunks cuesta del orden de cientos de USD por corrida.
- **Latencia del RAG aguas abajo:** la búsqueda vectorial necesita el índice disponible y consistente.

## Restricciones de negocio

- **Frescura:** una respuesta del RAG basada en un dato **obsoleto** es un bug silencioso peligroso (p.
  ej. un precio o una política vencida). El negocio tolera una **ventana de frescura** que *tú debes
  proponer y defender* (¿1 hora? ¿24 horas? distinta por fuente?). **Definir esa ventana es el "nunca
  más allá de X" del sistema.**
- Un documento corrupto o ilegible **no puede romper toda la corrida** del pipeline (debe aislarse, no
  tumbar el resto).
- El **modelo de embeddings** puede cambiar (mejora de versión). Cuando cambia, los vectores viejos y los
  nuevos **no son comparables**: hay que re-embeddear todo de forma controlada y versionada.
- El pipeline debe ser **observable y reproducible**: saber qué corrió, con qué datos, y poder re-correr.

## Pistas de qué decisiones esperar (no las respuestas)

ELT vs ETL; arquitectura medallion (bronze/silver/gold) vs flat; un orquestador (Dagster asset-centric o
Airflow) que dispara la transformación y luego el embedding; **data contracts** + tests de calidad
(frescura/volumen/schema drift); aislamiento de documentos malos (dead-letter); y la decisión central:
**re-embedding incremental por CDC** (solo lo que cambió) vs **rebuild nocturno completo** —con la
ventana de frescura y el costo como criterios. Más la estrategia de **versionado del modelo de
embeddings** (blue/green del índice). El **cuello de botella propio**: la frescura (latencia entre que un
dato cambia y el índice lo refleja) contra el costo del re-embedding.
