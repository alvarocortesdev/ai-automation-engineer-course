---
ejercicio_id: fase-6/diseno-llmops-plataforma
fase: fase-6
sub_unidad: "6.16"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es **una** respuesta defendible,
> no la única. El alumno debe diseñar y justificar el suyo; usa esto para evaluar la calidad del
> trade-off y detectar huecos, no para entregarle el diseño.

# Solución de referencia — La capa LLMOps de la plataforma RAG

## 1. Caching (dos capas)

**Prompt caching del provider.** Prefijo estable (cacheado a 0.1×): system prompt fijo +
instrucciones de citación + los **chunks recuperados** que se repiten en consultas similares.
Volátil (al final, sin cachear): la **pregunta del usuario** y cualquier metadato por-request. Un
error fatal es interpolar `datetime.now()` o el user_id al inicio del system prompt — rompe el
prefix match y `cache_read_input_tokens` se queda en 0. Se verifica con ese campo en cada deploy.

**Semantic cache.** Va **antes** del pipeline RAG: embeddear la pregunta, buscar la más parecida ya
respondida, y si la similitud coseno supera el umbral, servir la respuesta sin retrieval ni
generación. El umbral **no se inventa**: se calibra con el eval (6.9) — se mide qué fracción de
hits por encima de un umbral candidato son realmente correctos (faithfulness vs. la respuesta
fresca), y se elige el umbral más bajo que mantiene esa fracción alta (p. ej. ≥ 0.95 de hits
correctos). Empezar por 0.95 de similitud y bajar solo si el eval lo permite.

**Dónde NO sirve el caching:** consultas sobre datos que cambian rápido (precios, inventario,
estado de un pedido) — un hit de cache serviría un dato viejo; y prefijos de un solo uso, donde el
write a 1.25× nunca se amortiza.

## 2. Ruteo de modelos

**Escalones:** consultas factuales cortas / clasificación de la intención → **Haiku**; preguntas
estándar del RAG (recuperar + responder) → **Sonnet**; razonamiento multi-paso, síntesis larga,
consultas que el reranking marca como ambiguas → **Opus**. La **señal de dificultad** sale de
heurísticas baratas (largo de la pregunta, número de chunks relevantes, score del reranker) o de un
clasificador Haiku que solo decide el escalón antes de elegir el modelo grande.

**Evitar degradar la calidad:** el router se **evalúa** como cualquier otro componente — un eval
mide la calidad de la respuesta por escalón; si las consultas ruteadas a Haiku bajan de un umbral de
faithfulness, se sube ese tipo de consulta de escalón. El router no se confía a ciegas.

## 3. Batching

**Por Message Batches (asíncrono, 50% off):** el **ingest** (re-embeddear el corpus, generar
descripciones de chunks, backfill de un catálogo nuevo) y cualquier evaluación masiva offline.
**No puede ir por batch:** la **consulta del usuario en vivo** — es interactiva, el usuario espera
la respuesta en segundos; batching la haría inusable. El corte es por latencia: si hay un humano
esperando, es síncrono; si es trabajo de fondo, es batch.

## 4. Budget de costo/latencia (gate)

**Techo concreto:** USD ≤ 0.05 por consulta (embedding + retrieval + generación) y latencia
**p95 ≤ 3 s** (streaming: primer token ≤ 1 s). Es un **gate**: un cambio de prompt/modelo/chunking
que supere cualquiera de los dos se **bloquea en CI**, igual que el gate de regresión de calidad de
6.9. El budget es un criterio de bloqueo de primera clase, no una aspiración — se mide en el eval
harness sobre el dataset, junto con faithfulness/context recall.

## 5. LLMOps

- **Fallbacks:** cadena Opus → Sonnet → Haiku ante 429/529/5xx persistentes (el SDK ya reintenta
  con backoff); si toda la cadena falla, una respuesta degradada honesta ("no puedo responder ahora")
  en vez de un error 500 al usuario.
- **Versionado:** el prompt vive en el repo, cambia con **Conventional Commits** + un **ADR** que
  explica el porqué; el modelo se pinea explícitamente (saber a qué volver). La trazabilidad de 6.9
  ata score ↔ prompt ↔ modelo ↔ dataset.
- **Despliegue seguro:** un cambio pasa el gate de eval (calidad + budget) → sale en **canary** al
  5% del tráfico con métricas en vivo → **rollback inmediato** si USD/consulta, p95 o faithfulness
  se degradan → rollout 100% solo si el canary aguanta.
- **Monitoreo:** cada traza en **Langfuse** lleva USD, latencia (ms), score, prompt y modelo. Las
  consultas que costaron o tardaron de más, o que un usuario marcó con pulgar abajo, se **promueven
  al dataset de eval** — el ciclo se cierra y el sistema mejora solo.

## 6. Seguridad (hilo transversal)

**Riesgo:** un semantic cache mal scopeado sirve la respuesta de **un usuario a otro** — si el cache
key es solo el embedding de la pregunta, un usuario podría recibir una respuesta que contenía datos
privados de otro (sensitive information disclosure, OWASP LLM, 6.14). **Mitigación:** el cache key
incluye el **contexto de autorización** (tenant/usuario o el conjunto de documentos que el usuario
puede ver), y no se cachean respuestas que contengan PII o datos sensibles por-usuario. El caching
nunca debe cruzar el límite de autorización.

## Rango de respuestas aceptables

- Los **números** del budget (0.05 USD, 3 s p95) son ilustrativos; cualquier techo justificado y que
  actúe como gate es válido. Lo que no es válido: un budget sin números o que no bloquea.
- Los escalones de ruteo pueden variar (dos modelos en vez de tres, o un proveedor distinto) si la
  justificación por dificultad/costo está; lo que no es válido es "siempre el más potente".
- Un umbral de semantic cache distinto a 0.95 es aceptable **si** se calibra con el eval; un número
  "a ojo" no.
- Es aceptable proponer **no** usar semantic cache si el corpus cambia mucho — siempre que lo
  justifique con el riesgo de servir datos viejos.
