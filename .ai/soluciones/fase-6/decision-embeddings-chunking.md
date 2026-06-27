---
ejercicio_id: fase-6/decision-embeddings-chunking
fase: fase-6
sub_unidad: "6.5"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es **una** solución defendible,
> no la única. Úsala como vara de medir la calidad del razonamiento, no para exigir coincidencia
> literal (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Decisión: modelo de embeddings + chunking

## Escenario 1 — Buscador interno de manuales técnicos

- **Restricción dominante:** **privacidad** (los datos no pueden salir de la infra).
  Es una restricción *dura*: descarta cualquier API externa de entrada, sin importar
  cuánta calidad ofrezca.
- **Modelo:** **local / self-hosted**, multilingüe o específicamente bueno en
  **español** (familia tipo `multilingual-e5` o `bge-m3`, vía Sentence Transformers
  en infra propia). Dimensiones moderadas; el volumen es moderado, así que no hace
  falta recortar agresivamente. Calidad en español > tamaño del vector.
- **Chunking:** manuales largos → **párrafos de ~200–400 tokens con solape de ~15%**.
  El solape evita partir un procedimiento justo en el límite. Guardar la metadata
  (manual + página) para citar.
- **Riesgo concreto:** la **semántica sola falla con los códigos exactos** (`E_4521`,
  `SKU-99213`): la consulta "error E_4521" puede traer chunks sobre "errores" en
  general. Mitigación: **hybrid search** (coseno + BM25/palabra clave) para que el
  identificador literal se encuentre exacto (se profundiza en 6.7).

## Escenario 2 — Chatbot de soporte de e-commerce internacional

- **Restricción dominante:** **costo + latencia** (millones de consultas/mes) y
  **idioma** (varios idiomas). Datos no sensibles → la API está permitida.
- **Modelo:** un modelo **multilingüe** y **barato/rápido**. Opciones defendibles:
  API económica (`text-embedding-3-small`, con `dimensions` recortado a 256–512 para
  bajar RAM/latencia del índice), o un modelo multilingüe local pequeño si el volumen
  justifica self-hosting. La clave: multilingüe + barato, no el de máxima calidad.
- **Chunking:** las FAQs ya son cortas (1–3 frases) → **"no aplica": cada FAQ es un
  chunk**. Partirlas más las dejaría sin contexto; juntarlas mezclaría temas.
- **Riesgo concreto:** un modelo "multilingüe" puede ser mediocre en algún idioma
  concreto del catálogo de clientes. Mitigación: **medir con un eval por idioma**
  (6.9) sobre FAQs reales, no confiar en un leaderboard global.

## Escenario 3 — Deduplicar 2M de descripciones de productos

- **Restricción dominante:** **costo total** del embedding masivo (batch, una vez);
  la **latencia no importa**. Inglés, datos no sensibles.
- **Modelo:** el **más barato por token** que dé calidad suficiente. Defendible:
  `text-embedding-3-small` por API en **batch** (input es solo entrada, baratísimo;
  y la API de batch suele dar descuento), o un modelo local pequeño (`all-MiniLM-L6-v2`,
  384 dims) corriendo en GPU propia si ya se tiene el hardware ocioso. Dimensiones
  bajas ayudan: menos almacenamiento para 2M de vectores.
- **Chunking:** una descripción = un párrafo → **un chunk por producto** (no se parte;
  la unidad de dedup es el producto).
- **Riesgo concreto:** el **umbral de "casi-duplicado"** (p. ej. coseno ≥ 0.95) **no
  es universal** y depende del modelo. Si se fija a ciegas, se borran productos
  distintos o se dejan duplicados. Mitigación: **calibrar el umbral** sobre una
  muestra etiquetada a mano antes de correr sobre los 2M.

## Qué buscar al corregir

- ¿La decisión de modelo **se deriva** de la restricción dominante, o es "el mejor"?
- ¿El chunking se **adapta** al tipo de documento (manual largo vs FAQ corta vs
  producto), incluyendo reconocer cuándo "no aplica"?
- ¿Aparece al menos un **riesgo real** con mitigación (hybrid search para
  identificadores; eval por idioma; calibración de umbral)?
- Una solución que elija distinto (p. ej. local en el escenario 3 porque ya tienen
  GPU) es **igual de válida** si el trade-off está bien argumentado.
